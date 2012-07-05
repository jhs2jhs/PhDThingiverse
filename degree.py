from myutil import conn
import re

sql_things = '''
SELECT thing.url
FROM thing
'''

sql_degree_in = '''
SELECT COUNT(derived_raw.x_url)
FROM derived_raw
WHERE derived_raw.y_url = '%s'
'''

sql_degree_out = '''
SELECT COUNT(derived_raw.y_url)
FROM derived_raw
WHERE derived_raw.x_url = '%s'
'''

#select * from derived_raw where derived_raw.x_url = '/thing:19896'

def get_degree():
    f = open("./texts/degree.txt", 'w')
    f.write('EXPLAIN: for a relationship A->B means B (child object) is derived from A (father object). in_degree means how many A could derive to a single B. Out_degree means how many B could be derived from a single A. If you look at object 19141 (http://www.thingiverse.com/thing:19141), the in_degree is 3 as it is derived from 3 objects, the out_degree is 2 as it derived to 2 objects. \n')
    f.write('thing_id \tthing_url \tin_degree \tout_degree\n')
    c = conn.cursor()
    c.execute(sql_things, ())
    for raw in c.fetchall():
        thing_url = raw[0]
        thing_id = thing_url.strip().replace('/thing:', '')
        # in
        c_in = conn.cursor()
        c_in.execute(sql_degree_in%(thing_url), ())
        degree_in = ''
        for raw_in in c_in:
            degree_in = str(raw_in[0])
        if degree_in == '':
            degree_in == '0'
        c_in.close()
        # out
        c_out = conn.cursor()
        c_out.execute(sql_degree_out%(thing_url), ())
        degree_out = ''
        for raw_out in c_out:
            degree_out = str(raw_out[0])
        if degree_out == '':
            degree_out == '0'
        c_out.close()
        f.write('%s\t%s\t%s\t%s\n'%(thing_id, thing_url, degree_in, degree_out))
        print thing_url, thing_id, degree_in, degree_out
    c.close()
    f.close()
    print "hello"
