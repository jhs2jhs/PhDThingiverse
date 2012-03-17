from myutil import conn, http
import socks
import urllib
import re
from BeautifulSoup import Tag, NavigableString, BeautifulSoup
import db_insert


def test():
    print "web read test"
    url = 'http://www.thingiverse.com/login'
    body = {'username':'jianhuashao', 'password':'jianhuashao'}
    headers = {'content-type':'application/x-www-form-urlencoded'}
    response, content = http.request(url, 'POST', headers = headers, body = urllib.urlencode(body))
    headers = {'Cookie': response['set-cookie']}
    #print content
    url = 'http://www.thingiverse.com/thing:18017'
    response, content = http.request(url, 'GET', headers = headers)
    response, content = http.request(url, 'GET')
    print response
    #print content

def page_insert(page_dict):
    if page_dict['author_url'] == 1:
        author_id = db_insert.people_check(page_dict['author_url'])
    print author_id, "}}}}}}"
        
    


def s_work_in_progress(soup):
    lists = soup.findAll("div", attrs={'class':'BaseStatus'})
    if lists:
        #print "working in progress"
        #print lists
        return 0 # working n progress
    else:
        return 1 # finished

def s_thing_meta(soup, page_dict):
    lists = soup.findAll('div', attrs={'id':'thing-meta'})
    #print len(lists)
    if lists:
        author_url = lists[0].contents[3].contents[1].contents[1].contents[1].contents[1]['href']#author name
        page_dict['author_url'] = author_url
        #author_id = db_insert.people_check(author_url)
        #author_id = db_insert.people_check('http://www.thingiverse.com/Mjolnir')
        #print "author_id:", author_id
        #print lists[0].contents
        thing_name = lists[0].contents[1].contents[0]#thing name
        page_dict['thing_name'] = thing_name
        #print thing_name
        created_time = lists[0].contents[3].contents[1].contents[3].contents[0]
        created_time = created_time.strip("\n\tCreated on")
        #created_time = created_time.strip("\t")
        status = s_work_in_progress(soup)
        url = "http://www.thingiverse.com/thing:"#+str(index)
        author_id = 1
        thing_id = db_insert.thing_insert(url, status, thing_name, author_id, created_time)
        #print thing_id
        description = lists[0].contents[5]
        #print type(description), "****"
        db_insert.description_insert(thing_id, str(description))
        return page_dict



    
def s_gallery_images(soup):
    lists = soup.findAll('div', attrs={'id':'thing-gallery'})
    print len(lists)
    lists = soup.findAll('div', attrs={'id':'thing-gallery-main'})
    print len(lists), lists[0].contents[1]['href']
    # main image link
    lists = soup.findAll('div', attrs={'id':'thing-gallery-thumbs'})
    if lists:
        i = 0
        for l in lists[0].contents:
            if isinstance(l, Tag):
                i = i+1
                print l.contents[1]['href']
                # all the image link
    

def s_thing_widget(soup):# more example would come back later
    lists = soup.findAll('div', attrs={'id':'facebook_share_button'})
    print len(lists)
    url_widget = lists[0].contents[1]['src']
    response, content = http.request(url_widget, 'GET')
    if int(response['status']) == 200:
        #print content
        soup_widget = BeautifulSoup(content)
        lists_widget = soup_widget.findAll('div', attrs={'class':'connect_widget_button_count_count'})
        widget_count = lists_widget[1].contents[0]
        print widget_count
    
def s_thing_files(soup):
    lists = soup.findAll('div', attrs={'id':'thing-files'})
    print len(lists)
    if lists:
        i = 0
        for l in lists[0].contents:
            if type(l) == Tag:
                i = i + 1
                print '***********'
                #print i, l
                file_date = l['data-adddate']
                print file_date
                file_type = l['data-filetype']
                print file_type
                file_download = l['data-dlcount']
                print file_download
                file_href = l.contents[3].contents[1]['href']
                print file_href
                file_name = l.contents[3].contents[1]['title']
                print file_name

