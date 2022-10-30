from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

random.seed(datetime.datetime.now())
pages = set()

def get_links_contents(article_url):
    global pages
    html = urlopen(f'http://en.wikipedia.org{article_url}')
    bs = BeautifulSoup(html, 'html.parser')
    try:
        print(bs.h1.get_text())
        print(bs.find(id='mw-content-text').find_all('p')[0])
        print(bs.find(id='ca-edit').find('span').find('a').attrs['href'])
    except AttributeError:
        print('This page is missing something! Continuing.')
    for link in bs.find_all('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                new_page = link.attrs['href']
                print('-'*20)
                print(new_page)
                pages.add(new_page)
                get_links_contents(new_page) 

def get_links_relaxed(article_url):
    global pages
    html = urlopen(f'http://en.wikipedia.org{article_url}')
    bs = BeautifulSoup(html, 'html.parser')
    for link in bs.find_all('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                new_page = link.attrs['href']
                print(new_page)
                pages.add(new_page)
                get_links_relaxed(new_page)

def get_links(article_url):
    html = urlopen(f'http://en.wikipedia.org{article_url}')
    bs = BeautifulSoup(html, 'html.parser')
    return bs.find('div', {'id':'bodyContent'}).find_all(
        'a', href = re.compile('^(/wiki)((?!:).)*$')
    )

def main(base_url):
    links = get_links(base_url)
    while len(links) > 0:
        new_article = random.choice(links).attrs['href']
        print(new_article)
        links = get_links(new_article)

if __name__ == "__main__":
    #main('/wiki/Kevin_Bacon')
    #get_links_relaxed('')
    get_links_contents('')

'''
def kb_page():
    html = urlopen('http://en.wikipedia.org/wiki/Kevin_Bacon')
    bs = BeautifulSoup(html.read(), 'html.parser')
    #for link in bs.find_all('a'):
    #    if 'href' in link.attrs:
    #        print(link.attrs['href'])
    for link in bs.find('div', {'id':'bodyContent'}).find_all(
        'a', href = re.compile('^(/wiki)((?!:).)*$')):
        if 'href' in link.attrs:
            print(link.attrs['href'])
'''