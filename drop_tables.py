import sqlite3

conn = sqlite3.connect('backend.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE songs
          ''')

conn.commit()

c.execute('''
          DROP TABLE playlists
          ''')

conn.commit()


conn.close()
