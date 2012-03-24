from Queue import Queue
import time
import urllib2
from threading import Thread, Lock, stack_size
import web_read
import socket

stack_size(32768*16)
socket.setdefaulttimeout(10) # 10 second

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
                print "retries:", retries
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

##########################

class FetcherIO:
    def __init__(self, threads, get_retrives, web_scriptor):
        self.get_retrives = get_retrives
        self.web_scriptor = web_scriptor
        self.opener = urllib2.build_opener(urllib2.HTTPHandler)
        self.lock = Lock() # 
        self.q_req = Queue() #
        self.q_ans = Queue() #
        self.threads = threads
        for i in range(threads):
            t = Thread(target=self.threadget)
            t.setDaemon(True)
            t.start()
        self.running = 0
 
    def __del__(self): #
        time.sleep(0.5)
        self.q_req.join()
        self.q_ans.join()
 
    def taskleft(self):
        return self.q_req.qsize()+self.q_ans.qsize()+self.running
 
    def push(self,req):
        self.q_req.put(req)
 
    def pop(self):
        return self.q_ans.get()

    def webget(self, req, retries):
        try:
            ans = self.opener.open(req).read()
            return self.web_scriptor(ans, req)
        except urllib2.HTTPError, what:
            return {}
        except urllib2.URLError, what:
            if retries > 0:
                time.sleep(0.1)
                return self.webget(req, retries-1)
            else:
                self.q_req.put(req)
                print "99999999999999:", req
                return {}
        except Exception, what:
            print what
            return {}
        #return ans
 
    def threadget(self):
        while True:
            req = self.q_req.get()
            with self.lock: #critical area
                self.running += 1
            out = self.webget(req, self.get_retrives)
            self.q_ans.put((req, out))
            with self.lock:
                self.running -= 1
            self.q_req.task_done()
            time.sleep(0.1) # don't spam

def single_get(ans, req):
    return {'content':ans}

def fetchio_single(url): # need to be modify
    f = FetcherIO(threads=1, get_retrives=3, web_scriptor=single_get)
    f.push(url)
    content = {}
    while f.taskleft():
        url, content = f.pop()
    if content.has_key('content'):
        return (url, content['content'])
    else:
        return (url, '')

def fetchio_multi(links, threads, web_scriptor, web_processor):
    f = FetcherIO(threads=threads, get_retrives=3, web_scriptor=web_scriptor)
    for url in links:
        f.push(url)
    print f.taskleft()
    while f.taskleft():
        url, pagedict = f.pop()
        #print url
        web_processor(pagedict, url)

def fetch_multi_once_thread_pool(times, interval, threads, web_scriptor, web_processor):
    f = FetcherIO(threads=threads, get_retrives=3, web_scriptor=web_scriptor)
    #for url in links:
    #    f.push(url)
    for index in range(times):
        start = index*interval
        end = (index+1)*interval
        for url in ['http://www.thingiverse.com/thing:%d' %i for i in range (start, end)]:
            f.push(url)
        print " === finish %d to %d ==="%(start, end)
    while f.taskleft():
        url, pagedict = f.pop()
        #print url
        web_processor(pagedict, url)


if __name__ == "__main__":
    #links = [ 'http://www.verycd.com/topics/%d/'%i for i in range(5420,5430) ]
    links = ['http://www.thingiverse.com/thing:%d' %i for i in range (1, 200)]
    #f = Fetcher(threads=50)
    f = FetcherIO(threads=50, get_retrives=3, web_scriptor=web_read.content_script_derived)
    for url in links:
        f.push(url)
    while f.taskleft():
        url,content = f.pop()
        #print url,len(content)
        web_read.page_insert_derived(content, url)


'''
if __name__ == "__main__":
    print "start"
    links = ['http://www.thingiverse.com/thing:%d' %i for i in range (1, 20000)]
    #links = range(1, 20000)
    #fetch_single('http://www.thingiverse.com/thing:3', web_read.content_script_derived)
    fetch_multi(links, 50, web_read.content_script_derived)
    print "finish"
'''


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



    
