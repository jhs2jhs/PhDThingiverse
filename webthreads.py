from Queue import Queue
from threading import Thread, Lock, stack_size
import urllib2

class ThreadURLs(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
    def run(self):
        while True:
            req = self.queue.get()
            with self.lock
