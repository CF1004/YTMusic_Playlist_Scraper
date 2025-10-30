import pandas as pd
import pyodbc

# ------------------------------
# CONFIGURATION
# ------------------------------
SERVER = r'SERVER_NAME'       # e.g., localhost\SQLEXPRESS
DATABASE = 'DATABASE_NAME'    # e.g., Playlists
EXCEL_FILE_PATH = r'PATH_TO_EXCEL_FILE.xlsx'  # Local Excel file

# ------------------------------
# MAIN SCRIPT
# ------------------------------
def main():
    # Connect to the SQL Server
    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={SERVER};'
            f'DATABASE={DATABASE};'
            f'Trusted_Connection=yes'
        )
        cursor = conn.cursor()
        print("✅ Database connection successful!")
    except Exception as e:
        print("❌ Error connecting to the database:", e)
        return

    # Load Excel file
    try:
        df = pd.read_excel(EXCEL_FILE_PATH, sheet_name='Sheet1')
        print("✅ Excel file loaded successfully!")
        print(df.head())
    except Exception as e:
        print("❌ Error reading Excel file:", e)
        return

    # Initialize ID counters
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
        print("✅ Playlists inserted successfully!")
    except Exception as e:
        print("❌ Error inserting Playlists:", e)

    # Insert Songs and Songs_Playlists
    try:
        for _, row in df.iterrows():
            playlist_id = playlist_ids[row['p_name']]
            song_key = (row['s_name'], row['album'])
            if song_key not in songs_ids:
                songs_ids[song_key] = current_song_id
                cursor.execute(
                    "INSERT INTO Songs (s_id, s_name, album) VALUES (?, ?, ?)",
                    current_song_id, row['s_name'], row['album']
                )
                current_song_id += 1

            cursor.execute(
                "INSERT INTO Songs_Playlists (s_id, p_id) VALUES (?, ?)",
                songs_ids[song_key], playlist_id
            )
        print("✅ Songs and Songs_Playlists inserted successfully!")
    except Exception as e:
        print("❌ Error inserting Songs or Songs_Playlists:", e)

    # Insert Artists and Songs_Artists
    try:
        for _, row in df.iterrows():
            song_id = songs_ids[(row['s_name'], row['album'])]
            artist_name = row['a_name']
            p_id = playlist_ids[row['p_name']]

            if artist_name not in artists_ids:
                artists_ids[artist_name] = current_artist_id
                cursor.execute(
                    "INSERT INTO Artists (a_id, a_name, p_id) VALUES (?, ?, ?)",
                    current_artist_id, artist_name, p_id
                )
                current_artist_id += 1

            cursor.execute(
                "INSERT INTO Songs_Artists (s_id, a_id) VALUES (?, ?)",
                song_id, artists_ids[artist_name]
            )
        print("✅ Artists and Songs_Artists inserted successfully!")
    except Exception as e:
        print("❌ Error inserting Artists or Songs_Artists:", e)

    # Commit and close
    try:
        conn.commit()
        print("✅ All data committed successfully!")
    except Exception as e:
        print("❌ Error during commit:", e)
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")

# Entry point
if __name__ == "__main__":
    main()
