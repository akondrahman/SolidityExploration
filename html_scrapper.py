'''
Akond Rahman 
June 25, 2018 
Monday 
HTML Scrapping 
reff: http://docs.python-guide.org/en/latest/scenarios/scrape/
'''
from lxml import html
import requests 

def getLinks(link_file):
    web_links = []
    with open(link_file, 'rU') as _fil:
         file_str = _fil.read()
         web_links = file_str.split('\n')
         web_links = [x_ for x_ in web_links if len(x_) > 0]
    return web_links   

def getContentOfWebPage(link_str):
    page = requests.get(link_str)
    tree = html.fromstring(page.content)  
    source = tree.xpath('//pre[@class="js-sourcecopyarea"]/text()')[0] ## output is stored in a list 
    ### one contract can have multiple SOL files as source 
    # print source
    txCountStr  = tree.xpath('//span[@title="Normal Transactions"]/text()')[0] ## output is stored in a list 
    txCount     = int(txCountStr.split(' ')[0])
    print txCount

if __name__=='__main__':
    eth_link_file = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/100_filtered_contracts_list.txt'
    # url_ = 'https://etherscan.io/address/0x34f0d846c766874413938994da32360cf0e4350d#code'    


    links = getLinks(eth_link_file)
    # print links
    count = 0 
    for web_lin in links:
       getContentOfWebPage(web_lin)
       count += 1 
       print '{} processed, {} more to go'.format(count, len(links) - count)
       print '*'*25

