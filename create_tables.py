import sqlite3

conn = sqlite3.connect('student_db.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE student_tbl
          (student_id TEXT PRIMARY KEY,
           first_name TEXT NOT NULL,
           last_name TEXT NOT NULL)
          ''')

conn.commit()
conn.close()
