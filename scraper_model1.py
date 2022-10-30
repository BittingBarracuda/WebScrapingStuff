from bs4 import BeautifulSoup
from matplotlib.pyplot import title
import requests

class Content:
    def __init__(self, topic, url, title, body):
        self.topic = topic
        self.title = title
        self.body = body
        self.url = url
    
    def print(self):
        print(f'URL: {self.url}')
        print(f'TITLE: {self.title}')
        print(f'BODY:\n{self.body}')
        print(f'URL: {self.url}')