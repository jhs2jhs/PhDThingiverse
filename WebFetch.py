from Queue import Queue
import time
import urllib2
from threading import Thread, Lock, stack_size
import web_read
import socket

stack_size(32768*16)
socket.setdefaulttimeout(60) # 10 second

class Fetcher:
    def __init__(self, threads, get_retrives, web_processor):
        self.get_retrives = get_retrives
        self.web_processor = web_processor
        self.opener = urllib2.build_opener(urllib2.HTTPHandler)
        self.lock = Lock() 
        self.q = Queue() # for tasks
        self.threads = threads
        for i in range(threads):
            t = Thread(target=self.threadget)
            t.setDaemon(True)
            t.start()
        self.running = 0

    def __def__(self): # must to make sure all the thread is finished
        time.sleep(0.5)
        self.q.join()

    def taskleft(self):
        q1 = self.q.qsize()
        r = self.running
        left = q1 + r
        #print '***%d, \t%d, \t%d' %(left, q1, r)
        return left

    def push(self, req):
        self.q.put(req)
    def pop(self):
        return self.q.get()

    def webget(self, req, retries):
        #print "*******:", retries
        try:
            #url = 'http://www.thingiverse.com/thing:%d' % req
            #print url
            ans = self.opener.open(req).read()
            self.web_processor(ans, req)
            return
        except urllib2.HTTPError, what:
            #print what.code, req
            #self.q.put(req)
            return
        except urllib2.URLError, what:
            if retries > 0:
                #print "retries:", retries
                time.sleep(0.1)
                return self.webget(req, retries-1)
            else:
                self.q.put(req)
                #print "-----------------:"+req
                #return ''
                return
        #return ans

    def threadget(self):
        while True:
            #print self.q.qsize()
            req = self.q.get()
            with self.lock: # to make sure atom of thread
                self.running += 1
            self.webget(req, self.get_retrives)
            with self.lock:
                self.running -= 1
            self.q.task_done()
            time.sleep(0.1) # don't spam
            

    def start(self):
        self.q.join()


def fetch_single(url, web_processor):
    f = Fetcher(threads=1, get_retrives=3, web_processor=web_processor)
    f.push(url)
    f.start()

def fetch_multi(links, threads, web_processor):
    f = Fetcher(threads=threads, get_retrives=3, web_processor=web_processor)
    for url in links:
        f.push(url)
    f.start()

if __name__ == "__main__":
    print "start"
    links = ['http://www.thingiverse.com/thing:%d' %i for i in range (1, 20000)]
    #links = range(1, 20000)
    #fetch_single('http://www.thingiverse.com/thing:3', web_read.content_script_derived)
    fetch_multi(links, 50, web_read.content_script_derived)
    print "finish"


'''
if __name__ == "__main__":
    print "start"
    links = ['http://www.thingiverse.com/thing:%d' %i for i in range (1, 20000)]
    #links = range(1, 20000)
    f = Fetcher(threads=50, get_retrives=3, web_processor=web_read.content_script_derived)
    for url in links:
        f.push(url)
    f.start()
    print "finish"
'''



    
