from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import datetime
import pytz

# Setup Chrome options and driver
options = Options()
options.debugger_address = "127.0.0.1:9222"  # Connect to Chrome running on the debugging port
driver = webdriver.Chrome(service=Service(r"D:\Software\Chromedriver\chromedriver-win64\chromedriver.exe"), options=options)

print("Driver started")  # This will print to confirm if the driver was successfully initialized

print("Current URL:", driver.current_url)

time.sleep(5)  # Wait to ensure the browser is fully ready
print("Current URL after delay:", driver.current_url)


# Function to filter out invalid cookies
def filter_invalid_cookies(cookies):
    valid_cookies = []
    for cookie in cookies:
        if isinstance(cookie.get('expirationDate'), (int, float)):
            expiry_timestamp = cookie['expirationDate']
            if expiry_timestamp > time.time():
                valid_cookies.append(cookie)
            else:
                print(f"Skipping expired cookie: {cookie['name']}")
        else:
            print(f"Skipping cookie without valid expiry: {cookie['name']}")
    return valid_cookies


# Function to load cookies from the filtered_Cookies file
def load_filtered_Cookies():
    driver.get("https://music.youtube.com/library/playlists")
    time.sleep(5)  # Allow the page to load
    
    # Load the cookies from the filtered_Cookies file
    with open(r"D:/Cookies/filtered_Cookies.json", "r") as f:
        cookies = json.load(f)
        print(f"Loaded {len(cookies)} cookies.")  # Print how many cookies were loaded
        
        # Filter out invalid cookies based on expiration date
        valid_cookies = filter_invalid_cookies(cookies)
        
        for cookie in valid_cookies:
            print(cookie)  # Print each cookie to verify
            
            cookie_dict = {
                'name': cookie['name'],
                'value': cookie['value'],
                'path': cookie.get('path', '/'),
                'domain': cookie.get('domain', '.youtube.com'),
                'secure': cookie.get('secure', False),
                'httpOnly': cookie.get('httpOnly', False),
            }
            
            # Handle expiration date, ensuring it's a valid Unix timestamp
            expiry = cookie.get('expirationDate', None)
            if expiry:
                if expiry > 10000000000:  # Likely in milliseconds
                    expiry = int(expiry / 1000)  # Convert to seconds
                cookie_dict['expiry'] = int(expiry)
            
            try:
                driver.add_cookie(cookie_dict)
                print(f"Cookie {cookie['name']} added.")
            except Exception as e:
                print(f"Error adding cookie {cookie['name']}: {e}")
    
    driver.refresh()  # Refresh to make sure cookies are loaded and session is active


# Function to check if the user is logged in
def check_if_logged_in():
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "yt-img-shadow"))
        )
        print("Successfully logged in.")
    except:
        print("Failed to log in.")
        driver.quit()
        exit()

# Function to scroll the page until all playlists are loaded
def scroll_to_load_playlists(driver, max_scrolls=20, scroll_pause_time=3):
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    
    for _ in range(max_scrolls):
        # Scroll by a larger increment for better loading of playlists
        driver.execute_script("window.scrollBy(0, 5000);")  # Scroll by 5000 pixels
        time.sleep(scroll_pause_time)  # Wait for new content to load

        # Check the new height of the page
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        
        if new_height == last_height:
            print("No new playlists loaded.")
            break  # Stop if no new playlists are loaded

        last_height = new_height  # Update the height for the next iteration



# Function to scrape playlists with incremental scrolling
def scrape_playlists(total_playlists_needed=50):
    playlists = []
    
    try:
        print("Waiting for playlists to load...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ytmusic-two-row-item-renderer"))
        )
        print("Playlists are loaded.")
        
        # Start of playlist extraction process
        print("Searching for playlist elements...")
        
        # Initially find the playlists
        playlist_elements = driver.find_elements(By.XPATH, "//ytmusic-two-row-item-renderer//yt-formatted-string//a")
        print(f"Found {len(playlist_elements)} playlist(s) initially.")
        
        # Continue scrolling and extracting playlists until the total number is met
        while len(playlist_elements) < total_playlists_needed:  # Add logic to determine total_playlists_needed
            scroll_to_load_playlists(driver)  # Scroll the page
            playlist_elements = driver.find_elements(By.XPATH, "//ytmusic-two-row-item-renderer//yt-formatted-string//a")
            print(f"Found {len(playlist_elements)} playlists after scrolling.")
        
        # Extract the playlist details
        for element in playlist_elements:
            playlist_name = element.text.strip()
            playlist_url = element.get_attribute("href")
            
            if playlist_name and playlist_url:
                # Skip specific playlists (New Playlist, Liked Music)
                if playlist_name in ["New Playlist", "Liked Music"]:
                    print(f"Skipping playlist: {playlist_name}")
                    continue
                
                print(f"Scraping playlist: {playlist_name}")
                playlists.append({
                    "playlist_name": playlist_name,
                    "playlist_url": playlist_url
                })
            
    except Exception as e:
        print(f"Error: {e}")
    
    return playlists


# Function to scrape songs from a playlist
def scrape_songs_from_playlist(playlist_url):
    driver.get(playlist_url)
    time.sleep(5)  # Wait for the playlist page to load
    
    songs_data = []
    
    # Wait for the song elements to load
    song_elements = driver.find_elements(By.XPATH, "//ytmusic-responsive-list-item-renderer")

    for song_element in song_elements:
        try:
            # Extract song name, artist name, and album name using the provided XPaths
            song_name = song_element.find_element(By.XPATH, './div[2]/div[1]/yt-formatted-string/a').text
            artist_name = song_element.find_element(By.XPATH, './div[2]/div[3]/yt-formatted-string[1]/a').text
            album_name = song_element.find_element(By.XPATH, './div[2]/div[3]/yt-formatted-string[2]/a').text

            # Append song data to the list
            songs_data.append({
                "song_name": song_name,
                "artist_name": artist_name,
                "album_name": album_name
            })
        except Exception as e:
            print(f"Error extracting song details: {e}")
    
    return songs_data


# Main part of your script
load_filtered_Cookies()  # Load cookies
check_if_logged_in()  # Check if logged in

playlists = scrape_playlists()  # Scrape playlists
all_playlists_data = []

for playlist in playlists:
    print(f"Scraping {playlist['playlist_name']}...")
    
    # Call the scrape_songs_from_playlist function with the playlist URL
    songs_data = scrape_songs_from_playlist(playlist["playlist_url"])
    
    # Store the songs data for this playlist
    all_playlists_data.append({
        "playlist_name": playlist["playlist_name"],
        "songs": songs_data
    })

# Print the scraped data (for testing purposes)
for playlist in all_playlists_data:
    print(f"Playlist: {playlist['playlist_name']}")
    for song in playlist["songs"]:
        print(f"  Song: {song['song_name']}, Artist: {song['artist_name']}, Album: {song['album_name']}")

# Close the WebDriver
driver.quit()
