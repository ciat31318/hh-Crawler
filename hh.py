import os 
import re 
import requests
from bs4 import BeautifulSoup as bs
from sys import platform 

class Crawler:
    

    def __init__(self, target_url):
        
        self.url = target_url 
        self.html = self.analyze()
    
    def analyze( self ):
        headers = {'Cookie':\
            '611e55XbD_e8d7_smile=1D1; 611e55XbD_e8d7_ulastactivity=9140ZnTz7ewh9LsrCLDv1gL4JCyjVRCM9Ulg%2FRiWHLks%2Bovx3ORm; 612e55XbD_e8d7_smile=1D1; 612e55XbD_e8d7_ulastactivity=8bbfRVm7Qf5jrmLTg%2F9wvvLmI2fAnAylxZTF1qCnqbF77g996q9h; 613e55XbD_e8d7_smile=1D1; 613e55XbD_e8d7_ulastactivity=4b49aekSOvZUUqKObyTh9mfmvAShR0Hi257oNVAtHN4ZEf4MJz2P; 614e55XbD_e8d7_ulastactivity=8fe4tXJ5M01kvqvLhSvSJdRu9GSG4k8c1ba23OMC845TXO2e6amb; 614e55XbD_e8d7_smile=1D1; 615e55XbD_e8d7_smile=1D1; 615e55XbD_e8d7_ulastactivity=9d0fZd8QTwkdvVZeFNTdv6X8FXPthUGA5ZujudlNu5fXYEJyt4i9; 616e55XbD_e8d7_smile=1D1; 616e55XbD_e8d7_ulastactivity=2a2076DCQnW4vlMB0bYPyLbiNgBm8N5bRUUdkgaXzcp2dbcd5kmF; 617e55XbD_e8d7_auth=09d1by3NikMBDn4UBQt9csxCB7M0bbBNLr5UZzCuoFikOmX5jvZvJGrTepjj6s4; 617e55XbD_e8d7_lastvisit=1599974620; 617e55XbD_e8d7_ulastactivity=b241q3rM5hI6Pl6PeP%2BoWvTj5WGi7teNZpnwuCQ1rL7dJGZVHAl%2F; 617e55XbD_e8d7_favorite=a%3A1%3A%7Bi%3A431%3Bs%3A31%3A%22H+%E5%8B%95%E7%95%AB%E4%B8%8B%E8%BC%89%E5%8D%80%28%E4%B8%8A%E5%82%B3%E7%A9%BA%E9%96%93%29%22%3B%7D; 617e55XbD_e8d7_visitedfid=431; 617e55XbD_e8d7_smile=1D1; 618e55XbD_e8d7_auth=a747I9Enrfk2uVMbhgr5TRHsrRdO6X508CJwyQrY%2FWQst1L0rVR9uUofIsOOmrE; 618e55XbD_e8d7_lastvisit=1602157768; 618e55XbD_e8d7_smile=1D1; 618e55XbD_e8d7_sid=gzFZvg; 618e55XbD_e8d7_inlang=zh; 618e55XbD_e8d7_txlang=0; username=ciat31318; 618e55XbD_e8d7_ulastactivity=afc7j%2F5jh6tAmuqvoBwJtTElZobGWnQfpjUw%2FDqgu9Jd5trYk9fL; 618e55XbD_e8d7_sendmail=1; 618e55XbD_e8d7_onlineusernum=8720; 618e55XbD_e8d7_favorite=a%3A3%3A%7Bi%3A431%3Bs%3A31%3A%22H+%E5%8B%95%E7%95%AB%E4%B8%8B%E8%BC%89%E5%8D%80%28%E4%B8%8A%E5%82%B3%E7%A9%BA%E9%96%93%29%22%3Bi%3A205%3BN%3Bi%3A22%3Bs%3A29%3A%22%E5%8B%95%E7%95%AB%E4%B8%8B%E8%BC%89%E5%8D%80%28%E4%B8%8A%E5%82%B3%E7%A9%BA%E9%96%93%29%22%3B%7D; 618e55XbD_e8d7_indexview=all; 618e55XbD_e8d7_videoadult=1; 618e55XbD_e8d7_agree=206; 618e55XbD_e8d7_visitedfid=431D22; 618e55XbD_e8d7_forum_lastvisit=D_22_1602508073D_431_1602508096; 618e55XbD_e8d7_lastact=1602508097%09video.php%09'}
    
        session = requests.session()
        html = session.get(self.url,headers = headers)
        html.encode = 'utf-8'
        html = bs(html.text, 'html.parser')
        return html

class HMovie(Crawler):
    def __init__( self, target_url, hh_num ):
        super().__init__(target_url)
        self.hh_num = hh_num
        self.pages = self.page_links

    @property
    def page_links( self ):
        pages = []
        all_pages =  self.html.select('a.xst')  # .代表class \#代表id (css選擇器)  
        #print(self.html.select('a.xst'))
        for page in range(len(all_pages)):
            pages.append('http://www.eyny.com/{}'.format(all_pages[page]['href']))
        return pages
    
    def parser(self):
        content = ''
        count = 0   
        num = len(self.pages)
        for page in self.pages:
            crawler = Crawler(page)
            title_html = crawler.html.find('title')
            title = title_html.text.split()[1]
            href_html = crawler.html.find('link')
            #print(crawler.html)
            href = href_html['href']
            content += '{}\n{}\n\n'.format(title,href)
            count += 1
            print('Crawler: {:.2%}'.format(count/num))
        return content

class WriteFile:
    def __init__(self, file_name, data):
        self.file_name = file_name
        self.data = data
        self.write_data()
    
    def write_data(self):
        with open( self.file_name, 'wb' ) as f:
            f.write(self.data.encode('utf-8'))

    def open(self):
        path = os.path.abspath(self.file_name)
        os_mapping = {
            'linux':'gedit',
            'linux2':'gedit',
            'win32':''
        }
        os.system(os_mapping.get(platform)+path)
if __name__ == '__main__':
    print('Start Crawler...')
    url = 'http://www.eyny.com/forum.php?mod=forumdisplay&fid=431&filter=typeid&typeid=2397'
    file_name = 'hmovie.txt'
    crawler_page = 10
    hmovie = HMovie(url,crawler_page)
    data = hmovie.parser()
    write_file = WriteFile(file_name, data)
    write_file.open()










