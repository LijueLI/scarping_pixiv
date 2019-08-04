from selenium import webdriver
from bs4 import BeautifulSoup
import os
import urllib.request

driver = webdriver.Chrome(executable_path="chromedriver")
driver.get('https://www.pixiv.net/search.php?s_mode=s_tag&word=kp31')
pageSource = driver.page_source
soup = BeautifulSoup(pageSource,'html5lib')
sectiontag = soup.find(id="js-react-search-mid")
a = sectiontag.findChildren("a")
record = ""
idlast = ""
for href in a:
    string = href.get('href')
    id = string.partition('illust_id=')
    if(id[2]!='' and id[2]!=idlast):
        record = record+id[2]+'\n'
        spans=href.findChildren("span")
        index = 0
        for span in spans:
            if(span.text!=''):
                index = int(span.text)
        if(index != 0):
            for i in range(1,index+1):
                link = 'https://pixiv.cat/'+id[2]+'-'+str(i)+'.png'
                print(link)
                local = os.path.join('image/'+id[2]+'-'+str(i)+'.png')
                opener=urllib.request.build_opener()
                opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36')]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(link,local)
        else:
            link = 'https://pixiv.cat/'+id[2]+'.png'
            print(link)
            local = os.path.join('image/'+id[2]+'.png')
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(link,local)
        #print(id[2])
        idlast = id[2]

testfile = open('test.txt','w')
testfile.write(record)
testfile.close()

driver.close()