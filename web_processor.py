import db_insert
from myutil import page_dict_label as pdl

def page_processing(pagedict, req):
    if len(pagedict) == 0:
        return 
    index = req.strip('\n\thttp://www.thingiverse.com/thing:')
    index = int(index)
    if pagedict.has_key(pdl.author_url):
    #    author_id = db_insert.people_check(pagedict[pdl.author_url])
        author_url = pagedict[pdl.author_url]
    if pagedict.has_key(pdl.thing_name) and pagedict.has_key(pdl.thing_created_time) and pagedict.has_key(pdl.thing_index) and pagedict.has_key(pdl.thing_created_time):
        thing_url = "/thing:"+str(pagedict[pdl.thing_index])
        thing_status = pagedict.get(pdl.thing_status, 1)
        thing_name = pagedict[pdl.thing_name]
        thing_created_time = pagedict[pdl.thing_created_time]
        thing_id = db_insert.thing_insert(thing_url, thing_status, thing_name, author_url, thing_created_time)
    #print pagedict, req
    #print thing_url
    #print thing_id, "===================="
    if pagedict.has_key(pdl.description):
        description = pagedict[pdl.description]
        db_insert.description_insert(thing_id, description)
    if pagedict.has_key(pdl.instruction):
        instruction = pagedict[pdl.instruction]
        db_insert.instruction_insert(thing_id, instruction)
    if pagedict.has_key(pdl.thing_images):
        for image in pagedict[pdl.thing_images]:
            image_url = image[pdl.thing_image_url]
            image_type = image[pdl.thing_image_type]
            db_insert.image_insert(thing_id, image_url, image_type)
    if pagedict.has_key(pdl.thing_files):
        for f in pagedict[pdl.thing_files]:
            #print f
            file_type = f[pdl.file_type]
            file_name = f[pdl.file_name]
            file_date = f[pdl.file_date]
            file_url = f[pdl.file_url]
            file_download = f[pdl.file_download]
            db_insert.file_insert(thing_id, file_type, file_url, file_date, file_name, file_download)
    if pagedict.has_key(pdl.thing_tags):
        for t in pagedict[pdl.thing_tags]:
            tag_name = t[pdl.tag_name]
            db_insert.tag_insert(thing_id, tag_name)
    if pagedict.has_key(pdl.thing_likes):
        for l in pagedict[pdl.thing_likes]:
            follower_url = l[pdl.follower_url]
            #follower_id = db_insert.people_check(follower_url)
            db_insert.like_insert(thing_id, follower_url)
    if pagedict.has_key(pdl.thing_license):
        thing_license = pagedict[pdl.thing_license]
        db_insert.license_insert(thing_id, thing_license)
    if pagedict.has_key(pdl.thing_mades):
        for m in pagedict[pdl.thing_mades]:
            if m.has_key(pdl.made_time) and m.has_key(pdl.made_author_url) and m.has_key(pdl.made_url):
                continue
            made_time = m[pdl.made_time]
            made_author_url = m[pdl.made_author_url]
            y_url = m[pdl.made_url]
            x_url = '/thing:'+str(index)
            #print (x_url, y_url), "==="
            db_insert.made_insert(x_url, y_url, made_time, made_author_url)
        #print "======== copy ==========="
    if pagedict.has_key(pdl.thing_deriveds):
        #print "***&&&&&&:"+str(len(page_dict[pdl.thing_deriveds]))
        for d in pagedict[pdl.thing_deriveds]:
            y_url = d[pdl.derived_url]
            x_url = '/thing:'+str(index)
            #print (x_url, y_url)
            db_insert.derived_insert(x_url, y_url)
        #print "======== derived ==========="
    print "== finish %d =="%index
