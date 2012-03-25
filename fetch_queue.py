import Queue
import threading
import urllib2
import time
from BeautifulSoup import BeautifulSoup
import web_read
import web_processor


hosts = ['http://www.thingiverse.com/thing:%d' %i for i in range (1, 200)]

queue_in = Queue.Queue()
out_queue = Queue.Queue()

class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, retrives, queue_in, out_queue, web_scripting):
        threading.Thread.__init__(self)
        self.queue_in = queue_in
        self.out_queue = out_queue
        self.opener = urllib2.build_opener(urllib2.HTTPHandler)
        self.retrives = retrives
        self.web_scripting = web_scripting

    def webget(self, req, retries):
        try:
            url = urllib2.urlopen(req)
            chunk = url.read()
            #print chunk
            return chunk
        except urllib2.HTTPError as what:
            return ''
        except urllib2.URLError as what:
            if retries > 0:
                time.sleep(0.1)
                return self.webget(req, retries-1)
            else:
                self.queue_in.put(req)
                return ''
        except Exception as what:
            # need to log the error here
            return ''
    

    def run(self):
        while True:
            #grabs host from queue
            host = self.queue_in.get()

            #grabs urls of hosts and then grabs chunk of webpage
            #url = urllib2.urlopen(host)
            #print url
            #chunk = url.read()
            chunk = self.webget(host, self.retrives) # chunk can be ''
            #print chunk
            pagedict = self.web_scripting(chunk, host)

            #place chunk into out queue
            self.out_queue.put((host, pagedict))

            #signals to queue job is done
            self.queue_in.task_done()
            time.sleep(0.1)

class DatamineThread(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, out_queue, web_processing):
        threading.Thread.__init__(self)
        self.out_queue = out_queue
        self.web_processing = web_processing

    def run(self):
        while True:
            #grabs host from queue
            host, pagedict = self.out_queue.get()
            print pagedict
            self.web_processing(pagedict, host)

            #parse the chunk
            #soup = BeautifulSoup(chunk)
            #print soup.findAll(['title'])

            #signals to queue job is done
            self.out_queue.task_done()

start = time.time()
def main():

    #spawn a pool of threads, and pass them queue instance
    for i in range(10):
        t = ThreadUrl(3, queue_in, out_queue, web_read.content_scripting)
        t.setDaemon(True)
        t.start()

    #populate queue with data
    for host in hosts:
        queue_in.put(host)

    for i in range(10):
        dt = DatamineThread(out_queue, web_processor.page_processing)
        dt.setDaemon(True)
        dt.start()


    #wait on the queue until everything has been processed
    queue_in.join()
    out_queue.join()

main()
print "Elapsed Time: %s" % (time.time() - start)
