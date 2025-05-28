# Add these functions outside the Config class
import os

def is_running_in_docker():
    # Check for a common Docker environment variable
    return os.environ.get('RUNNING_IN_DOCKER', '').lower() in ('true', '1')

# Third-party imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from .utils import get_chrome_options, get_chrome_service


def test_scrape_h2_tags_from_webscraper_io():
    """
    Scrapes and prints all H2 tags from https://webscraper.io/test-sites/tables.
    This function is structured as a pytest test.
    """
    options = Options()
    if is_running_in_docker():
        print("INFO: Running in Docker mode, configuring headless Chrome.")
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')  # Recommended for headless environments
        options.add_argument("window-size=1920,1080") # Specify window size for consistency
    else:
        print("INFO: Running in local mode (non-Docker).")

    driver = None  # Initialize driver to None for robust cleanup in the finally block
    try:
        print("INFO: Setting up Chrome WebDriver...")
        # Setup WebDriver using webdriver_manager to handle driver download and path
        driver = webdriver.Chrome(
            service=get_chrome_service(),
            options=get_chrome_options()
        )
        print("INFO: WebDriver setup complete.")

        url = "https://webscraper.io/test-sites/tables"
        print(f"INFO: Navigating to {url}...")
        driver.get(url)
        print(f"INFO: Page '{driver.title}' loaded successfully.")

        print("INFO: Finding H2 elements...")
        h2_elements = driver.find_elements(By.TAG_NAME, "h2")
        print(f"INFO: Found {len(h2_elements)} H2 elements.")

        print(f"\n--- H2 Tags from {url} ---")
        if h2_elements:
            for index, h2 in enumerate(h2_elements):
                print(f"{index + 1}. {h2.text.strip()}")
        else:
            print("No H2 tags found on the page.")
        print("--- End of H2 Tags ---")

    except Exception as e:
        print(f"ERROR: An error occurred during the scraping process: {e}")
    finally:
        if driver:
            print("INFO: Closing WebDriver.")
            driver.quit()
            print("INFO: WebDriver closed.")

if __name__ == "__main__":
    test_scrape_h2_tags_from_webscraper_io()