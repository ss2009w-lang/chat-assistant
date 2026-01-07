import sqlite3

conn = sqlite3.connect('service.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS admins (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT,
  password TEXT,
  role TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS report_roles (
  role TEXT,
  category TEXT
)
''')

c.execute("INSERT OR IGNORE INTO admins (id,username,password,role) VALUES (1,'admin','admin123','super')")

c.execute("INSERT OR IGNORE INTO report_roles (role,category) VALUES ('tech','تقني')")
c.execute("INSERT OR IGNORE INTO report_roles (role,category) VALUES ('medical','طبي')")
c.execute("INSERT OR IGNORE INTO report_roles (role,category) VALUES ('admin','إداري')")

conn.commit()
conn.close()
