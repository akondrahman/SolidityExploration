'''
Akond Rahman 
June 25, 2018 
Monday 
HTML Scrapping 
'''
from lxml import html
import requests 

if __name__=='__main__':
    # url_ = 'http://econpy.pythonanywhere.com/ex/001.html'
    url_ = 'https://etherscan.io/address/0x34f0d846c766874413938994da32360cf0e4350d#code'    

    page = requests.get(url_)
    tree = html.fromstring(page.content)  

    source = tree.xpath('//pre[@class="js-sourcecopyarea"]/text()')
    print source

    # buyers = tree.xpath('//div[@title="buyer-name"]/text()')
    # print buyers 