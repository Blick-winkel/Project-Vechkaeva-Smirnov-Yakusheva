import urllib.request as url
import re,os,codecs
from bs4 import BeautifulSoup
authorsurl = ['http://www.the-village.ru/users/984403/posts']
              #'http://www.the-village.ru/users/970043/posts','http://www.the-village.ru/users/1062749/posts']
authors_texts = {}
def get_address():
    global authorsurl
    global authors_texts
    for urll in authorsurl:
        page = url.urlopen(urll)
        text = page.read().decode('utf-8')
        pagenumber2 = re.search('">([0-9]*?)</a></li></ul><a class="pages-arrow next"', text)
        pagenumber3 = int((pagenumber2.group(1)))
        name = re.search('data-full_name="(.*?)"',text)
        print (name.group(1))
        authors_texts[name.group(1)] = []
        for pagenumber in range(1,pagenumber3 + 1):
            page = url.urlopen(urll + '?&page='+str(pagenumber))
            text = page.read().decode('utf-8')
            texts =re.findall('post-block-.*?"><a href="(.*?)" class="post-link"', text)
            for tex in texts:
                if tex not in authors_texts[name.group(1)]:
                    authors_texts[name.group(1)].append(tex)
get_address()

print(authors_texts)
def getting_texts():
    global authors_texts
    for author in authors_texts:
        for text1 in authors_texts[author]:
            print(text1)
            page = url.urlopen('http://www.the-village.ru/'+text1)
            text = page.read().decode('utf-8')
            if not os.path.exists(author):
                os.makedirs(author)
            textname = re.sub('/','_',text1)
            f = codecs.open(author+'/'+textname+'.txt','w', 'utf-8')
            html = text
            parsed_html = BeautifulSoup(html,'html.parser')
            text2 = (parsed_html.body.find('div',attrs={'class':'article-text'}).text)
            f.write(text2)
            f.close()

getting_texts()