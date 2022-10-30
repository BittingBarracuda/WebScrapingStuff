from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import random

from pyrsistent import get_in

pages = set()
all_ext_links = set()
all_int_links = set()
random.seed(23)

def get_internal_links(bs, include_url):
    # Scheme -> Esquema de comunicación (http, https...)
    include_url = f'{urlparse(include_url).scheme}://{urlparse(include_url).netloc}'
    internal_links = []
    for link in bs.find_all('a', href = re.compile('^(/|.*'+include_url+')')):
        if link.attrs['href'] is not None:
            if link.attrs['href'].startswith('/'):
                internal_links.append(include_url + link.attrs['href'])
            else:
                internal_links.append(link.attrs['href'])
    return internal_links

def get_external_links(bs, exclude_url):
    external_links = []
    # Encuentra todos los enlaces que empiezan con http o www
    # que no contienen la URL actual
    for link in bs.find_all('a', href=re.compile('^(http|www)((?!'+exclude_url+').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in external_links:
                external_links.append(link.attrs['href'])
    return external_links

def get_random_external_link(starting_page):
    html = urlopen(starting_page)
    bs = BeautifulSoup(html.read(), 'html.parser')
    external_links = get_external_links(bs, urlparse(starting_page).netloc)
    if len(external_links) == 0:
        print('No external links, looking around the site for one')
        domain = f'{urlparse(starting_page).scheme}://{urlparse(starting_page).netloc}'
        internal_links = get_internal_links(bs, domain)
        return get_random_external_link(random.choice(internal_links))
    else:
        return random.choice(external_links)

def follow_external_only(starting_site):
    external_link = get_random_external_link(starting_site)
    print(f'Random external link is: {external_link}')
    follow_external_only(external_link)

def get_all_external_links(site_url):
    global all_ext_links, all_int_links

    html = urlopen(site_url)
    domain = f'{urlparse(site_url).scheme}://{urlparse(site_url).netloc}'
    bs = BeautifulSoup(html.read(), 'html.parser')
    internal_links = get_internal_links(bs, domain)
    external_links = get_external_links(bs, domain)
    #print(internal_links)
    #print(external_links)

    for link in external_links:
        if link not in all_ext_links:
            all_ext_links.add(link)
            print(link)
    for link in internal_links:
        if link not in all_int_links:
            all_int_links.add(link)
            get_all_external_links(link)

if __name__ == "__main__":
    #follow_external_only('http://oreilly.com')
    #global all_int_links
    all_int_links.add('http://oreilly.com')
    get_all_external_links('http://oreilly.com')