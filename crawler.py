import requests
import re
from urllib.parse import urlparse
import config
from store import Store
from data import Documents
from queue import Queue
from parse import parse
import datetime
from sys import argv


class Crawler:
    def __init__(self, seeds):
        """
        Initialize the crawler
        :param seeds:[string] URL set, seed of crawler
        """
        self.seeds = seeds
        self.visited = set()
        self.queue = Queue()
        self.discover_count = 0
        self.documents = {}
        for url in seeds:
            self.queue.put(url)

    def __call__(self):
        """
        Run crawler. Scrap the web and sub-links
        :return: {String:{String:Int}} for each url store amount of time appear each word in.
        """
        while not self.queue.empty():
            if len(self.visited) > config.page_count - 1:
                break
            url = self.queue.get()
            if url not in self.visited:
                html = self.read_html(url)
                if html != '':
                    self.visited.add(url)
                    html_parsed = parse(html)
                    self.documents[url] = html_parsed
                    self.discover_count += 1
                    print(f'Link: {url}, {self.discover_count}')
                    for i in self.parse_link(url):
                        self.queue.put(i)
        return self.documents

    def read_html(self, url):
        """
        Read teh content of URL
        :param url: String
        :return: String content in url
        """
        try:
            h = requests.head(url, timeout=2)
            ct = h.headers.get('content-type').split(';')[0]
            if not ct == 'text/html':
                return ''
            html = requests.get(url)
        except Exception as e:
            print(e)
            return ''
        return html.content.decode('latin-1')

    def parse_link(self, url):
        """
        Get link in document of url
        :param url: String
        :return: [String] list of url in html
        """
        html = self.read_html(url)
        url_info = urlparse(url)
        links_to_check = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', html)
        for i in range(len(links_to_check)):
            if not urlparse(links_to_check[i]).netloc:
                if links_to_check[0] == '/':
                    links_to_check[i] = url_info.scheme + url_info.netloc + links_to_check[i]
                else:
                    links_to_check[i] = url + links_to_check[i] if url[-1] == '/' else url + '/' + links_to_check[i]
        return set(filter(lambda x: 'mailto' not in x, links_to_check))


if __name__ == "__main__":
    if len(argv) <= 1:
        print("python3 crawler url_document seeds\n"
              # "[-save]: For make a local save of de more relevant documents\n"
              "url_document: URL of document to compare\n"
              "seeds: URLs of seeds for crawler")
    else:
        storage = Store()
        if argv[1] in ['-s', '--save']:
            storage = Store(save=True)
            argv.pop(1)
        t = datetime.datetime.now().timestamp()
        query_document = argv[1]
        seeds = argv[2:]
        crawler = Crawler(seeds)
        docs = crawler()
        query_document = crawler.read_html(query_document)
        query_document = parse(query_document)
        engine = Documents(query_document, docs)
        relevant = engine.get_relevant()
        storage.store(relevant, 'discovered/')
        storage.store(relevant[:config.relevant_count], 'relevant/')
        print((datetime.datetime.now().timestamp() - t))
