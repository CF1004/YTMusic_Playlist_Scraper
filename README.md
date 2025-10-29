# YTMusic_Playlist_Scraper
An automated project combining Python, Selenium, and SQL to scrape, structure, and store my personal YouTube Music playlists in a relational database.

⚙️ Overview

This project connects three key technologies — Python, Excel, and SQL — to create a full data pipeline:
1. Automated login to YouTube Music using Selenium and Chrome debugging mode.
2. Playlist scraping with dynamic scrolling and XPath-based element detection.
3. Data transfer from Excel into an SQL Server database using pyodbc and pandas.
- Designed to automate scraping for a multitude of playlists (100,000 songs+) - no manual entry required.

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

📊 Example Output

Playlist: Black Music - Best Of
-   Song: Ready or Not Here I Come (Can't Hide from Love), Artist: The Delfonics, Album: The Sound Of Sexy Soul
-   Song: After Laughter (Comes Tears), Artist: Wendy Rene, Album: Stax-Volt: The Complete Singles 1959-1968
-   Song: Just Memories, Artist: Eddie Kendricks, Album: Keep On Truckin’: The Motown Solo Albums, Vol. 1
-   Song: Groovin', Artist: Willie Mitchell, Album: Solid Soul
-   Song: Hard Times, Artist: Baby Huey, Album: The Baby Huey Story: The Living Legend
-   Song: Anywhere in Glory, Artist: The Mighty Indiana Travelers, Album: LAMP Records - It Glowed Like the Sun: The Story of Naptown's Motown (1969-1972)
-   Song: Free, Artist: Deniece Williams, Album: This Is Niecy (Expanded Edition)
-   Song: You've Really Got A Hold On Me, Artist: The Miracles, Album: The Chaperone
-   Song: Turn on Some Music, Artist: Marvin Gaye, Album: Midnight Love
-   Song: 'Til Tomorrow, Artist: Marvin Gaye, Album: Midnight Love
-   Song: Love's In Need Of Love Today, Artist: Stevie Wonder, Album: Songs In The Key Of Life
-   Song: Give You What I Got, Artist: Wendy Rene, Album: Stax-Volt: The Complete Singles 1959-1968
-   Song: I'd Rather Go Blind, Artist: Etta James, Album: Tell Mama
-   Song: Inside My Love, Artist: Minnie Riperton, Album: Adventures In Paradise
-   Song: 溫泉鄉的吉他, Artist: 李雅芳, Album: 一曲情未了
-   Song: Love Ballad, Artist: L.T.D., Album: Love To The World

Playlist: Purity Ring - Best Of
-   Song: belispeak, Artist: Purity Ring, Album: shrines
-   Song: obedear, Artist: Purity Ring, Album: shrines
-   Song: lofticries, Artist: Purity Ring, Album: shrines
-   Song: fineshrine, Artist: Purity Ring, Album: shrines
-   Song: heartsigh, Artist: Purity Ring, Album: another eternity
-   Song: push pull, Artist: Purity Ring, Album: another eternity
-   Song: bodyache, Artist: Purity Ring, Album: another eternity
-   Song: begin again, Artist: Purity Ring, Album: another eternity
-   Song: pink lightning, Artist: Purity Ring, Album: Womb
-   Song: sinew, Artist: Purity Ring, Album: Womb
-   Song: peacefall, Artist: Purity Ring, Album: Womb
-   Song: i like the devil, Artist: Purity Ring, Album: Womb
-   Song: stardew, Artist: Purity Ring, Album: Womb
-   Song: neverend, Artist: Purity Ring, Album: graves
-   Song: soshy, Artist: Purity Ring, Album: graves
-   Song: graves, Artist: Purity Ring, Album: graves

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
