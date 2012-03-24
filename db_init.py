#!/usr/bin/python
from myutil import conn

sql = '''
CREATE TABLE IF NOT EXISTS error (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  url TEXT,
  error TEXT
);
CREATE TABLE IF NOT EXISTS people (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  name TEXT, 
  url TEXT UNIQUE NOT NULL,
  register_time TEXT
);
CREATE TABLE IF NOT EXISTS thing (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  url TEXT UNIQUE NOT NULL,
  status INTEGER NOT NULL DEFAULT 1, -- 1 is finished, 0 is working in progress
  name TEXT, 
  author_id INTEGER NOT NULL,
  created_time TEXT,
  FOREIGN KEY (author_id) REFERENCES people(id)
);
CREATE TABLE IF NOT EXISTS description (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  thing_id INTEGER NOT NULL,
  description TEXT,
  FOREIGN KEY (thing_id) REFERENCES thing(id)
);
CREATE TABLE IF NOT EXISTS instruction (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  thing_id INTEGER NOT NULL,
  instruction TEXT,
  FOREIGN KEY (thing_id) REFERENCES thing(id)
);
CREATE TABLE IF NOT EXISTS gallery_image (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  thing_id INTEGER NOT NULL,
  url TEXT NOT NULL,
  type INTEGER NOT NULL DEFAULT 1, -- 1 is sub thumbinal, 0 is main image in the windows
  FOREIGN KEY (thing_id) REFERENCES thing(id)
);
-- WIDGET IS NOT SET UP HERE 
---
---
CREATE TABLE IF NOT EXISTS file_type (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  type TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS file (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  thing_id INTEGER NOT NULL,
  date TEXT,
  type_id INTEGER NOT NULL,
  download_count INTEGER,
  url TEXT,
  name TEXT,
  FOREIGN KEY (thing_id) REFERENCES thing(id),
  FOREIGN KEY (type_id) REFERENCES file_type(id)
);
CREATE TABLE IF NOT EXISTS tag (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS thing_tag (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  thing_id INTEGER NOT NULL,
  tag_id INTGER NOT NULL,
  FOREIGN KEY (thing_id) REFERENCES thing(id),
  FOREIGN KEY (tag_id) REFERENCES tag(id),
  UNIQUE (thing_id, tag_id)
);
CREATE TABLE IF NOT EXISTS made (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  thing_id INTEGER NOT NULL,
  url TEXT,
  made_time TEXT,
  made_author_id INTEGER NOT NULL,
  FOREIGN KEY (thing_id) REFERENCES thing(id),
  FOREIGN KEY (made_author_id) REFERENCES people(id)
);
CREATE TABLE IF NOT EXISTS derived (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  thing_id INTEGER NOT NULL,
  url TEXT,
  FOREIGN KEY (thing_id) REFERENCES thing(id)
);
------------------update ---------
CREATE TABLE IF NOT EXISTS made_raw (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  x_url TEXT,
  y_url TEXT,
  made_time TEXT,
  made_author_id INTEGER NOT NULL,
  FOREIGN KEY (made_author_id) REFERENCES people(id),
  UNIQUE(x_url, y_url)
);
CREATE TABLE IF NOT EXISTS derived_raw (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  x_url TEXT,
  y_url TEXT,
  UNIQUE (x_url, y_url)
);
----------------update--------------
CREATE TABLE IF NOT EXISTS like (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  thing_id INTEGER NOT NULL,
  follower_id INTEGER NOT NULL,
  FOREIGN KEY (thing_id) REFERENCES thing(id),
  FOREIGN KEY (follower_id) REFERENCES people(id),
  UNIQUE (thing_id, follower_id)
);
CREATE TABLE IF NOT EXISTS license (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  url TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS thing_license (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  thing_id INTEGER NOT NULL,
  license_id INTEGER NOT NULL,
  FOREIGN KEY (thing_id) REFERENCES thing(id),
  FOREIGN KEY (license_id) REFERENCES license(id),
  UNIQUE (thing_id, license_id)
);
'''

def init():
    c = conn.cursor()
    c.executescript(sql)
    conn.commit()
    c.execute('''SELECT * FROM SQLITE_MASTER ''')
    tables = c.fetchall()
    print "** tables total number:"+str(len(tables))
    c.close()
