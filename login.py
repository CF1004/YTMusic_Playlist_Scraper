import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Step 1: Set up Selenium WebDriver with your Chrome profile
options = Options()
options.binary_location = r"D:\Software\Chrome Browser\chrome.exe"  # Adjust this path
options.add_argument("user-data-dir=C:/Users/Chraisy/AppData/Local/Google/Chrome/User Data")  # Path to your Chrome User Data folder
options.add_argument("profile-directory=Default")  # Adjust if using a different profile


# Make sure you've downloaded the appropriate ChromeDriver from https://sites.google.com/a/chromium.org/chromedriver/downloads
service = Service(r"D:\Software\Chromedriver\chromedriver-win64\chromedriver.exe")  # Replace with your ChromeDriver path
driver = webdriver.Chrome(service=service, options=options)

try:
    # Step 2: Open YouTube Music
    driver.get("https://music.youtube.com")
    time.sleep(5)  # Wait for the page to load

    # Step 3: Load Cookies from the file
    with open(r"D:/Cookies/filtered_Cookies.json", "r") as file:  # Use the filtered file
        cookies = json.load(file)
        for cookie in cookies:
            cookie.pop("sameSite", None)  # Remove if necessary
            driver.add_cookie(cookie)


    # Step 4: Refresh the page to apply cookies
    driver.refresh()
    time.sleep(5)  # Wait for the page to reload with the cookies applied

    # You should now be logged in
    print("Successfully logged in using cookies!")

    # Keep the browser open for testing
    input("Press Enter to close the browser...")  # Keeps the browser open until you press Enter
finally:
    driver.quit()  # Close the browser when done