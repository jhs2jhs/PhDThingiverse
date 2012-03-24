from myutil import conn, http, page_url_root
from myutil import page_dict_label as pdl
import socks
import urllib
import re
from BeautifulSoup import Tag, NavigableString, BeautifulSoup
import db_insert
import Queue
import threading
import httplib2
import WebFetch as fetch

http = httplib2.Http()


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

def s_base_error(soup, index, page_dict):
    lists = soup.findAll('div', attrs={'class':'BaseError'})
    if lists:
        # there is a base error, one example is: http://www.thingiverse.com/thing:5183
        page_dict[pdl.thing_error] = 0
        print "*** base error on thing: :"+str(index)
    else:
        page_dict[pdl.thing_error] = 1

def s_work_in_progress(soup, page_dict):
    lists = soup.findAll("div", attrs={'class':'BaseStatus'})
    if lists:
        #print "working in progress"
        #print lists
        #return 0 # working n progress
        page_dict[pdl.thing_status] = 0
    else:
        #return 1 # finished
        page_dict[pdl.thing_status] = 1

def s_thing_meta(soup, page_dict):
    lists = soup.findAll('div', attrs={'id':'thing-meta'})
    #print len(lists)
    if lists:
        #author_url = lists[0].contents[3].contents[1].contents[1].contents[1].contents[1]['href']#author name
        author_url = lists[0].contents[3].contents[1].contents[1].contents[1].contents
        #print type(author_url)
        #print author_url
        if len(author_url) == 3:# if no thumb image availble next to cretator name
            author_url = lists[0].contents[3].contents[1].contents[1].contents[1].contents[1].contents[3]['href']
            #print "777777777"
            #print author_url
        else:
            author_url = lists[0].contents[3].contents[1].contents[1].contents[1].contents[1]['href']
            #print "88888"
            #print author_url
        #print "lllllllllll"
        page_dict[pdl.author_url] = author_url
        thing_name = lists[0].contents[1].contents[0]#thing name
        thing_name = unicode(thing_name)
        page_dict[pdl.thing_name] = thing_name
        created_time = lists[0].contents[3].contents[1].contents[3].contents[0]
        #print created_time
        #sys.exit()
        created_time = created_time.strip("\n\tCreated on")
        page_dict[pdl.thing_created_time] = created_time
        description = lists[0].contents[5]
        description = unicode(description)
        page_dict[pdl.description] = description
        #return page_dict



    
def s_gallery_images(soup, page_dict):
    images = []
    lists = soup.findAll('div', attrs={'id':'thing-gallery'})
    #print len(lists)
    lists = soup.findAll('div', attrs={'id':'thing-gallery-main'})
    #print len(lists), lists[0].contents[1]['href']
    # main image link
    image_main = lists[0].contents[1]['href']
    images.append({
            pdl.thing_image_url:image_main,
            pdl.thing_image_type:0
            })
    lists = soup.findAll('div', attrs={'id':'thing-gallery-thumbs'})
    if lists:
        i = 0
        for l in lists[0].contents:
            if isinstance(l, Tag):
                i = i+1
                #print l.contents[1]['href']
                # all the image link
                image_sub = l.contents[1]['href']
                images.append({
                        pdl.thing_image_url:image_sub,
                        pdl.thing_image_type:1
                        })
    page_dict[pdl.thing_images] = images
    

def s_thing_widget(soup, page_dict):# more example would come back later
    lists = soup.findAll('div', attrs={'id':'facebook_share_button'})
    print len(lists)
    url_widget = lists[0].contents[1]['src']
    response, content = fetch.fetchio_single(url_widget)
    if True:
        #print content
        soup_widget = BeautifulSoup(content)
        lists_widget = soup_widget.findAll('div', attrs={'class':'connect_widget_button_count_count'})
        widget_count = lists_widget[1].contents[0]
        print widget_count
    
