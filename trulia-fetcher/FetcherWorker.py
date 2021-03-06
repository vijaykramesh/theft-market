import threading
import urllib2
import time
import ParserWorker

class FetcherWorker(threading.Thread):

    def __init__(self, url_queue, apikey, match_rule, writers, locks, metadata_table):
        self.url_queue = url_queue
        #self.text_queue = text_queue
        self.apikey = apikey
        self.writers_params = {"match_rule":match_rule, "writers":writers, "locks":locks, "metadata_table":metadata_table}
        threading.Thread.__init__(self)

    def run(self):
        while 1:

            url_tup = self.url_queue.get()
            if url_tup is None:
                # add end-of-queue markers for parsers
                #self.text_queue.put(None) 
                # ends thread
                break

            url = url_tup[0] + self.apikey 
            location = url_tup[1]
            t1 = time.time()
            
            # try twice for now, put in while loop next
            print "fetching try 1", location
            resp = urllib2.urlopen(url)
            if resp.code == 200: 
                text = resp.read()
                ParserWorker.ParserWorker((text,location, self.writers_params)).start()
                #self.text_queue.put((text, location))
            else:
                print 'failed once', location
                time.sleep(10)
                print "fetching try 2", location
                resp = urllib2.urlopen(url)
                if resp.code == 200:
                    text = resp.read()
                    ParserWorker.ParserWorker((text,location, self.writers_params)).start()
                    #self.text_queue.put((text, location))

            #print "done fetching", location

            # make sure we don't use the same API key within 2 seconds
            t2 = time.time()
            if t2 - t1 < 2.0:
                time.sleep(2.0 - (t2 - t1))

            self.url_queue.task_done()
