from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def ex_1():
    html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
    bs = BeautifulSoup(html.read(), 'html.parser')
    name_list = bs.find_all('span', {'class':'green'})
    for name in name_list:
        print(name.get_text())

def ex_2():
    html = urlopen('http://www.pythonscraping.com/pages/page3.html')
    bs = BeautifulSoup(html.read(), 'html.parser')
    #for line in html.readlines():
    #    print(line)
    for child in bs.find('table', {'id':'giftList'}).children:
        print(child)
    for sibling in bs.find('table', {'id':'giftList'}).tr.next_siblings:
        print(sibling)
    print(bs.find('img', {'src':'../img/gifts/img1.jpg'}).parent.previous_sibling.get_text())
    images = bs.find_all('img', {'src':re.compile('\.\./img\/gifts/img.*\.jpg')})
    for image in images:
        print(image['src'])
    two_attrs = bs.find_all(lambda tag: len(tag.attrs) >= 2)
    for tag in two_attrs:
        print(tag.get_text())
    

if __name__ == "__main__":
    ex_2()