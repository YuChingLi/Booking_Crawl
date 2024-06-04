from bs4 import BeautifulSoup as bs
import requests
import json
from emoji import demojize as de

base_url = 'https://www.booking.com'
#start_url = 'https://www.booking.com/reviews/tw/city/t-ai-pei.zh-tw.html' #測試用
start_url = 'https://www.booking.com/reviews'

#取得主頁面個別飯店評論網頁網址
def get_url(soup):
    url_all = soup.find_all('li', class_='rlp-main-hotel-review__review_link')
    url = []
    for _ in url_all:
        url.append(base_url + _.find('a')['href'])
    return url

'''
取得要爬的下個頁面
取得飯店頁面，好評:本頁往後取，負評:本頁往前取
取得評論頁面，本頁往後取
'''
def get_next_url(soup, mode):
    if mode == 'next':
        page = soup.find('a', class_='rlp-main-pagination__btn-txt--next')
    elif mode == 'previous':
        page = soup.find('a', class_='rlp-main-pagination__btn-txt--prev')
    elif mode == 'review':
        page = soup.find('a', id = 'review_next_page_link')
    elif mode == 'last':
        page = soup.find_all('a', class_='rlp-main-pagination__btn-txt')[-1]
    return base_url + page['href']
    
#取得評論
def get_review(url, status):
    r = requests.get(url)
    review = {'status':[], 'review':[]}
    control_state = True
    
    while control_state:
        if r.status_code == requests.codes.ok:
            r.encoding = "utf8"
            soup = bs(r.text, 'lxml')
            review_container = soup.find_all('div', class_='review_item_review')
            for review_li in review_container:
                check = review_li.find('p', class_='review_none')
                if check:
                    control_state = False
                    break
                score = eval(review_li.find('span', class_='review-score-badge').text.strip())
                
                if status == 'pos':
                    review_pos = review_li.find('p', class_='review_pos')
                    if score > 7 and review_pos:
                            review['review'].append(de(review_pos.text.strip()))
                            review['status'].append('good')
                elif status == 'neg':
                    review_neg = review_li.find('p', class_='review_neg')
                    if score < 8  and review_neg:
                            review['review'].append(de(review_neg.text.strip()))
                            review['status'].append('bad')
                else:
                    print('wrong argument')
                    control_state = False
            
            if not control_state:
                #print('Leave review page since having no review')
                break
            #取得下一頁評論
            try:
                url = get_next_url(soup, 'review')
                r = requests.get(url)
            except:
                #print('Last page')
                break
        else:
            print('Fail to get review page', url)
    return review

all_review = {'status':[], 'review':[]}
 
#取得正面評論
def crawl_pos(start_url, all_review):
    print('抓取正面評論') 
    print('請稍等') 
    r = requests.get(start_url)
    for page in range(1, 2):
        if r.status_code == requests.codes.ok:
            print('正在爬取 top%d 飯店評論' % (page*30))
            r.encoding = "utf8"
            soup = bs(r.text, 'lxml')
            url = get_url(soup)
            #取得各飯店評論
            for url_ in url:
                print(url_)
                temp = get_review(url_, 'pos')
                all_review['status'] += temp['status']
                all_review['review'] += temp['review']
            #爬取下一頁飯店資料
            next_url = get_next_url(soup, mode='next')
            print(next_url)
            r = requests.get(next_url)
        else:
            print('Fail to get hotel page')
     
#取得負面評論
def crawl_neg(start_url, all_review):
    print('抓取負面評論') 
    print('請稍等') 
    r = requests.get(start_url)
    r.encoding = "utf8"
    r = requests.get(get_next_url(bs(r.text, 'lxml'), 'last'))
    
    for page in range(1, 4):
        if r.status_code == requests.codes.ok:
            print('正在爬取倒數 top%d 飯店評論' % (page*30))
            r.encoding = "utf8"
            soup = bs(r.text, 'lxml')
            url = get_url(soup)
            #取得各飯店評論
            for url_ in url:
                print(url_)
                temp = get_review(url_, 'neg')
                all_review['status'] += temp['status']
                all_review['review'] += temp['review']
            #爬取下一頁飯店資料
            next_url = get_next_url(soup, mode='previous')
            print(next_url)
            r = requests.get(next_url)
        else:
            print('Fail to get hotel page')

#想要爬取的地區url
road_map = {
    "t-ai-pei":
        {'url': '/tw/city/t-ai-pei.zh-tw.html?'
         },
    "kao-hsiung":
        {'url':'/tw/city/kao-hsiung.zh-tw.html?'
         },
    "tai-chung":
        {'url': '/tw/city/tai-chung.zh-tw.html?'
         },
    "tainan":
        {'url': '/tw/city/tai-nan.zh-tw.html?'
         },
    "taoyuan":
        {'url': '/region/taoyuan.zh-tw.html?'
         },
    "pingtung":
        {'url': '/region/pingtung.zh-tw.html?'
         },
    "hualien":
        {'url': '/region/hualien.zh-tw.html'
         },
    "nantou":
        {'url': '/region/nantou.zh-tw.html'
         }
    }

#開始爬取    
for key in road_map.keys():
    print(key)
    print(start_url + road_map[key]['url'])
    crawl_pos(start_url + road_map[key]['url'], all_review)
    crawl_neg(start_url + road_map[key]['url'], all_review)

#儲存資料
json_data = json.dumps(all_review, indent=4, ensure_ascii=False)  # indent參數用於縮排，讓JSON易讀性更高

# 寫入到檔案中
with open('booking_crawl.json', 'w', encoding='utf8') as f:
    f.write(json_data)