'''
Akond Rahman 
June 25, 2018 
Monday 
HTML Scrapping 
'''
from lxml import html
import requests 

if __name__=='__main__':
    url_ = 'http://econpy.pythonanywhere.com/ex/001.html'
    page = requests.get(url_)
    tree = html.fromstring(page.content)  