'''def s_thing_files(soup):
    lists = soup.findAll('div', attrs={'id':'thing-files'})
    #print len(lists)
    if lists:
        #i = 0
        files = []
        for l in lists[0].contents:
            if type(l) == Tag:
                #i = i + 1
                #print '***********'
                #print i, l
                print l
                print l['id']
                print l['data-adddate']
                file_date = l['data-adddate']
                #page_dict[pdl.file_date] = file_date #
                file_type = l['data-filetype']
                #page_dict[pdl.file_type] = file_type #
                file_download = l['data-dlcount']
                file_download = int(file_download)
                #page_dict[pdl.file_download] = file_download #
                file_url = l.contents[3].contents[1]['href']
                #page_dict[pdl.file_url] = file_href #
                file_name = l.contents[3].contents[1]['title']
                #page_dict[pdl.file_name] = file_name #
                files.append({
                        pdl.file_name:file_name,
                        pdl.file_type:file_type,
                        pdl.file_date:file_date,
                        pdl.file_download:file_download,
                        pdl.file_url:file_url
                        })
        page_dict[pdl.thing_files] = files
'''
def s_thing_files(soup, page_dict):
    lists = soup.findAll('div', attrs={'class':'thing-file'})
    #print len(lists)
    if lists:
        #i = 0
        files = []
        for l in lists:
            #print l
            if type(l) == Tag:
                #i = i + 1
                #print '***********'
                #print i, l
                #print l.contents
                #print l['id']
                #print l['data-adddate']
                file_date = l['data-adddate']
                #page_dict[pdl.file_date] = file_date #
                file_type = l['data-filetype']
                #page_dict[pdl.file_type] = file_type #
                file_download = l['data-dlcount']
                file_download = int(file_download)
                #page_dict[pdl.file_download] = file_download #
                #print l.contents[3].contents[1]['href']
                file_url = l.contents[3].contents[1]['href']
                #page_dict[pdl.file_url] = file_href #
                file_name = l.contents[3].contents[1]['title']
                #page_dict[pdl.file_name] = file_name #
                files.append({
                        pdl.file_name:file_name,
                        pdl.file_type:file_type,
                        pdl.file_date:file_date,
                        pdl.file_download:file_download,
                        pdl.file_url:file_url
                        })
        page_dict[pdl.thing_files] = files
        #print files
        


def s_thing_instruction(soup, page_dict):
    lists = soup.findAll('div', attrs={'id':'thing-instructions'})
    #print len(lists)
    if lists:
        instruments = lists[0]
        instruments = unicode(instruments)
        page_dict[pdl.instruction] = instruments
    #print instruments
    
def s_comments(soup, index, page_dict):
    #lists = soup.findAll('div', attrs={'id':'thing-comments'})
    #print len(lists)
    #print lists
    #http://js-kit.com/comments-data.js?ref=http%3A%2F%2Fwww.thingiverse.com%2Fthing%3A17773&p[0]=%2Fthing%3A17773&permalink[0]=http%3A%2F%2Fwww.thingiverse.com%2Fthing%3A17773
    #http://js-kit.com/comments-data.js?ref=http%3A%2F%2Fwww.thingiverse.com%2Fthing%3A17773&p[0]=%2Fthing%3A17773&permalink[0]=http%3A%2F%2Fwww.thingiverse.com%2Fthing%3A17773&jx[0]=0
    #http://js-kit.com/comments-data.js?ref=http%3A%2F%2Fwww.thingiverse.com%2Fthing%3A17773&p[0]=%2Fthing%3A17773&jx[0]=0
    #http://js-kit.com/comments-data.js?ref=http://www.thingiverse.com/thing:17773&p[0]=/thing:17773&jx[0]=0
    url = 'http://js-kit.com/comments-data.js?ref=http://www.thingiverse.com/thing:'+str(index)+'&p[0]=/thing:'+str(index)+'&jx[0]=0'
    print url
    response, content = fetch.fetchio_single(url)
    print response
    print content
    if int(response['status']) == 200:
        print content

def s_thing_tags(soup, page_dict):
    lists = soup.findAll('li', attrs={'class':'tag_display'})
    #print len(lists)
    if lists:
        tags = []
        for l in lists:
            if type(l) == Tag:
                tag_name = l.contents[0]['href']
                #print tag_name
                #tag_number = l.contents[0].contents[0]
                #tag_number = re.findall('\(\d+\)', tag_number)[0]# the number here may not exist, see thing:13661
                #tag_number = tag_number.strip('()')
                #tag_number = tag_number.strip(')')
                #print tag_number
                tags.append({
                        pdl.tag_name:tag_name
                        })
        page_dict[pdl.thing_tags] = tags

