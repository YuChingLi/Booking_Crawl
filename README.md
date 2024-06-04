# Booking_Crawl
## 程式碼操作步驟
### 訓練模型
1 在任意 IDE 使用 booking_crawl.py 爬取資料，將輸出 booking_crawl.json  
2 將 booking_crawl.json 儲存至個人雲端硬碟  
3 在 Google Colab 開啟 model_training.ipynb  
4 「執行階段」->「變更執行階段類型」-> 選擇任意GPU  
5 「執行階段」->「全部執行」，將在雲端硬碟自動建立資料夾 outputs 儲存模型參數

### 資料分析
1. 在任意 IDE 打開 user_crawl.py，使用者輸入欲爬飯店的網址，將輸出 hotel_review.json
2. 將資料上傳到雲端硬碟
3. 在 Google Colab 開啟 data_analysis.ipynb
4. 「執行階段」->「變更執行階段類型」-> 選擇任意GPU
5. 「執行階段」->「全部執行」  
    將在畫面及雲端輸出兩張文字雲的圖，分別是模型分類好的好評文字雲及負評文字雲
6. 在文字反向篩選的功能中，使用者可以自行輸入文字雲上出現的關鍵字，反向搜索評論

**因目前技術上的關係，無否提供讀者模型參數，使得讀者能直接使用模型做資料分析，請給予本宅一些時間學習**
