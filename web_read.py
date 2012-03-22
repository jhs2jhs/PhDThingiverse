from myutil import conn, http, page_url_root
from myutil import page_dict_label as pdl
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

page_dict = {}

def page_insert(page_dict):
    #print page_dict
    if page_dict.has_key(pdl.author_url):
        author_id = db_insert.people_check(page_dict[pdl.author_url])
    #if page_dict[pdl.thing_status]:
    #    thing_status = page_dict[pdl.thing_status]
    if page_dict.has_key(pdl.thing_name) and page_dict.has_key(pdl.thing_created_time) and page_dict.has_key(pdl.thing_index) and page_dict.has_key(pdl.thing_created_time):
        thing_url = "/thing:"+str(page_dict[pdl.thing_index])
        thing_status = page_dict.get(pdl.thing_status, 1)
        thing_name = page_dict[pdl.thing_name]
        thing_created_time = page_dict[pdl.thing_created_time]
        thing_id = db_insert.thing_insert(thing_url, thing_status, thing_name, author_id, thing_created_time)
    if page_dict.has_key(pdl.description):
        description = page_dict[pdl.description]
        db_insert.description_insert(thing_id, description)
    if page_dict.has_key(pdl.instruction):
        instruction = page_dict[pdl.instruction]
        db_insert.instruction_insert(thing_id, instruction)
    if page_dict.has_key(pdl.thing_images):
        for image in page_dict[pdl.thing_images]:
            image_url = image[pdl.thing_image_url]
            image_type = image[pdl.thing_image_type]
            db_insert.image_insert(thing_id, image_url, image_type)
    if page_dict.has_key(pdl.thing_files):
        for f in page_dict[pdl.thing_files]:
            #print f
            file_type = f[pdl.file_type]
            file_name = f[pdl.file_name]
            file_date = f[pdl.file_date]
            file_url = f[pdl.file_url]
            file_download = f[pdl.file_download]
            db_insert.file_insert(thing_id, file_type, file_url, file_date, file_name, file_download)
    if page_dict.has_key(pdl.thing_tags):
        for t in page_dict[pdl.thing_tags]:
            tag_name = t[pdl.tag_name]
            db_insert.tag_insert(thing_id, tag_name)
    if page_dict.has_key(pdl.thing_likes):
        for l in page_dict[pdl.thing_likes]:
            follower_url = l[pdl.follower_url]
            follower_id = db_insert.people_check(follower_url)
            db_insert.like_insert(thing_id, follower_id)
    if page_dict.has_key(pdl.thing_license):
        thing_license = page_dict[pdl.thing_license]
        db_insert.license_insert(thing_id, thing_license)
    if page_dict.has_key(pdl.thing_deriveds):
        for d in page_dict[pdl.thing_deriveds]:
            derived_url = d[pdl.derived_url]
            db_insert.derived_insert(thing_id, derived_url)
    if page_dict.has_key(pdl.thing_mades):
        for m in page_dict[pdl.thing_mades]:
            made_url = m[pdl.made_url]
            db_insert.made_insert(thing_id, made_url)
    #print "page_insert::::::::", thing_id
    page_dict = {}

def s_base_error(soup, index):
    lists = soup.findAll('div', attrs={'class':'BaseError'})
    if lists:
        # there is a base error, one example is: http://www.thingiverse.com/thing:5183
        page_dict[pdl.thing_error] = 0
        print "*** base error on thing: :"+str(index)
    else:
        page_dict[pdl.thing_error] = 1

def s_work_in_progress(soup):
    lists = soup.findAll("div", attrs={'class':'BaseStatus'})
    if lists:
        #print "working in progress"
        #print lists
        #return 0 # working n progress
        page_dict[pdl.thing_status] = 0
    else:
        #return 1 # finished
        page_dict[pdl.thing_status] = 1

def s_thing_creator(soup):
    lists = soup.findAll('div', attrs={'id':'thing-creator'})
    if lists:
        author_name = lists
        print author_name
        print "00000000000"

def s_thing_meta(soup):
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



    
def s_gallery_images(soup):
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
def s_thing_files(soup):
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
        


def s_thing_instruction(soup):
    lists = soup.findAll('div', attrs={'id':'thing-instructions'})
    #print len(lists)
    if lists:
        instruments = lists[0]
        instruments = unicode(instruments)
        page_dict[pdl.instruction] = instruments
    #print instruments
    
def s_comments(soup, index):
    #lists = soup.findAll('div', attrs={'id':'thing-comments'})
    #print len(lists)
    #print lists
    #http://js-kit.com/comments-data.js?ref=http%3A%2F%2Fwww.thingiverse.com%2Fthing%3A17773&p[0]=%2Fthing%3A17773&permalink[0]=http%3A%2F%2Fwww.thingiverse.com%2Fthing%3A17773
    #http://js-kit.com/comments-data.js?ref=http%3A%2F%2Fwww.thingiverse.com%2Fthing%3A17773&p[0]=%2Fthing%3A17773&permalink[0]=http%3A%2F%2Fwww.thingiverse.com%2Fthing%3A17773&jx[0]=0
    #http://js-kit.com/comments-data.js?ref=http%3A%2F%2Fwww.thingiverse.com%2Fthing%3A17773&p[0]=%2Fthing%3A17773&jx[0]=0
    #http://js-kit.com/comments-data.js?ref=http://www.thingiverse.com/thing:17773&p[0]=/thing:17773&jx[0]=0
    url = 'http://js-kit.com/comments-data.js?ref=http://www.thingiverse.com/thing:'+str(index)+'&p[0]=/thing:'+str(index)+'&jx[0]=0'
    print url
    response, content = http.request(url, 'GET')
    print response
    print content
    if int(response['status']) == 200:
        print content

