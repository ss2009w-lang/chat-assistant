import sqlite3

conn = sqlite3.connect('service.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS reports (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  category TEXT,
  priority TEXT,
  message TEXT,
  status TEXT,
  created_at TEXT
)
''')

conn.commit()
conn.close()
