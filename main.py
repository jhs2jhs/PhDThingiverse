import web_read
import db_init
import db_insert
import db_analysis
import WebFetch as fetch
import web_processor

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
    for index in range(20):
        start = 53#index*100
        end = 62#(index+1)*100
        links = ['http://www.thingiverse.com/thing:%d' %i for i in range (start, end)]
        fetch.fetchio_multi(links, 10, web_read.content_scripting, web_processor.page_processing)
        print " === finish %d to %d ==="%(start, end)
        
    #links = ['http://www.thingiverse.com/thing:%d' %i for i in range (1, 20000)]
    #fetch.fetchio_multi(links, 50, web_read.content_scripting, web_processor.page_processing)
    

def db_analysising():
    db_analysis.test()


if __name__ == "__main__":
    print "** main start **"
    db_initing()
    #web_reading()
    web_reading_threads()
    #db_analysising()