def s_thing_tags(soup):
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

def s_made_one(soup):
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
                        
                        
def s_like(soup):
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

def s_license(soup):
    lists = soup.findAll('div', attrs={'id':'thing-license'})
    if lists:
        if lists[0]:
            if lists[0].contents:
                if lists[0].contents[1]:
                    if lists[0].contents[1].has_key('rel'):
                        thing_license = lists[0].contents[1]['href']
                        page_dict[pdl.thing_license] = thing_license


def content_script(content, index):
    soup = BeautifulSoup(content)
    print "** "+str(index)+" **"
    page_dict[pdl.thing_index]= index
    s_base_error(soup, index)
    if page_dict[pdl.thing_error] == 0:
        return
    #s_thing_creator(soup)
    s_thing_meta(soup)
    s_work_in_progress(soup)
    s_gallery_images(soup)
    s_thing_files(soup)
    s_thing_instruction(soup)
    s_thing_tags(soup)
    s_made_one(soup)
    s_like(soup)
    s_license(soup)
    #s_thing_widget(soup)#
    #s_comments(soup, index)#
    #print page_dict
    page_insert(page_dict)

################################
def s_made_derived_new(soup, page_dict):
    #lists = soup.findAll('form', attrs={'id':'i_made_one_form'})
    lists = soup.findAll('div', attrs={'id':'thing-made'})
    #print len(lists)
    #print lists
    if lists:
        mades = []
        deriveds = []
        for l in lists:
            if l.contents[1].contents[0] == "Who's Made It?":
                if l.contents[5]:
                    if l.contents[5].contents[0]:
                        made_count = l.contents[5].contents[0].strip('\n\tView all copies')
                        #print l.contents[5].contents
                        print made_count
                        made_count = int(made_count)
                        if made_count >= 20:
                            made_lists_url = l.contents[5]['href']
                            made_lists_url = page_url_root+made_lists_url
                            response, content = http.request(made_lists_url, 'GET')
                            if int(response['status']) != 200:
                                print '((((made lists not existing)))'+str()
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
                                    response, content = http.request(page_url, 'GET')
                                    if int(response['status']) != 200:
                                        print 'each made page is not available'
                                    soup_made = BeautifulSoup(content)
                                    made_lists = soup_made.findAll('div', attrs={'class':'things'})
                                    for li in made_lists[0].contents:
                                        if type(li) == Tag:
                                            #print ".........."
                                            #print li.contents
                                            if not li.contents:
                                                #print '+++++++++++++++'
                                                break
                                            made_href = li.contents[1].contents[1]['href']
                                            #print derived_href
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
            if l.contents[1].contents[0] == "Who's Derived It?":
                if l.contents[5]:
                    if l.contents[5].contents[0]:
                        derivation_count = l.contents[5].contents[0].strip('\n\tView all variations')
                        derivation_count = int(derivation_count)
                        if derivation_count >= 20:
                            #print derivation_count
                            derivation_lists_url = l.contents[5]['href']
                            #url_root = 'http://www.thingiverse.com'
                            derivation_lists_url = page_url_root+derivation_lists_url
                            response, content = http.request(derivation_lists_url, 'GET')
                            if int(response['status']) != 200:
                                print '((((derivation lists not exisitng)))'+str()
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
                                    response, content = http.request(page_url, 'GET')
                                    if int(response['status']) != 200:
                                        print 'each derivation page is not available'
                                    soup_derived = BeautifulSoup(content)
                                    derived_lists = soup_derived.findAll('div', attrs={'class':'things'})
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
        if len(mades) > 0:
            page_dict[pdl.thing_mades] = mades
        if len(deriveds) > 0:
            page_dict[pdl.thing_deriveds] = deriveds

def page_insert_derived(page_dict, index):
    if page_dict.has_key(pdl.thing_mades):
        for m in page_dict[pdl.thing_mades]:
            y_url = m[pdl.made_url]
            x_url = '/thing:'+str(index)
            print (x_url, y_url), "==="
            db_insert.made_insert_new(x_url, y_url)
        #print "======== copy ==========="
    if page_dict.has_key(pdl.thing_deriveds):
        #print "***&&&&&&:"+str(len(page_dict[pdl.thing_deriveds]))
        for d in page_dict[pdl.thing_deriveds]:
            y_url = d[pdl.derived_url]
            x_url = '/thing:'+str(index)
            print (x_url, y_url)
            #db_insert.derived_insert_new(x_url, y_url)
        #print "======== derived ==========="

def content_script_derived(content, index):
    soup = BeautifulSoup(content)
    print "**"+str(index)+"**"
    page_dict = {}
    s_made_derived_new(soup, page_dict) #list has to passed into method, otherwise it will not recognised, and make the list massive. 
    #print str(page_dict)
    page_insert_derived(page_dict, index)
#################################

def page_read(index):
    #url_root = 'http://www.thingiverse.com/thing:'
    url = page_url_root+'/thing:'+str(index)
    response, content = http.request(url, 'GET')
    if int(response['status']) != 200:
        print "**** status error when reading page: "+response['status']
        return 
    #content_script(content, index) # this is the normal command
    content_script_derived(content, index)

def page_loop(index_start, index_end):
    for i in range(index_start, index_end+1, 1): 
        page_read(i)
    print "finish loop page reading"
        


if __name__ == "__main__":
    print "** web **"