def s_made_one(soup, page_dict):
    #lists = soup.findAll('form', attrs={'id':'i_made_one_form'})
    lists = soup.findAll('div', attrs={'id':'thing-made'})
    #print len(lists)
    #print lists
    if lists:
        mades = []
        deriveds = []
        for l in lists:
            if l.contents[1].contents[0] == "Who's Made It?":
                lists_made = l.contents[3].contents
                for lm in lists_made:
                    if type(lm) == Tag:
                        #print lm
                        made_href = lm.contents[1]['href']
                        mades.append({pdl.made_url:made_href})
                        #print made_href
                        #print "**********"
            if l.contents[1].contents[0] == "Who's Derived It?":
                lists_derived = l.contents[3].contents
                for lm in lists_derived:
                    if type(lm) == Tag:
                        #print lm
                        derived_href = lm.contents[1]['href']
                        deriveds.append({pdl.derived_url:derived_href})
                        #print derived_href
                        #print "***=========="
        page_dict[pdl.thing_mades] = mades
        page_dict[pdl.thing_deriveds] = deriveds
                        
                        
def s_like(soup, page_dict):
    lists = soup.findAll('div', attrs={'id':'thing-like'})
    #print lists[0].contents
    #print "============="
    if lists:
        likes = []
        for l in lists[0].contents:
            if type(l) == Tag and l:
                for ll in l:
                    if type(ll) == Tag:
                        follower_url = ll.contents[1]['href']
                        likes.append({
                                pdl.follower_url:follower_url
                                })
                        #print "******"
        page_dict[pdl.thing_likes] = likes

def s_license(soup, page_dict):
    lists = soup.findAll('div', attrs={'id':'thing-license'})
    if lists:
        if lists[0]:
            if lists[0].contents:
                if lists[0].contents[1]:
                    if lists[0].contents[1].has_key('rel'):
                        thing_license = lists[0].contents[1]['href']
                        page_dict[pdl.thing_license] = thing_license


