from myutil import conn, http
from BeautifulSoup import Tag, NavigableString, BeautifulSoup
import re

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
                                print "****"
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


def thing_insert(url, status, name, author_id, created_time):# default value for status is 1 which is in finished status
    sql_i = 'INSERT INTO thing (url, status, name, author_id, created_time) VALUES (?,?,?,?,?)'
    param = (url, status, name, author_id, created_time, )
    print param
    c = conn.cursor()
    c.execute(sql_i, param)
    conn.commit()
    sql = 'SELECT id FROM thing WHERE url=?'
    param = (url, )
    c.execute(sql, param)
    thing_id = c.fetchone()
    if thing_id:
        return thing_id[0]

def description_insert(thing_id, description):
    sql_i = 'INSERT INTO description (thing_id, description) VALUES (?,?)'
    param = (thing_id, description, )
    print param
    c = conn.cursor()
    c.execute(sql_i, param)
    conn.commit()
    
