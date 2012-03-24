import db_insert
from myutil import page_dict_label as pdl

def page_insert_derived(pagedict, req):
    index = req.strip('\n\thttp://www.thingiverse.com/thing:')
    index = int(index)
    if pagedict.has_key(pdl.thing_mades):
        for m in pagedict[pdl.thing_mades]:
            y_url = m[pdl.made_url]
            x_url = '/thing:'+str(index)
            print (x_url, y_url), "==="
            db_insert.made_insert_new(x_url, y_url)
        #print "======== copy ==========="
    if pagedict.has_key(pdl.thing_deriveds):
        #print "***&&&&&&:"+str(len(page_dict[pdl.thing_deriveds]))
        for d in pagedict[pdl.thing_deriveds]:
            y_url = d[pdl.derived_url]
            x_url = '/thing:'+str(index)
            print (x_url, y_url)
            db_insert.derived_insert_new(x_url, y_url)
        #print "======== derived ==========="
