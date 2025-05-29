import unittest
import subprocess
import json
import os

# Define the image name, assuming it's built as 'base-lambda-scraper'
DOCKER_IMAGE_NAME = "base-lambda-scraper"
# Define the expected output
EXPECTED_OUTPUT = {'h2_tags': ['Table playground', 'Semantically correct table with thead and tbody']}
# Import the function and custom exception to be tested
from src.main import scrape_h2_tags_from_webscraper_io, ScrapingError

class TestScrapingLogic(unittest.TestCase):

    @classmethod # This setup might still be useful for other tests that DO run the container
    def setUpClass(cls):
        """
        Optional: Build the Docker image once before all tests in this class.
        This assumes the Dockerfile is in the parent directory of this test file's location.
        Adjust the path to Dockerfile if necessary.
        """
        dockerfile_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        print(f"Attempting to build Docker image: {DOCKER_IMAGE_NAME} from {dockerfile_dir}")
        try:
            # Check if image already exists to avoid unnecessary rebuilds if not desired
            # For CI, you might always want to build.
            subprocess.run(
                ["docker", "image", "inspect", DOCKER_IMAGE_NAME],
                check=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            print(f"Docker image {DOCKER_IMAGE_NAME} already exists. Skipping build.")
        except subprocess.CalledProcessError:
            print(f"Docker image {DOCKER_IMAGE_NAME} not found. Building...")
            build_process = subprocess.run(
                ["docker", "build", "-t", DOCKER_IMAGE_NAME, "."],
                cwd=dockerfile_dir, # Run docker build from the directory containing the Dockerfile
                check=True,
                capture_output=True,
                text=True,
                timeout=300 # 5 minutes timeout for build
            )
            print("Docker image build successful.")
            # print("Build STDOUT:", build_process.stdout) # Uncomment for debugging build
            # print("Build STDERR:", build_process.stderr) # Uncomment for debugging build


    def test_scrape_function_returns_expected_json(self):
        """
        Tests that the scrape_h2_tags_from_webscraper_io function
        returns the expected JSON data.
        This test calls the function directly, not via Docker.
        """
        print("Testing scrape_h2_tags_from_webscraper_io function directly...")
        # Ensure the environment is clean for this test, e.g., RUNNING_IN_DOCKER is not set
        # unless specifically testing that scenario with mocking.
        # For this test, we assume it runs as if in a local environment.
        # If 'RUNNING_IN_DOCKER' is set in your test environment and you want to override:
        # with unittest.mock.patch.dict(os.environ, {'RUNNING_IN_DOCKER': 'false'}, clear=True):
        #    json_string_output = scrape_h2_tags_from_webscraper_io()
        
        json_string_output = None # Initialize to ensure it's defined for the except block
        try:
            json_string_output = scrape_h2_tags_from_webscraper_io()
            actual_output = json.loads(json_string_output)
            self.assertEqual(actual_output, EXPECTED_OUTPUT, "Container output did not match expected output.")
        except ScrapingError as se:
            self.fail(f"Scraping function raised an error: {se}")
        except json.JSONDecodeError as e:
            self.fail(f"Failed to decode JSON from function output: {e}\nOutput was: {json_string_output}")
        except Exception as e:
            self.fail(f"An unexpected error occurred during the test: {e}")

if __name__ == '__main__':
    unittest.main()