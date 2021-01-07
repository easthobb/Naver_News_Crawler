import requests
from bs4 import BeautifulSoup
import csv
import time

class Crawler(object):
    def __init__(self):
        self.search_word = "" 
        self.start_period = ""
        self.end_period = ""
        self.URL_list = list()
        self.article_list = list()
    
    def set_options(self,word,start,end):
        
        self.search_word = word
        self.start_period = start
        self.end_period = end


    def create_search_URL(self,page):
        return (
            "https://search.naver.com/search.naver?&where=news&query="+
            self.search_word +
            "&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=4&"+
            "ds=" + self.start_period + "de=" + self.end_period +
            "&docid=&nso=so:r,p:" +
            "from"+ (self.start_period).replace('.','') + "to" + (self.end_period).replace('.','') +
            ",a:all&mynews=0&cluster_rank=29&" +
            "start=" + str(page) +
            "&refresh_start=0"
        )

    def get_inner_links(self,URL):
        ## 
        link_list = [] # 개별 article 접근, 로우로 접근 불가,  
        URL_list = [] # 가공된 article 접근 URL 리스트(반환)
        oid_aid_list = [ ] # oid,aid 저장용도 2차원 배열[[oid0,aid0],...]

        html = requests.get(URL)
        soup = BeautifulSoup(html.text,"html.parser")
        articles = soup.select("ul.list_news > li")
        
        for ar in articles:
        ## 종후전임님이 알려주신 접근 방법
            links = ar.select('a')
            for link in links:
                if 'news.naver' in link['href']:
                    link_list.append(link)

        link_list = list(set(link_list)) # 중복 링크 제거
        link_list = list(map(str,link_list))

        for link in link_list:
            oid = link.split("oid=")[1].split('&')[0]
            aid = link.split("aid=")[1].split('&')[0].split('"')[0]
            ##임시로 oid>5000 일 경우, 네이버 미서비스 기사 파싱하지 않음
            if(int(oid)>5000):
                pass
            oid_aid_list.append([oid,aid])

        ##개별 기사 접근 url 생성
        baseArticleURL = [ 
            'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=105&oid=',
            #oid
            '&aid=',
            #aid
        ]
        for oid, aid in oid_aid_list:
            URL = baseArticleURL[:]
            URL.insert(1,str(oid))
            URL.append(str(aid))
            URL = "".join(URL)
            URL_list.append(URL)


        return URL_list

    def get_article(self,URL):
        
        req = requests.get(URL,headers={'User-Agent':'Mozilla/5.0'})
        soup = BeautifulSoup(req.text,"html.parser")

        title = soup.find("h3",{"id":"articleTitle"}).text
        print(title)
        time = soup.find("span",{"class":"t11"}).text
        text = soup.find("div",{"id":"articleBodyContents"}).text
        press = soup.find("div",{"class":"press_logo"})
        press = str(press).split("title=\"")[1].split("\"")[0]
        text_altered = str(text).replace(" ","")
        author = text_altered[text_altered.find("기자")-3:text_altered.find("기자")+2]
        
        article = [str(self.search_word),str(title),str(time),str(text),str(press),str(author)]

        return article

    def convert_to_csv(self,article_list):

        with open('./result.csv', 'w', encoding='utf-8-sig', newline='') as f: 
            writer = csv.writer(f) 
            writer.writerow(['key_word','title','pub_time','article_text','press','author'])
            for article in enumerate(article_list):
                if(article[0]<=100):
                    writer.writerow(article[1],) 
 

    def start(self):

        ## 사용자 입력 부분 - 조건 걸어야 함
        print("input search word : ")
        self.search_word = input()
        print("input search start period(like 2020.01.01 ) : ")
        self.start_period = input()
        print("input search end period(like 2020.01.01 ) : ")
        self.end_period = input()

        ## 포털 검색창에서 URL 생성
        for i in range(10):
            portal_URL = self.create_search_URL(1+i*0)
            print("requesting : ", portal_URL)
            self.URL_list = self.URL_list + self.get_inner_links(portal_URL)
            if(len(self.URL_list)>=100):
                break
        
        ## 링크리스트 내 아티클 접근 및 정보 크롤링
        for URL in self.URL_list:
            article = self.get_article(URL)
            #time.sleep(1)
            self.article_list.append(article)
        
        ## CSV 변환
        self.convert_to_csv(self.article_list)

        print("all done")




if __name__ == "__main__":
    Crawler = Crawler()
    Crawler.start()