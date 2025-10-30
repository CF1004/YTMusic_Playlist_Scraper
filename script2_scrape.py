import time
import json
import datetime
import pytz
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ------------------------------
# CONFIGURATION
# ------------------------------
CHROME_DRIVER_PATH = "PATH_TO_CHROMEDRIVER"          # Path to ChromeDriver executable
CHROME_DEBUGGER_ADDRESS = "127.0.0.1:9222"          # Chrome debugging port (if using remote debugging)
COOKIES_FILE = "PATH_TO_COOKIES_JSON"               # Path to cookies JSON
BASE_URL = "https://music.youtube.com"

TOTAL_PLAYLISTS_NEEDED = 50                          # Number of playlists to scrape

# ------------------------------
# DRIVER SETUP
# ------------------------------
def setup_driver():
    """Set up Selenium WebDriver with optional debugger address."""
    options = Options()
    # Connect to a running Chrome instance if debugging (optional)
    # options.debugger_address = CHROME_DEBUGGER_ADDRESS
    
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# ------------------------------
# COOKIE HANDLING
# ------------------------------
def filter_invalid_cookies(cookies):
    """Filter out cookies that are expired or invalid."""
    valid_cookies = []
    for cookie in cookies:
        expiry = cookie.get('expirationDate')
        if isinstance(expiry, (int, float)) and expiry > time.time():
            valid_cookies.append(cookie)
    return valid_cookies

def load_filtered_cookies(driver, cookies_file):
    """Load cookies from a JSON file into the Selenium driver."""
    driver.get(f"{BASE_URL}/library/playlists")
    time.sleep(5)
    
    with open(cookies_file, "r") as f:
        cookies = json.load(f)
    
    valid_cookies = filter_invalid_cookies(cookies)
    for cookie in valid_cookies:
        cookie_dict = {
            'name': cookie['name'],
            'value': cookie['value'],
            'path': cookie.get('path', '/'),
            'domain': cookie.get('domain', '.youtube.com'),
            'secure': cookie.get('secure', False),
            'httpOnly': cookie.get('httpOnly', False),
        }
        expiry = cookie.get('expirationDate')
        if expiry:
            if expiry > 10000000000:  # convert ms to s if needed
                expiry = int(expiry / 1000)
            cookie_dict['expiry'] = int(expiry)
        try:
            driver.add_cookie(cookie_dict)
        except Exception:
            pass
    
    driver.refresh()
    time.sleep(5)

# ------------------------------
# LOGIN CHECK
# ------------------------------
def check_if_logged_in(driver):
    """Check if user is logged in using a visible element as proxy."""
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "yt-img-shadow"))
        )
        print("✅ Successfully logged in.")
    except:
        print("❌ Failed to log in. Exiting.")
        driver.quit()
        exit()

# ------------------------------
# SCROLLING & PLAYLIST LOADING
# ------------------------------
def scroll_to_load_playlists(driver, max_scrolls=20, scroll_pause_time=3):
    """Scroll down the page to load more playlists dynamically."""
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    
    for _ in range(max_scrolls):
        driver.execute_script("window.scrollBy(0, 5000);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scrape_playlists(driver, total_playlists_needed=TOTAL_PLAYLISTS_NEEDED):
    """Scrape playlist names and URLs with incremental scrolling."""
    playlists = []
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ytmusic-two-row-item-renderer"))
        )
        
        playlist_elements = driver.find_elements(By.XPATH, "//ytmusic-two-row-item-renderer//yt-formatted-string//a")
        
        while len(playlist_elements) < total_playlists_needed:
            scroll_to_load_playlists(driver)
            playlist_elements = driver.find_elements(By.XPATH, "//ytmusic-two-row-item-renderer//yt-formatted-string//a")
        
        for element in playlist_elements:
            name = element.text.strip()
            url = element.get_attribute("href")
            if name and url and name not in ["New Playlist", "Liked Music"]:
                playlists.append({"playlist_name": name, "playlist_url": url})
    except Exception as e:
        print(f"Error scraping playlists: {e}")
    return playlists

# ------------------------------
# SONG SCRAPING
# ------------------------------
def scrape_songs_from_playlist(driver, playlist_url):
    """Scrape songs from a single playlist."""
    driver.get(playlist_url)
    time.sleep(5)
    songs_data = []
    
    song_elements = driver.find_elements(By.XPATH, "//ytmusic-responsive-list-item-renderer")
    for song in song_elements:
        try:
            song_name = song.find_element(By.XPATH, './div[2]/div[1]/yt-formatted-string/a').text
            artist_name = song.find_element(By.XPATH, './div[2]/div[3]/yt-formatted-string[1]/a').text
            album_name = song.find_element(By.XPATH, './div[2]/div[3]/yt-formatted-string[2]/a').text
            songs_data.append({
                "song_name": song_name,
                "artist_name": artist_name,
                "album_name": album_name
            })
        except Exception:
            pass
    return songs_data

# ------------------------------
# MAIN EXECUTION
# ------------------------------
def main():
    driver = setup_driver()
    try:
        load_filtered_cookies(driver, COOKIES_FILE)
        check_if_logged_in(driver)
        
        playlists = scrape_playlists(driver)
        all_data = []
        
        for playlist in playlists:
            songs = scrape_songs_from_playlist(driver, playlist["playlist_url"])
            all_data.append({
                "playlist_name": playlist["playlist_name"],
                "songs": songs
            })
        
        # Print scraped data (for demonstration purposes)
        for playlist in all_data:
            print(f"Playlist: {playlist['playlist_name']}")
            for song in playlist["songs"]:
                print(f"  Song: {song['song_name']}, Artist: {song['artist_name']}, Album: {song['album_name']}")
    
    finally:
        driver.quit()
        print("Browser closed.")

# Entry point
if __name__ == "__main__":
    main()

