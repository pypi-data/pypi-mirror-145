import pandas as pd
import simplejson as json
from dotenv import find_dotenv, load_dotenv
from s3fs import S3FileSystem

from . import aws


def load_data_from_s3(path: aws.S3Path) -> pd.DataFrame:
    """Load data from s3."""

    # Check extension
    allowed_extensions = [".csv", ".json"]
    if not any(str(path).endswith(ext) for ext in allowed_extensions):
        raise RuntimeError(f"Allowed file extensions: {allowed_extensions}")

    # Load env variables
    load_dotenv(find_dotenv())

    # Set up s3 file system
    fs = S3FileSystem()

    # Open and read
    with fs.open(path, "rb") as ff:

        if str(path).endswith(".csv"):
            return pd.read_csv(ff)
        else:
            return json.loads(ff.read())


def save_csv_data_to_s3(data: pd.DataFrame, path: aws.S3Path) -> None:
    """Write CSV data to s3."""

    # Load .csv
    if not str(path).endswith(".csv"):
        raise RuntimeError("Only csv files can be saved to s3")

    # Load env variables
    load_dotenv(find_dotenv())

    # Set up s3 file system
    fs = S3FileSystem()

    # Make sure the bucket exists
    bucket_name = path.bucket_name
    if not fs.exists(bucket_name):
        fs.mkdir(bucket_name)

    # Write the data
    with fs.open(path, "w") as ff:
        data.to_csv(ff, index=False)


def save_json_data_to_s3(data: list, path: aws.S3Path) -> None:
    """Write JSON data to s3."""

    # Load .csv
    if not str(path).endswith(".json"):
        raise RuntimeError("Only JSON files can be saved to s3")

    # Load env variables
    load_dotenv(find_dotenv())

    # Set up s3 file system
    fs = S3FileSystem()

    # Make sure the bucket exists
    bucket_name = path.bucket_name
    if not fs.exists(bucket_name):
        fs.mkdir(bucket_name)

    # Write the data
    with fs.open(path, "w") as ff:
        ff.write(json.dumps(data, ignore_nan=True))
