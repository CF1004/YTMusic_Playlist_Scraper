## ⚠️ Note on Login / Cookies Due to YouTube Music’s authentication structure, session cookies must be manually extracted & updated to enable login automation. This project demonstrates the scraping and database design logic, but running it fully requires: 
- Valid user session cookies
- Selenium WebDriver setup
- Basic knowledge of browser debugging tools

Preparation:
Log into your YouTube Music Account and extract your session cookies. You need a Chrome Extension called "EditThisCookie2"

1. Download Google Chrome Developer Version
2. Navigate to the Chrome Version folder
3. Open Chrome with Debugging Command -> Windows + R -> enter your path and command -> "D:\Software\Chrome Browser\chrome.exe" --remote-debugging-port=9222
4. Run the first Python script 'SuccessfulLoggingIntoYTM'. This will fail because you need to put in your paths first (into the script) and maybe filter the session cookies. You will have to work with the error messages
5. If you are logged in successfully (which is the hardest part), run Python script 'WorkingScrape2.0.1'
6. Wait
7. If everything worked fine you can copy and paste the data into Excel and arrange it to your liking.
8. You now have a lot of data from all playlists you have created.