def s_made(soup, page_dict):
    #lists = soup.findAll('form', attrs={'id':'i_made_one_form'})
    lists = soup.findAll('div', attrs={'id':'thing-made'})
    #print len(lists)
    #print lists
    if lists:
        mades = []
        deriveds = []
        for l in lists:
            if l.contents[1].contents[0] == "Who's Made It?":
                try:
                    if l.contents[5].contents[0]:
                        made_count = l.contents[5].contents[0].strip('\n\tView all copies')
                        #print l.contents[5].contents
                        #print made_count
                        made_count = int(made_count)
                        if made_count >= 20:
                            made_lists_url = l.contents[5]['href']
                            made_lists_url = page_url_root+made_lists_url
                            response, content = fetch.fetchio_single(made_lists_url)
                            soup_lists = BeautifulSoup(content)
                            page_lists = soup_lists.findAll('div', attrs={'class':'pagination'})
                            page_lists = page_lists[0].contents[1].contents
                            page_last = page_lists[len(page_lists)-2]
                            page_last = page_last.contents[0]['href'].strip()
                            page_last = re.findall('/page:\d+', page_last)
                            if page_last:
                                page_last = page_last[0].strip('/page:')
                                page_last = int(page_last)
                                #print page_last
                                page_first = 1
                                for page_url in range(page_first, page_last+1, 1):
                                    page_url = made_lists_url+"/page:"+str(page_url)
                                    print page_url
                                    response, content = fetch.fetchio_single(page_url)
                                    soup_made = BeautifulSoup(content)
                                    made_lists = soup_made.findAll('div', attrs={'class':'things'})
                                    if len(made_lists) == 0:
                                        #print "hello:::::::::::::::::::", made_lists
                                        continue
                                    for li in made_lists[0].contents:
                                        if type(li) == Tag:
                                            #print ".........."
                                            #print li.contents
                                            if not li.contents:
                                                #print '+++++++++++++++'
                                                break
                                            made_href = li.contents[1].contents[1]['href']
                                            #print made_href
                                            made_href = page_url_root+made_href
                                            mades.append({pdl.made_url:made_href})
                        else:
                            lists_made = l.contents[3].contents
                            for lm in lists_made:
                                if type(lm) == Tag:
                        #print lm
                                    made_href = lm.contents[1]['href']
                                    mades.append({pdl.made_url:made_href})
                        #print made_href
                        #print "**********"
                except Exception, what:
                    print what
                    continue
            if l.contents[1].contents[0] == "Who's Derived It?":
                try:
                    if l.contents[5].contents[0]:
                        derivation_count = l.contents[5].contents[0].strip('\n\tView all variations')
                        derivation_count = int(derivation_count)
                        if derivation_count >= 20:
                            #print derivation_count
                            derivation_lists_url = l.contents[5]['href']
                            #url_root = 'http://www.thingiverse.com'
                            derivation_lists_url = page_url_root+derivation_lists_url
                            response, content = fetch.fetchio_single(derivation_lists_url)
                            soup_lists = BeautifulSoup(content)
                            page_lists = soup_lists.findAll('div', attrs={'class':'pagination'})
                            page_lists = page_lists[0].contents[1].contents
                            page_last = page_lists[len(page_lists)-2]
                            page_last = page_last.contents[0]['href'].strip()
                            page_last = re.findall('/page:\d+', page_last)
                            if page_last:
                                page_last = page_last[0].strip('/page:')
                                page_last = int(page_last)
                                #print page_last
                                page_first = 1
                                for page_url in range(page_first, page_last+1, 1):
                                    page_url = derivation_lists_url+"/page:"+str(page_url)
                                    print page_url
                                    response, content = fetch.fetchio_single(page_url)
                                    if int(response['status']) != 200:
                                        print 'each derivation page is not available'
                                    soup_derived = BeautifulSoup(content)
                                    derived_lists = soup_derived.findAll('div', attrs={'class':'things'})
                                    if len(derived_lists) == 0:
                                        continue
                                    for li in derived_lists[0].contents:
                                        if type(li) == Tag:
                                            #print ".........."
                                            #print li
                                            if not li.contents:
                                                #print '+++++++++++++++'
                                                break
                                            derived_href = li.contents[1].contents[1]['href']
                                            #print derived_href
                                            deriveds.append({pdl.derived_url:derived_href})
                                            #print "*****************"
                                    #sys.exit()
                                    #print "finish"
                        else:
                            lists_derived = l.contents[3].contents
                            for lm in lists_derived:
                                if type(lm) == Tag:
                        #print lm
                                    derived_href = lm.contents[1]['href']
                                    deriveds.append({pdl.derived_url:derived_href})
                        #print derived_href
                        #print "***=========="
                except Exception, what:
                    print what
                    continue
        if len(mades) > 0:
            mades_author_urls = []
            for m in mades:
                made_url = m[pdl.made_url]
                response, content = fetch.fetchio_single(made_url)
                soup_made_author_url = BeautifulSoup(content)
                lists = soup_made_author_url.findAll('div', attrs={'class':'byline'})
                try:
                    made_time = lists[0].contents[1].contents[2].strip('onby')
                    made_time = made_time.strip()
                    made_author_url = lists[0].contents[3]['href']
                    mades_author_urls.append({pdl.made_url:made_url, pdl.made_time:made_time, pdl.made_author_url:made_author_url})
                except Exception, what:
                    print what
                    continue
            page_dict[pdl.thing_mades] = mades_author_urls
        if len(deriveds) > 0:
            page_dict[pdl.thing_deriveds] = deriveds



def content_scripting(content, req):
    index = req.strip('\n\thttp://www.thingiverse.com/thing:')
    index = int(index)
    soup = BeautifulSoup(content)
    pagedict = {}
    s_base_error(soup, index, pagedict)
    if pagedict[pdl.thing_error] == 0:
        return
    s_thing_meta(soup, pagedict)
    #print pagedict
    pagedict[pdl.thing_index] = index
    #print pagedict, "==="
    s_work_in_progress(soup, pagedict)
    s_gallery_images(soup, pagedict)
    s_thing_files(soup, pagedict)
    s_thing_instruction(soup, pagedict)
    s_thing_tags(soup, pagedict)
    s_made_one(soup, pagedict)
    s_like(soup, pagedict)
    s_license(soup, pagedict)
    s_made(soup, pagedict) #list has to passed into method, otherwise it will not recognised, and make the list massive. 
    #s_thing_widget(soup)#
    #s_comments(soup, index)#
    #print page_dict
    #print str(page_dict)
    print "**"+str(index)+"**"
    return pagedict
    #page_insert_derived(page_dict, index)
#################################


if __name__ == "__main__":
    page_loop_threads(1, 10)
    print "** web **"
