import sqlite3

conn = sqlite3.connect('unanswered.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS unanswered (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    created_at TEXT NOT NULL
)
''')

conn.commit()
conn.close()
print('DB READY')
