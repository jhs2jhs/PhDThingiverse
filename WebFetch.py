from Queue import Queue
import time
import urllib2
from threading import Thread, Lock, stack_size
import web_read

stack_size(32768*16)

class Fetcher:
    def __init__(self, threads, get_retrives):
        self.get_retrives = get_retrives
        self.opener = urllib2.build_opener(urllib2.HTTPHandler)
        self.lock = Lock() 
        self.q = Queue() # for tasks
        self.q_un = Queue()
        self.threads = threads
        for i in range(threads):
            t = Thread(target=self.threadget_init)
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

    def get_times(self, req, retries):
        #print "*******:", retries
        try:
            ans = self.opener.open(req).read()
            print "==", req
            index = req.strip("\n\thttp://www.thingiverse.com/thing:")
            index = int(index)
            print "index:", index
            #self.q_2.put((req, ans))
            web_read.content_script_derived(ans, index)
            return
        except urllib2.HTTPError, what:
            print what.code, req
            #self.q.put(req)
            return
        except urllib2.URLError, what:
            if retries > 0:
                print "retries:", retries
                return self.get_times(req, retries-1)
            else:
                self.q.put(req)
                print "-----------------:"+req
                #return ''
                return
        #return ans

    def threadget_init(self):
        while True:
            #print self.q.qsize()
            req = self.q.get()
            with self.lock: # to make sure atom of thread
                self.running += 1
            self.get_times(req, self.get_retrives)
            with self.lock:
                self.running -= 1
            self.q.task_done()
            time.sleep(0.1) # don't spam
            

    def start(self):
        self.q.join()


if __name__ == "__main__":
    print "start"
    links = ['http://www.thingiverse.com/thing:%d' %i for i in range (1, 20000)]
    f = Fetcher(threads=50, get_retrives=3)
    for url in links:
        f.push(url)
    f.start()
    print "finish"

