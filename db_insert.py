from myutil import conn, http
from BeautifulSoup import Tag, NavigableString, BeautifulSoup
import re
import sys

def test():
    sql = ''' SELECT * FROM SQLITE_MASTER'''
    c = conn.cursor()
    c.execute(sql)
    for r in c.fetchall():
        print r


def people_check(url):
    sql_id = 'SELECT id FROM people WHERE url=?'
    c = conn.cursor()
    c.execute(sql_id, (url,))
    people_id = c.fetchone()
    #print "***", people_id
    #print "***", people_id[0]
    if people_id:
        return people_id[0]
    else:
        name = ''
        register_time = ''
        response, content = http.request(url, 'GET')
        if int(response['status']) == 200:
            soup = BeautifulSoup(content)
            lists = soup.findAll('div', attrs={'id':'user-meta'})
            if lists:
                #print lists[0].contents
                name = lists[0].contents[1].contents[0]
                #print name
                #print lists[0].contents[3].contents
                #print "======"
                for l in lists[0].contents[3].contents:
                    if type(l) == Tag:
                        for r in l.contents:
                            if type(r) == Tag:
                                #print r.contents
                                temp = r.contents[0].strip('\n\t')
                                #print temp
                                t = re.findall('Registered on', temp)
                                if t:
                                    register_time = temp.strip('Registered on')
                                    #print register_time
                                    break
                                #tag_number = tag_number.strip('()')
                                #print t
                                #print "****"
                        #print "======"
        else:
            print "user's profile is not existing:"+url
        sql = 'INSERT INTO people (name, url, register_time) VALUES (?, ?, ?)'
        param = (name, url, register_time, )
        #print param
        c.execute(sql, param)
        conn.commit()
        c.execute(sql_id, (url,))
        people_id = c.fetchone()
        if people_id:
            return people_id[0]
    c.close()


def thing_insert(url, status, name, author_id, created_time):# default value for status is 1 which is in finished status
    sql_i = 'INSERT INTO thing (url, status, name, author_id, created_time) VALUES (?,?,?,?,?)'
    param = (url, status, name, author_id, created_time, )
    #print param
    c = conn.cursor()
    c.execute(sql_i, param)
    conn.commit()
    sql = 'SELECT id FROM thing WHERE url=?'
    param = (url, )
    c.execute(sql, param)
    thing_id = c.fetchone()
    if thing_id:
        return thing_id[0]
    c.close()

def description_insert(thing_id, description):
    sql_i = 'INSERT INTO description (thing_id, description) VALUES (?,?)'
    param = (thing_id, description, )
    #print param
    c = conn.cursor()
    c.execute(sql_i, param)
    conn.commit()
    c.close()

def instruction_insert(thing_id, instruction):
    sql_i = 'INSERT INTO instruction (thing_id, instruction) VALUES (?,?)'
    param = (thing_id, instruction, )
    #print param
    c = conn.cursor()
    c.execute(sql_i, param)
    conn.commit()
    c.close()
    
def image_insert(thing_id, image_url, image_type):
    sql_i = 'INSERT INTO gallery_image (thing_id, url, type) VALUES (?,?,?)'
    param = (thing_id, image_url, image_type, )
    #print param
    c = conn.cursor()
    c.execute(sql_i, param)
    conn.commit()
    c.close()

def file_insert(thing_id, file_type, file_url, file_date, file_name, file_download):
    sql_i = 'INSERT OR IGNORE INTO file_type (type) VALUES (?)'
    c = conn.cursor()
    param = (file_type, )
    #print param
    c.execute(sql_i, param)
    conn.commit()
    sql_i = 'SELECT id FROM file_type WHERE type=?'
    param = (file_type, )
    c.execute(sql_i, param)
    type_id = c.fetchone()[0]
    if type_id:
        sql_i = 'INSERT INTO file (thing_id, date, type_id, download_count, url, name) VALUES (?, ?, ?, ?, ?, ?)'
        param = (thing_id, file_date, type_id, file_download, file_url, file_name, )
        #print param
        c.execute(sql_i, param)
        conn.commit()
    else:
        sys.error('file type is not correct in database')
    c.close()

def tag_insert(thing_id, tag_name):
    sql_i = 'INSERT OR IGNORE INTO tag (name) VALUES (?)'
    c = conn.cursor()
    param = (tag_name, )
    c.execute(sql_i, param)
    conn.commit()
    sql_i = 'SELECT id FROM tag WHERE name = ?'
    param = (tag_name, )
    c.execute(sql_i, param)
    tag_id = c.fetchone()[0]
    if tag_id:
        sql_i = 'INSERT INTO thing_tag (thing_id, tag_id) VALUES (?, ?)'
        param = (thing_id, tag_id, )
        print param
        c.execute(sql_i, param)
        conn.commit()
    else:
        sys.error('tag is not exisitng in database file')
    c.close()

def like_insert(thing_id, follower_id):
    sql_i = 'INSERT INTO like (thing_id, follower_id) VALUES (?, ?)'
    c = conn.cursor()
    param = (thing_id, follower_id,)
    print param
    c.execute(sql_i, param)
    conn.commit()
    c.close()

def license_insert(thing_id, license_url):
    sql_i = 'INSERT OR IGNORE INTO license (url) VALUES (?)'
    c = conn.cursor()
    param = (license_url, )
    c.execute(sql_i, param)
    conn.commit()
    sql_i = 'SELECT id FROM license WHERE url = ?'
    param = (license_url, )
    c.execute(sql_i, param)
    license_id = c.fetchone()[0]
    if license_id:
        sql_i = 'INSERT INTO thing_license (thing_id, license_id) VALUES (?,?)'
        param = (thing_id, license_id, )
        print param
        c.execute(sql_i, param)
        conn.commit()
    else:
        sys.error('license error in database')
    c.close()

def derived_insert(thing_id, derived_url):
    sql_i = 'INSERT INTO derived (thing_id, url) VALUES (?, ?)'
    c = conn.cursor()
    param = (thing_id, derived_url,)
    c.execute(sql_i, param)
    conn.commit()
    c.close()

def made_insert(thing_id, made_url):
    response, content = http.request(made_url, 'GET')
    if int(response['status']) == 200:
        soup = BeautifulSoup(content)
        lists = soup.findAll('div', attrs={'class':'byline'})
        #print lists[0].contents
        made_time = lists[0].contents[1].contents[2].strip('onby')
        made_time = made_time.strip()
        #print made_time
        made_author = lists[0].contents[3]['href']
        made_author_id = people_check(made_author)
        #print made_author
        sql_i = 'INSERT INTO made (thing_id, url, made_time, made_author_id) VALUES (?,?,?,?)'
        c = conn.cursor()
        param = (thing_id, made_url, made_time, made_author_id, )
        print param
        c.execute(sql_i, param)
        conn.commit()
        print "*******"
        c.close()
    

    
