import sqlite3

conn = sqlite3.connect('student_db.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE student_tbl
          ''')

conn.commit()
conn.close()
