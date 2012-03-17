import httplib2
http = httplib2.Http()

import sqlite3
sqlite_file_path = './db/thingiver.db'
conn = sqlite3.connect(sqlite_file_path)
