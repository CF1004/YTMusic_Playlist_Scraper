import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# ------------------------------
# CONFIGURATION
# ------------------------------
CHROME_DRIVER_PATH = "PATH_TO_CHROMEDRIVER"           # Path to ChromeDriver executable
CHROME_USER_DATA = "PATH_TO_CHROME_USER_DATA"        # Path to Chrome User Data
CHROME_PROFILE = "PROFILE_NAME"                      # e.g., Default
COOKIES_FILE = "PATH_TO_COOKIES_JSON"               # Path to your cookies JSON
YOUTUBE_MUSIC_URL = "https://music.youtube.com"      # URL to open

# ------------------------------
# FUNCTIONS
# ------------------------------
def setup_driver():
    """Set up and return a Selenium Chrome WebDriver."""
    options = Options()
    # options.binary_location = r"PATH_TO_CHROME_BINARY"  # Optional if Chrome is default
    options.add_argument(f"user-data-dir={CHROME_USER_DATA}")
    options.add_argument(f"profile-directory={CHROME_PROFILE}")

    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def load_cookies(driver, cookies_file):
    """Load cookies from a JSON file into the Selenium driver."""
    with open(cookies_file, "r") as file:
        cookies = json.load(file)
        for cookie in cookies:
            cookie.pop("sameSite", None)  # Remove unsupported attribute
            driver.add_cookie(cookie)


def main():
    driver = setup_driver()
    try:
        driver.get(YOUTUBE_MUSIC_URL)
        time.sleep(5)  # Wait for page to load

        load_cookies(driver, COOKIES_FILE)
        driver.refresh()
        time.sleep(5)  # Wait for page to reload with cookies applied

        print("✅ Successfully logged in using cookies!")

    finally:
        driver.quit()
        print("Browser closed.")


# ------------------------------
# ENTRY POINT
# ------------------------------
if __name__ == "__main__":
    main()
