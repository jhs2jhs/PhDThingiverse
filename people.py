from myutil import conn
import re

sql_things = '''
SELECT thing.url, thing.author_url, thing.created_time
FROM thing
'''

def thing_people():
    f = open("./texts/people.txt", 'w')
    f.write('thing_id \tthing_url \tauthor_name \tthing_created_time \tthing_author_url\n')
    c = conn.cursor()
    c.execute(sql_things, ())
    for raw in c.fetchall():
        thing_url = raw[0]
        thing_id = thing_url.strip().replace('/thing:', '')
        thing_author_url = raw[1]
        thing_author = thing_author_url.strip().replace('http://www.thingiverse.com/', '')
        thing_time = raw[2]
        f.write('%s\t%s\t%s\t%s\t%s\n'%(thing_id, thing_url, thing_author, thing_time, thing_author_url))
        print thing_id, thing_url, thing_author, thing_time, thing_author_url
    c.close()
    f.close()
