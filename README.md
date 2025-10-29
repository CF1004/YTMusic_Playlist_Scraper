# YTMusic_Playlist_Scraper
An automated project combining Python, Selenium, and SQL to scrape, structure, and store my personal YouTube Music playlists in a relational database.

⚙️ Overview

This project connects three key technologies — Python, Excel, and SQL — to create a full data pipeline:
1. Automated login to YouTube Music using Selenium and Chrome debugging mode.
2. Playlist scraping with dynamic scrolling and XPath-based element detection.
3. Data transfer from Excel into an SQL Server database using pyodbc and pandas.
- Designed to automate scraping for a multitude of playlists - no manual entry required.

🧰 Tools & Skills

- Python (Selenium, Pandas, PyODBC)
- SQL Server for data storage and schema design
- Excel for intermediate data cleaning
- Automation & data engineering

🧩 Project Flow
Step	Description
1. Login  Launches Chrome via debugging port and injects valid cookies for YT Music login.
2. Scrape Uses Selenium to scroll, detect, and extract playlist names, songs, artists, and albums.
3. Import	Cleans and loads the final Excel dataset into SQL tables (Playlists, Songs, Artists, etc.).

🗃️ Database Design

![Database Diagram](Database_Diagram.png)
Each table includes IDs and relationships for efficient querying and analysis.

📊 Example Output (Preview)

Since live scraping requires authentication, below is a mock example of the final data format stored in SQL:

Playlist	Song	Artist	Album
Jazz Moods	So What	Miles Davis	Kind of Blue
Road Trip Vibes	Highway Tune	Greta Van Fleet	From the Fires
Focus Session	Breathe	Pink Floyd	Dark Side of the Moon

🚀 Run Instructions

1️⃣ Start Chrome in debug mode:
"D:\Software\Chrome Browser\chrome.exe" --remote-debugging-port=9222

2️⃣ Run the scripts in order:
python 1_LoginToYTM.py
python 2_ScrapePlaylists.py
python 3_ImportToSQL.py

🧠 Highlights

End-to-end ETL pipeline (Extract → Transform → Load)
Automated web scraping with cookie-based authentication
Dynamic content handling with scrolling & XPath parsing
Multi-table relational SQL integration
No manual entry — full automation

🔍 Learnings

Handling real-world cookie authentication challenges
Structuring clean SQL schemas for scraped data
Debugging Selenium and timing issues in dynamic pages
Using Excel as a lightweight staging layer before SQL import

💬 Summary

This project demonstrates my ability to:
Automate data extraction, manage large datasets, and integrate multiple tools into a cohesive workflow — from web scraping to database management.
