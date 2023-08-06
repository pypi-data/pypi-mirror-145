from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_webdriver(headless=False):
    """Return a new webdriver instance."""

    # Create the options
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    if headless:
        options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    return driver


def is_element_present(driver, how, what):
    """Return True if the element is present."""
    try:
        driver.find_element(by=how, value=what)
    except NoSuchElementException:
        return False
    return True
