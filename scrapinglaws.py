import requests
import pandas
import os
from urllib.parse import urljoin
from bs4 import BeautifulSoup

data = pandas.read_csv('urls.csv') 
urls = data['url'].tolist()
years = data["yearstr"].tolist()
numbers = data["number"].tolist()

folder_location = r'C:\Users\dario.marino5\Documents\R\webscraping'
if not os.path.exists(folder_location):
    os.mkdir(folder_location)
    
    
evtName = 'Legislative proposal published'

tdSel, spSel, aSel = 'div.ep-table-cell', 'span.ep_name', 'a[href$="EN.pdf"]'
dlSel = f'{tdSel}+{tdSel}+{tdSel} {spSel}>{aSel}' 
trSel = f'div.ep-table-row:has(>{dlSel}):has(>{tdSel}+{tdSel} {spSel})'

for url in urls:
    response = requests.get(url)
    soup= BeautifulSoup(response.text, "html.parser")

    pgPdfLinks = [
        tr.select_one(dlSel).get('href') for tr in soup.select(trSel) if 
        evtName.strip().lower() in 
        tr.select_one(f'{tdSel}+{tdSel} {spSel}').get_text().strip().lower()
        ## if you want [case sensitive] exact match, change condition to
        # tr.select_one(f'{tdSel}+{tdSel} {spSel}').get_text() == evtName
    ]     
    for link in pgPdfLinks[:1]:
        # for link in... this can delete and put the last 3 if it does not work
        procnum = url.replace('?', '&').split('&procnum=')[-1].split('&')[0]
        procnum = ''.join(c if (
            c.isalpha() or c.isdigit() or c in '_-[]'
        ) else ('_' if c == '/' else '') for c in procnum)
        filename = f"proc-{procnum} {link.split('/')[-1]}"
        # filename = f"proc-{procnum} {link['href'].split('/')[-1]}" # in your current code

        filename = os.path.join(folder_location, filename)
        with open(filename, 'wb') as f:
            f.write(requests.get(urljoin(url, link)).content)
            # f.write(requests.get(urljoin(url['href'], link)).content) # in your current code
        
        
        
#        filename = os.path.join(folder_location, link.split('/')[-1])
#        with open(filename, 'wb') as f:
#            f.write(requests.get(urljoin(url, link)).content)
            
            
            
            
            
            
            