# selenium driver : C:\\Users\\user1\\Desktop\\StockNews\\chromedriver.exe
from selenium import webdriver
import datetime
import pandas as pd
def PrintNews(headline_list, news_info, Text):
    for i in range(len(headline_list)):
        print('['+ news_info[i], end = '] ')
        print(headline_list[i])
        #print(Text[i]) #본문보기

def PrintPrice(NameList, PriceInfo, Fluctuation):
    for i in range(len(NameList)):
        print(NameList[i], end=' : ')
        print(PriceInfo[i], end='[KRW], / 전일대비 : ')
        print(Fluctuation[i])
def News_get_driver(Head):
   if(Head == False):
       chrome_options = webdriver.ChromeOptions()
       chrome_options.add_argument('headless')
       chrome_options.add_argument('--disable-gpu')
       chrome_options.add_argument('land=ko_KR')
       driver = webdriver.Chrome("C:\\Users\\user1\\Desktop\\StockNews\\chromedriver.exe", chrome_options=chrome_options)
       driver.implicitly_wait(1)
   else:
       driver = webdriver.Chrome("C:\\Users\\user1\\Desktop\\StockNews\\chromedriver.exe")
   url = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=101&sid2=258"  # Naver Stock News
   driver.get(url)  # driver open
   return driver

def get_headlines():
    headline_list = []
    news_info = []
    Text = []
    driver = News_get_driver(False)
    table = driver.find_element_by_class_name('type06_headline') # Section 1 Table 파싱
    rows = table.find_elements_by_tag_name("li")
    for index, value in enumerate(rows):
        try:
            body = value.find_elements_by_tag_name('dt')[1] #이미지가 첨부된 뉴스 헤드라인 파싱
            headline_list.append(body.text)
            info = value.find_elements_by_tag_name('dd')[0] # 신문사, 시간 파싱

        except:
            body = value.find_elements_by_tag_name('dt')[0] # 이미지 미첨부 뉴스 헤드라인 파싱
            headline_list.append(body.text)
        try:
            info = value.find_elements_by_tag_name('dd')[0] # 신문사, 시간 파싱
            info = info.text.split("\n")
            news_info.append(info[1])
            Text.append(info[0])
        except:
            print("Err ] info parsing")

    table = driver.find_element_by_class_name('type06') # Section 2 Table
    rows = table.find_elements_by_tag_name("li")
    for index, value in enumerate(rows):
        try:
            body = value.find_elements_by_tag_name('dt')[1] #이미지가 첨부된 뉴스 헤드라인 파싱
            headline_list.append(body.text)
        except:
            body = value.find_elements_by_tag_name('dt')[0] # 이미지 미첨부 뉴스 헤드라인 파싱
            headline_list.append(body.text)
        try:
            info = value.find_elements_by_tag_name('dd')[0]  # 신문사, 시간 파싱
            info = info.text.split("\n")
            news_info.append(info[1])
            Text.append(info[0])
        except:
            print("Err ] info parsing")
            
    return headline_list, news_info, Text # 순서대로 헤드라인, 신문사 정보 및 시간 정보, 본문 내용
def save_headlines(headline_list, news_info, Text):
    now = datetime.datetime.now()
    # print(now)  # 2015-04-19 12:11:32.669083
    #
    # nowDate = now.strftime('%Y-%m-%d')
    # print(nowDate)  # 2015-04-19
    #
    # nowTime = now.strftime('%H:%M:%S')
    # print(nowTime)  # 12:11:32
    nowDatetime = now.strftime('%Y_%m_%d_%H시%M분%S초')
    #print("[현재 시각] : " + nowDatetime)  # 2015-04-19 12:11:32

    data = pd.DataFrame({
        '헤드라인' : headline_list,
        '신문사 정보' : news_info,
        '본문' : Text
    })
    data.to_csv('Data/News'+nowDatetime+'.csv', index = False, encoding='cp949')
def NowPriceDriver(Head):
    if (Head == False):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('land=ko_KR')
        driver = webdriver.Chrome("C:\\Users\\user1\\Desktop\\StockNews\\chromedriver.exe",
                                  chrome_options=chrome_options)
        driver.implicitly_wait(1)
    else:
        driver = webdriver.Chrome("C:\\Users\\user1\\Desktop\\StockNews\\chromedriver.exe")
    url = "http://www.krx.co.kr/main/main.jsp"  # Naver Stock News
    driver.get(url)  # driver open
    return driver
def get_prices():
    NameList = [] # 종목
    PriceInfo=[] # 현재 가격 정보
    Fluctuation = [] #전일 대비 변동폭
    driver = NowPriceDriver(False)
    table = driver.find_element_by_class_name('section-wap-top')
    cols = table.find_elements_by_class_name('index-info_wap')
    for index, value in enumerate(cols):
        info = value.find_elements_by_class_name('index-price')[0]
        Name = value.find_elements_by_class_name('index-name')[0]
        change = value.find_elements_by_class_name('index-up')[0]
        NameList.append(Name.text)
        PriceInfo.append(info.text)
        Fluctuation.append(change.text)
    return NameList, PriceInfo, Fluctuation
