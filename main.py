import web_read
import db_init
import db_insert
import db_analysis
import WebFetch as fetch
import web_processor
import dot_gv as gv
import db_tree as tree
import output_text as texts
import degree
import people

def db_initing():
    print "** db_initing **"
    db_init.init()
    print "** db_initing finish **"
    #db_insert.test()

def web_reading():
    print "** web_reading **"
    #web_read.test()
    index_start = 19300
    index_end = 19316 # it can be finded by visiting this site: http://www.thingiverse.com/newest
    #web_read.page_loop(index_start, index_end)
    web_read.page_loop_threads(index_start, index_end)
    #web_read.page_read(7)
    #web_read.page_read(17773)
    print "** web_reading finish **"

def web_reading_threads():
    fetch.fetch_multi_once_thread_pool(200, 100, 100, web_read.content_scripting, web_processor.page_processing)
    #for index in range(20):
    #    start = index*10
    #    end = (index+1)*10
    #    links = ['http://www.thingiverse.com/thing:%d' %i for i in range (start, end)]
    #    fetch.fetchio_multi(links, 5, web_read.content_scripting, web_processor.page_processing)
    #    print " === finish %d to %d ==="%(start, end)
        
    #links = ['http://www.thingiverse.com/thing:%d' %i for i in range (1, 20000)]
    #fetch.fetchio_multi(links, 50, web_read.content_scripting, web_processor.page_processing)
    

def db_analysising():
    db_analysis.test()

def db_gving():
    #gv.test()
    gv.derived_x_to_y()

def db_tree():
    #tree.test()
    #tree.get_tree()
    child_list = tree.get_things_with_multiple_parents()
    tree_list = tree.get_tree()
    print len(tree_list)
    tl = []
    for t in tree_list:
        if t not in tl:
            tl.append(t)
    print len(tl)
    parent_list = tree.get_thing_with_multi_parents_root_list(tree_list, child_list)
    tree_clean = tree.get_tree_individual(tree_list, parent_list)
    tree.tree_write(tree_clean)
    tree.thing_check()
    
def output_text():
    texts.text_things()


def get_degree():
    degree.get_degree()

def get_people():
    people.thing_people()


if __name__ == "__main__":
    print "** main start **"
    #db_initing()
    #web_reading()
    #web_reading_threads()
    #db_analysising()
    #db_gving()
    db_tree()
    #output_text()
    #get_degree()
    #get_people()
