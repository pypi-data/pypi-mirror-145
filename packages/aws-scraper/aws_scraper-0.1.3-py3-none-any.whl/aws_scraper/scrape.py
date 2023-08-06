import os
import random
from abc import ABC, abstractmethod
from typing import Any, Literal

import pandas as pd
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from tryagain import retries
from webdriver_manager.chrome import ChromeDriverManager


def get_chrome_webdriver(headless: bool = False) -> webdriver.Chrome:
    """Return a new Selenium webdriver instance."""

    # Create the options
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    if headless:
        options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    return driver


class WebScraper(ABC):
    """
    Scraper abstract base class.

    Parameters
    ----------
    url :
        The url of the website to scrape
    headless :
        Whether to run the scraper in headless mode
    """

    def __init__(self, url: str, headless: bool = False) -> None:
        """Initialize the web driver."""
        # Save attributes
        self.url = url
        self.headless = headless

        # Silent
        os.environ["WDM_LOG_LEVEL"] = "0"

        # Initialize the webdriver
        self.init()

    def init(self) -> None:
        """
        Initialize the webdriver.

        This will reset the `driver` attribute.
        """
        # Get the driver
        self.driver = get_chrome_webdriver(headless=self.headless)

        # Navigate to the URL
        self.driver.get(self.url)

    def cleanup(self) -> None:
        """Clean up the web driver."""
        # Close and delete the driver
        self.driver.close()
        del self.driver

        # Log it
        logger.info("Retrying...")

    def post_call_hook(self) -> None:
        """
        Post call hook.

        This function is called after scraping each data row.
        """
        pass

    def scrape_data(
        self,
        data: pd.DataFrame,
        errors: Literal["raise", "ignore"] = "ignore",
        max_retries: int = 5,
        min_sleep: int = 30,
        max_sleep: int = 120,
        log_freq: int = 25,
    ) -> pd.DataFrame:
        """
        Scrape the data.

        Parameters
        ----------
        data :
            Scrape each row in this data frame
        errors :
            Whether to "raise" or "ignore" exceptions
        max_retries :
            After failing on a row, how many times to retry
        min_sleep :
            Minimum sleep time in seconds between retries
        max_sleep :
            Maximum sleep time in seconds between retries
        log_freq :
            How often to log messages
        """

        @retries(
            max_attempts=max_retries,
            cleanup_hook=self.cleanup,
            pre_retry_hook=self.init,
            wait=lambda n: min(min_sleep + 2 ** n + random.random(), max_sleep),
        )
        def call(i: int) -> dict[str, Any]:
            """Wrapper to __call__ for each data row."""

            # Get this data row
            row = data.iloc[i]

            # Log
            if i % log_freq == 0:
                logger.info(f"Scraping data row #{i+1}")

            # Scrape
            return self(row.to_dict())

        # Try to scrape
        results = []
        index = []
        for i in range(len(data)):

            this_result = {}
            try:
                # Call for this row
                this_result = call(i)

                # Call any post hook
                self.post_call_hook()

            except Exception as e:

                # Skip
                if errors == "ignore":
                    logger.info(f"Exception raised for i = {i}")
                    logger.info(f"Ignoring exception: {str(e)}")
                # Raise
                else:
                    logger.exception(f"Exception raised for i = {i}'")
                    raise

            # Save the scraper result
            if isinstance(this_result, dict):
                results.append(this_result)
                index.append(data.index[i])
            elif isinstance(this_result, list):
                results += this_result
                index += [data.index[i]] * len(this_result)
            else:
                raise TypeError("Scraper result must be a dict or list")

        # Log it
        logger.debug(f"Done scraping {i+1} rows")

        # Convert to a dataframe
        results = pd.DataFrame(results, index=index)

        # Return the combined results
        return data.join(results)

    @abstractmethod
    def __call__(self, row: dict[str, Any]) -> dict[str, Any]:
        """Run the scraping operation for the specified row of the data frame."""
        pass