def s_thing_instruction(soup):
    lists = soup.findAll('div', attrs={'id':'thing-instructions'})
    print len(lists)
    instruments = lists[0]
    #print instruments
    
def s_comments(soup):
    lists = soup.findAll('div', attrs={'id':'thing-comments'})
    print len(lists)
    print lists
    #http://js-kit.com/comments-data.js?ref=http%3A%2F%2Fwww.thingiverse.com%2Fthing%3A17773&p[0]=%2Fthing%3A17773&permalink[0]=http%3A%2F%2Fwww.thingiverse.com%2Fthing%3A17773
    #http://js-kit.com/comments-data.js?ref=http%3A%2F%2Fwww.thingiverse.com%2Fthing%3A17773&p[0]=%2Fthing%3A17773&permalink[0]=http%3A%2F%2Fwww.thingiverse.com%2Fthing%3A17773&jx[0]=0
    #http://js-kit.com/comments-data.js?ref=http%3A%2F%2Fwww.thingiverse.com%2Fthing%3A17773&p[0]=%2Fthing%3A17773&jx[0]=0
    #http://js-kit.com/comments-data.js?ref=http://www.thingiverse.com/thing:17773&p[0]=/thing:17773&jx[0]=0

def s_thing_tags(soup):
    lists = soup.findAll('li', attrs={'class':'tag_display'})
    print len(lists)
    if lists:
        for l in lists:
            if type(l) == Tag:
                tag_name = l.contents[0]['href']
                print tag_name
                tag_number = l.contents[0].contents[0]
                tag_number = re.findall('\(\d+\)', tag_number)[0]
                tag_number = tag_number.strip('()')
                #tag_number = tag_number.strip(')')
                print tag_number

def s_made_one(soup):
    #lists = soup.findAll('form', attrs={'id':'i_made_one_form'})
    lists = soup.findAll('div', attrs={'id':'thing-made'})
    print len(lists)
    #print lists
    if lists:
        for l in lists:
            if l.contents[1].contents[0] == "Who's Made It?":
                lists_made = l.contents[3].contents
                for lm in lists_made:
                    if type(lm) == Tag:
                        #print lm
                        made_href = lm.contents[1]['href']
                        print made_href
                        print "**********"
            if l.contents[1].contents[0] == "Who's Derived It?":
                lists_derived = l.contents[3].contents
                for lm in lists_derived:
                    if type(lm) == Tag:
                        derived_href = lm.contents1[1]['href']
                        print derived_href
                        print "********"
                        
                        
def s_like(soup):
    lists = soup.findAll('div', attrs={'id':'thing-like'})
    #print lists[0].contents
    print "============="
    if lists:
        for l in lists[0].contents:
            if type(l) == Tag and l:
                for ll in l:
                    if type(ll) == Tag:
                        print ll.contents[1]['href']
                        print "******"

def s_license(soup):
    lists = soup.findAll('div', attrs={'id':'thing-license'})
    if lists[0]:
        print lists[0].contents[1]['href']

def content_script(content, index):
    soup = BeautifulSoup(content)
    page_dict = {'page':'thingivers'}
    page_dict = s_thing_meta(soup, page_dict)
    #s_work_in_progress(soup)
    #s_gallery_images(soup)
    #s_thing_widget(soup)
    #s_thing_files(soup)
    #s_thing_instruction(soup)
    #s_comments(soup)
    #s_thing_tags(soup)
    #s_made_one(soup)
    #s_like(soup)
    #s_license(soup)
    page_insert(page_dict)

def page_read(index):
    url_root = 'http://www.thingiverse.com/thing:'
    url = url_root+str(index)
    response, content = http.request(url, 'GET')
    if int(response['status']) != 200:
        print "**** status error when reading page: "+status
    content_script(content, index)

def page_loop():
    index_start = 0
    index_end = 19183 # it can be finded by visiting this site: http://www.thingiverse.com/newest
    for i in range(index_start, index_end+1, 1): 
        page_read(i)
    print "finish loop page reading"
        


if __name__ == "__main__":
    print "**web **"
