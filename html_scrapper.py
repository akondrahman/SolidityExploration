'''
Akond Rahman 
June 25, 2018 
Monday 
HTML Scrapping 
reff: http://docs.python-guide.org/en/latest/scenarios/scrape/
'''
from lxml import html
import requests 
import os 

def getLinks(link_file):
    web_links = []
    with open(link_file, 'rU') as _fil:
         file_str = _fil.read()
         web_links = file_str.split('\n')
         web_links = [x_ for x_ in web_links if len(x_) > 0]
    return web_links   

def dumpContentIntoFile(strP, fileP):
    fileToWrite = open( fileP, 'w')
    fileToWrite.write(strP )
    fileToWrite.close()
    return str(os.stat(fileP).st_size)

def getContentOfWebPage(link_str):
    txCount = 0 
    src = ''
    page = requests.get(link_str)
    tree = html.fromstring(page.content)  
    try:
       source = tree.xpath('//pre[@class="js-sourcecopyarea"]/text()')
       if(len(source)> 0):
         src    = source[0] ## output is stored in a list 
    except IndexError as e:
       print 'Got an index error ... not sure why ....:', e 
    ### one contract can have multiple SOL files as source 
    # print source
    txCountStr  = tree.xpath('//span[@title="Normal Transactions"]/text()')
    # print txCountStr
    if (len(txCountStr) > 0):
       txCountStr  = txCountStr[0] ## output is stored in a list 
       txCount     = int(txCountStr.split(' ')[0])
    print txCount
    return src, txCount

if __name__=='__main__':
    eth_link_file = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/100_filtered_contracts_list.txt'
    # url_ = 'https://etherscan.io/address/0x34f0d846c766874413938994da32360cf0e4350d#code'    


    links = getLinks(eth_link_file)
    # print links
    count = 0 
    str_map = ''
    for web_lin in links:
       sol_src, tra_cnt =getContentOfWebPage(web_lin)
       count += 1 
       file2save = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/verified_contracts/' + str(count) + '.sol'
       saved_bytes = dumpContentIntoFile(sol_src, file2save)
       print '{} processed, {} more to go'.format(count, len(links) - count)
       print '*'*25
       str_map = str_map + web_lin + ',' + file2save + ',' + str(tra_cnt) + ',' + str(saved_bytes) + '\n'
    str_map = 'CONTRACT_LINK,CONTRACT_SOURCE,TX_CNT,SOURCE_SIZE' + '\n' + str_map
    dumpContentIntoFile(str_map, '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/verified_contracts/THE_MAP.csv')

