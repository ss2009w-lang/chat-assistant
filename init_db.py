import sqlite3

conn = sqlite3.connect('service.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS tickets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  email TEXT,
  phone TEXT,
  type TEXT,
  created_at TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS ratings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  rating INTEGER,
  created_at TEXT
)
''')

conn.commit()
conn.close()
