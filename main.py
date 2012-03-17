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
    #web_read.page_loop()
    web_read.page_read(17773)
    print "** web_reading finish **"

if __name__ == "__main__":
    print "**main start**"
    db_initing()
    web_reading()
