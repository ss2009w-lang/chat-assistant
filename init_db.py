import sqlite3

conn = sqlite3.connect('service.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  email TEXT,
  phone TEXT,
  created_at TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS questions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  question TEXT,
  answer TEXT,
  created_at TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS ratings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  rating INTEGER,
  created_at TEXT
)
''')

conn.commit()
conn.close()
