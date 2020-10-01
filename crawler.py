from html.parser import HTMLParser
import requests
from urllib import request, parse
import sys

class LinkParser(HTMLParser):
    def __init__(self):
        self.link=[]
        HTMLParser.__init__(self)

    def handle_starttag(self,tag,attrs):
        if tag =='a':
            try:
                self.link.append( dict(attrs)["href"])
            except KeyError:
                pass


def prepare_url(url, nexturl):

    newurl = parse.urljoin(url, nexturl)
    newurl = newurl.split('#')[0]
    newurl = newurl.split('?')[0]
    return newurl



def crawl(url, max_depth=3, depth=0):
    
    if url in visited:
        return
    visited.add(url)

    print(request.unquote(url))
    try:
        page = requests.get(url)
        if page.status_code == 200:    
            html = page.text
            lparser = LinkParser()
            lparser.feed(html)
            depth+=1
            if depth <= max_depth:
                for l in lparser.link:
                    crawl(prepare_url(url,l), max_depth, depth)
    except: 
        pass


visited = set()


if __name__ == '__main__':
    import argparse
    argp = argparse.ArgumentParser(
        prog = 'crawler',
        description = """Mon crawler""",
        epilog = """ mon epilog crawl"""
    )
    argp.add_argument(
            'url',
            help = """url ou crawler""",
            type = str
    )
    argp.add_argument(
            'max_depth',
            nargs='?',
            help = """max depth, default = 3""",
            type = int
    )
    arg = argp.parse_args()
    if len(sys.argv) > 2:
        crawl(arg.url, arg.max_depth)
    else:
        crawl(arg.url)
