#!/usr/bin/env python
import time
import Queue
import threading
import random

q = Queue.Queue()
l = threading.Lock()
stalls = {}

class ProducerThread(threading.Thread):
    def __init__(self):
        super(ProducerThread, self).__init__()
        self.daemon = True
    def run(self):
        global q
        while True:
            item = [random.choice(range(5)),random.choice (range(2))]
            print "Item produced" + str(item)
            q.put(item)
            time.sleep (1)
class ConsumerThread(threading.Thread):
    def __init__(self):
        super(ConsumerThread, self).__init__()
        self.daemon = True
    def addItem(self, item):
        global stalls
        if (stalls.has_key(item[0])):
            if (stalls[item[0]] != item[1]):
                stalls[item[0]] = item[1]
        else:
            stalls[item[0]] = item[1]
        print repr(stalls)
    def run(self):
        global q
        global l
        while True:
            item = q.get()
            q.task_done()
            l.acquire()
            self.addItem(item)
            l.release()

            #print ("Consumed " + str(item) + "items in queue: " + str(q.qsize()))
            #time.sleep(random.random())

ProducerThread().start()
ConsumerThread().start()

while True:
    time.sleep(1)
