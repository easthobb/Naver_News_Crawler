import requests
from bs4 import BeautifulSoup

result = requests.get("https://search.naver.com/search.naver?&where=news&query=LG%EC%A0%84%EC%9E%90&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=3&ds=2020.01.01&de=2020.01.30&docid=&nso=so:r,p:from20200101to20200130,a:all&mynews=0&cluster_rank=29&start=1&refresh_start=0")

#print(result.text)
# #print(indeed_result.text)

soup = BeautifulSoup(result.text,"html.parser")
articles = soup.select("ul.list_news > li")
link_list=[]
for ar in articles:
    link = ar.find('a',{"class":"dsc_thumb"})
    try:
        link_list.append(link.attrs['onclick'])
    except:
        pass

oid_sid_list =[]
for link in link_list:
    oid, sid = link.split("&g=")[1].split("&")[0].split(".")
    if(int(oid)>5000):
        pass
    else:
        oid_sid_list.append([oid,sid])

print(oid_sid_list)
print(len(oid_sid_list))
    #print(link)
    #link_list.append(link.attrs['onclick'])
    
    
    #title = ar.select_one("a.news_tit")
    #inner_link = ar.find_all('a',class_='info')
    #print(inner_link)

print(len(link_list))

# # articleUrl = soup.find("a")["href"]
# article_url = soup.find("a",{"class":"news_tit"})['href']
# article_raw = requests.get(article_url)
# innerHtml = BeautifulSoup(article_raw.text, "html.parser")
# print(innerHtml)
#links = pagination.find_all('a')




# links = pagination.find_all('a')

# pages =[]
# for link in links[:-1]:
#     pages.append(int(link.find('span').string))

# max_page = print(pages[-1])
    