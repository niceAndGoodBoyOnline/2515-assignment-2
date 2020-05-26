import sqlite3

conn = sqlite3.connect('backend.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE songs
          (id INTEGER PRIMARY KEY ASC,
            title TEXT NOT NULL,
            file_path TEXT NOT NULL,
            runtime TIME,
            date_added TEXT NOT NULL,
            play_count INTEGER NOT NULL,
            last_played TEXT,
            rating INTEGER,
            album TEXT,
            genre TEXT,
            artist TEXT NOT NULL,
            playlists TEXT)
          ''')
conn.commit()

c.execute('''
          CREATE TABLE playlists
          (playlist_name TEXT PRIMARY KEY NOT NULL,
          playlist_desc TEXT)
          ''')
conn.commit()

conn.close()
