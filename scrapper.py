from urllib import request
from queue import Queue
from threading import Thread
from parse import parse


class Scrapper:
    def __init__(self, seeds):
        self.seeds = seeds
        self.queue = Queue()
        self.threads = Queue(8)
        for url in seeds:
            self.queue.put(request.urlopen(url))

    def __call__(self):
        while not self.queue.empty():
            self.threads.put(
                Thread(target=parse, args=(
                    self.queue.get(),)
                       )
            )


