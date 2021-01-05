import requests
from bs4 import BeautifulSoup

## 사용자 입력 필요
result = requests.get("https://search.naver.com/search.naver?&where=news&query=LG%EC%A0%84%EC%9E%90&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=3&ds=2020.01.01&de=2020.01.30&docid=&nso=so:r,p:from20200101to20200130,a:all&mynews=0&cluster_rank=29&start=1&refresh_start=0")

## list_news에서 개별 뉴스에 접근
soup = BeautifulSoup(result.text,"html.parser")
articles = soup.select("ul.list_news > li")

##개별 뉴스로부터 oid,aid 받아옴

dsc_thumb_list=[ ] # dsc_thumb class에 onclick 저장 용도
oid_aid_list = [ ] # oid,aid 저장용도 2차원 배열[[oid0,aid0],...]

for ar in articles:
    link = ar.find('a',{"class":"dsc_thumb"})
    try:
        dsc_thumb_list.append(link.attrs['onclick'])
    except:
        pass

for dsc_thumb in dsc_thumb_list:
    oid, aid = dsc_thumb.split("&g=")[1].split("&")[0].split(".")
    ##임시로 oid>5000 일 경우, 네이버 미서비스 기사 파싱하지 않음
    if(int(oid)>5000):
        pass
    oid_aid_list.append([oid,aid])

#https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=105&oid=092&aid=0002179720
##개별 기사 접근 url 생성
baseArticleURL = [ 'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=105&oid=',
    #oid
    '&aid=',
    #aid
]

## 제목, 내용, 언론사, 발행시간, 기자 추출


## 리스트 CSV로 전환 및 저장