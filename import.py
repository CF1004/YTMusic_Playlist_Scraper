import pandas as pd
import pyodbc

# Replace these with your server and database details
server = r'BLACK-BEAUTY\SQLEXPRESS'
database = 'Playlists'

try:
    # Set up the connection
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'Trusted_Connection=yes'
    )
    cursor = conn.cursor()
    print("Connection successful!")
except Exception as e:
    print("Error while connecting to the database:", e)
    exit()

# Load your Excel file
file_path = r'C:\Users\Chraisy\Desktop\Data Analytics\Projects\PlaylistData3.0.xlsx'
try:
    df = pd.read_excel(file_path, sheet_name='Sheet1')
    print("Excel file loaded successfully!")
    print(df.head())
except Exception as e:
    print("Error while reading the Excel file:", e)
    exit()

# Initialize ID counters starting from 1000
current_playlist_id = 1000
current_song_id = 1000
current_artist_id = 1000

# Dictionaries to track IDs
playlist_ids = {}
songs_ids = {}
artists_ids = {}

# Insert Playlists
try:
    for playlist_name in df['p_name'].unique():
        playlist_ids[playlist_name] = current_playlist_id
        cursor.execute(
            "INSERT INTO Playlists (p_id, p_name) VALUES (?, ?)",
            current_playlist_id, playlist_name
        )
        current_playlist_id += 1
    print("Playlists inserted successfully!")
except Exception as e:
    print("Error inserting data into Playlists:", e)

# Insert Songs and Songs_Playlists
try:
    for _, row in df.iterrows():
        playlist_id = playlist_ids[row['p_name']]

        # Insert into Songs table (without p_id)
        song_key = (row['s_name'], row['album'])  # Unique song key
        if song_key not in songs_ids:
            songs_ids[song_key] = current_song_id
            cursor.execute(
                "INSERT INTO Songs (s_id, s_name, album) VALUES (?, ?, ?)",
                current_song_id, row['s_name'], row['album']
            )
            current_song_id += 1

        # Insert into Songs_Playlists
        cursor.execute(
            "INSERT INTO Songs_Playlists (s_id, p_id) VALUES (?, ?)",
            songs_ids[song_key], playlist_id
        )
    print("Songs and Songs_Playlists inserted successfully!")
except Exception as e:
    print("Error inserting data into Songs or Songs_Playlists:", e)

# Insert Artists and Songs_Artists
try:
    for _, row in df.iterrows():
        song_id = songs_ids[(row['s_name'], row['album'])]

        # Insert into Artists table
        artist_name = row['a_name']
        p_id = playlist_ids[row['p_name']]  # Fetch the playlist ID

        if artist_name not in artists_ids:
            artists_ids[artist_name] = current_artist_id
            cursor.execute(
                "INSERT INTO Artists (a_id, a_name, p_id) VALUES (?, ?, ?)",  # Include p_id here
                current_artist_id, artist_name, p_id
            )
            current_artist_id += 1

        # Insert into Songs_Artists
        cursor.execute(
            "INSERT INTO Songs_Artists (s_id, a_id) VALUES (?, ?)",
            song_id, artists_ids[artist_name]
        )
    print("Artists and Songs_Artists inserted successfully!")
except Exception as e:
    print("Error inserting data into Artists or Songs_Artists:", e)

# Commit and close the connection
try:
    conn.commit()
    print("All data inserted and committed successfully!")
except Exception as e:
    print("Error during commit:", e)
finally:
    cursor.close()
    conn.close()
    print("Database connection closed.")
