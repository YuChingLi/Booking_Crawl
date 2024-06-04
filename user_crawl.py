from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup as bs
from emoji import demojize as de
import json

#抓取評論
def get_review(soup):
    good_num = 0 
    review = []
    all_review = soup.find_all('div', attrs={'data-testid': "review-positive-text"})
    for review_li in all_review:
        try:
            if review_li.text not in ['無', '沒有']:
                review.append(de(review_li.text))
                good_num += 1
        except:
            print(review_li.text)
    all_review = soup.find_all('div', attrs={'data-testid': "review-negative-text"})
    for review_li in all_review:
        try:
            if review_li.text != '無':
                review.append(de(review_li.text))
        except:
            print(review_li.text)
    return review, good_num

#使用者輸入網址
user_url = input('請輸入飯店 booking.com 頁面網址 : ').split('?')[0]

driver = webdriver.Chrome()
driver.get(user_url)

sleep(5)

driver.find_element(By.XPATH, '//*[@id="basiclayout"]/div[1]/div[1]/div[1]/div[1]/div/nav/div/ul/li[6]/a').click()
sleep(5)
number_review = driver.find_element(By.XPATH, '//*[@id="hp-reviews-sliding"]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div[2]').text
number_review = eval(number_review.rstrip(' 則評語').replace(',', ''))

#抓取最近100筆評論資料
pages_remaining = True

if number_review >= 100:
    page_num = 10
else:
    page_num = number_review//10
    
page_current = 1

review = []
good = 0
for _ in range(page_num-1):
    soup = bs(driver.page_source, 'lxml')
    review_, good_ = get_review(soup)
    review += review_
    good += good_
    sleep(5)
    driver.find_element(By.XPATH, '//*[@id="reviewCardsSection"]/div[2]/div[1]/div/div/div[3]/button').click()
    sleep(5)
 
driver.close()

json_data = json.dumps(review, indent=4, ensure_ascii=False)  # indent參數用於縮排，讓JSON易讀性更高

# 寫入到檔案中
with open('hotel_review.json', 'w', encoding='utf8') as f:
    f.write(json_data)