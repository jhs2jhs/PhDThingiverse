import web_read
import db_init
import db_insert

def db_initing():
    print "** db_initing **"
    db_init.init()
    print "** db_initing finish **"
    #db_insert.test()

def web_reading():
    print "** web_reading **"
    #web_read.test()
    index_start = 13661
    index_end = 19316 # it can be finded by visiting this site: http://www.thingiverse.com/newest
    web_read.page_loop(index_start, index_end)
    #web_read.page_read(7)
    #web_read.page_read(17773)
    print "** web_reading finish **"

if __name__ == "__main__":
    print "** main start **"
    db_initing()
    web_reading()
