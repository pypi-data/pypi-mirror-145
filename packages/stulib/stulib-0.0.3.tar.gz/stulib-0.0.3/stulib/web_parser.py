import requests
from bs4 import BeautifulSoup
import re

def parse(url):
    return get_web_document(url)


def get_web_document(url:str, tag:str = 'p,li'):
    tagl = tag.split(',')
    results  = getweb_document(url, tagl)
    return results

def getweb_document(url, tag):
    res = requests.get(url)
    if res:
        soup = BeautifulSoup(res.content, 'html.parser')
    d = {}
    str_con = ''
    vlist = []
    og = getweb_og(soup)
    
    for a in soup.findAll(tag):
        text = a.text.strip()
        if len(text) != 0:
            str_con += text + '\n'
            vlist.append(text)
        
    str_con = str_con.strip()
    
    d['content'] = str_con
    d['vlist'] = vlist
    d.update(og)
    
    return d


def getweb_og(soup):
    d = {}
    
    for a in soup.findAll('meta', property=True):
        if str(a['property']).startswith('og'):
            d[a['property']] = a['content'].strip()

    return d

def isurl(url):

    regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None