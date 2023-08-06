from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import boto3
from dotenv import find_dotenv, load_dotenv
from loguru import logger
from s3fs import S3FileSystem


@dataclass(frozen=True)
class S3Path:
    """A path on AWS s3."""

    path: str

    def __post_init__(self):
        """Verify input."""

        if not self.path.startswith("s3://"):
            raise ValueError("Path must start with s3://")

    def __str__(self) -> str:
        return self.path

    @property
    def path_no_prefix(self):
        """The path without the s3 prefix."""
        return self.path[5:]

    @property
    def bucket_name(self) -> str:
        """Return the bucket name."""
        return self.path_no_prefix.split("/", maxsplit=1)[0]

    @property
    def key(self) -> str:
        """Return the path key"""
        return self.path_no_prefix.split("/", maxsplit=1)[1]


def running_on_aws() -> None:
    """Check if an instance is running on ECS Fargate on AWS."""
    return os.getenv("AWS_EXECUTION_ENV") == "AWS_ECS_FARGATE"


@dataclass
class AWSConnection:
    """Connection to Amazon Web Services."""

    bucket_name: str
    cluster_name: str
    task_family: str
    debug: bool = False

    def __post_init__(self) -> None:
        """Initialize the connection to AWS."""

        # Load any environment variables from .env files
        load_dotenv(find_dotenv())

        # Container name should be in the .env file
        self.container_name = os.getenv("CONTAINER_NAME")
        if self.container_name is None:
            raise ValueError("Please specify 'CONTAINER_NAME' in .env file")

        # Set up the AWS session
        # This searches for AWS credentials in the environment
        self.session = boto3.Session(
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

        # Set up the file systems
        self.remote = S3FileSystem()

        # Set up clients
        self.ecs = self.session.client("ecs")
        self.ec2 = self.session.client("ec2")
        self.s3 = self.session.client("s3")

        # Set up the output s3 bucket (and create it if we need to)
        if not self.remote.exists(self.bucket_name):
            self.s3.create_bucket(Bucket=self.bucket_name)

        # Are we running on AWS
        self.on_aws = running_on_aws()

    def initialize_ecs_cluster(self) -> None:
        """
        Initialize the ECS cluster.

        This will set the following attributes:
            - `subnets` : cluster subnets
            - `task_definition` : task definition we are using
        """

        # Verify that the cluster exists
        clusters = self.ecs.list_clusters()
        cluster_names = [c.split("/")[-1] for c in clusters["clusterArns"]]
        if self.cluster_name not in cluster_names:
            raise RuntimeError(f"Missing ECS cluster: {self.cluster_name}")

        # Get the subnets
        self.subnets = [d["SubnetId"] for d in self.ec2.describe_subnets()["Subnets"]]
        if self.debug:
            logger.info(f"Subnets: {self.subnets}")

        # Get the latest task definition
        definitions = self.ecs.list_task_definitions(
            familyPrefix=self.task_family, sort="ASC"
        )["taskDefinitionArns"]

        if not len(definitions):
            raise RuntimeError(
                f"No task definitions with prefix '{self.task_family}' found"
            )

        # Use the latest (last)
        self.task_definition = definitions[-1]

        if self.debug:
            logger.info(f"Task definition: {self.task_definition}")

    def list_files(self, pattern: str) -> list[str]:
        """List remote files on AWS that match the specified pattern."""

        # Invalidate the cache first
        self.remote.invalidate_cache()

        # Return the pattern glob
        return self.remote.glob(pattern)

    def submit_job(self, command) -> dict[str, Any]:
        """Submit jobs to the ECS cluster."""

        # Initialize the cluster if we need to
        if not hasattr(self, "subnets"):
            raise RuntimeError(
                "Please initialize cluster by calling initialize_ecs_cluster()"
            )

        # Set the network config
        NETWORK_CONFIG = {
            "awsvpcConfiguration": {
                "assignPublicIp": "ENABLED",
                "subnets": self.subnets,
            }
        }

        # Submit the task
        task = self.ecs.run_task(
            taskDefinition=self.task_definition,
            cluster=self.cluster_name,
            networkConfiguration=NETWORK_CONFIG,
            launchType="FARGATE",
            overrides={
                "containerOverrides": [
                    {"name": self.container_name, "command": command}
                ]
            },
        )

        # Check if provisioning failed:
        failed = len(task["tasks"]) == 0 and len(task["tasks"]["failures"]) > 0
        if failed:
            reason = task["tasks"]["failures"][0]["reason"]
            raise ValueError(f"Task provisioning failed: {reason}")

        return task

    def wait_for_tasks(self, tasks: list[dict[str, Any]]) -> None:
        """Wait for tasks to finish"""

        # Get the task ids
        task_ids = [task["tasks"][0]["taskArn"] for task in tasks]

        # Wait for all jobs to complete
        logger.info(f"Waiting for tasks to complete")
        waiter = self.ecs.get_waiter("tasks_stopped")
        waiter.wait(
            cluster=self.cluster_name,
            tasks=task_ids,
            WaiterConfig={"Delay": 60, "MaxAttempts": 500},
        )
        logger.info(f"...all tasks completed")

        # Check for errors
        task_results = self.ecs.describe_tasks(
            cluster=self.cluster_name, tasks=task_ids
        )

        # Check the exit codes
        exit_codes = [
            task["containers"][0]["exitCode"] for task in task_results["tasks"]
        ]
        if any([code != 0 for code in exit_codes]):
            raise ValueError("One or more tasks failed!")
