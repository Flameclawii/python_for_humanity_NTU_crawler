期末專案構想：

名稱：NTU_ceiba_update_imformer

內容：
    能夠行檢查ntu ceiba上發生的更新，並且依照類別通知使用者
    
    支援的內容有：
        內容會照不同的科目大致有以下幾種分類：
            (1)成績更新通知
            (2)公布欄更新通知
            (3)作業繳交期限通知
            (4)其餘更新通知
    使用的方法為背景執行，讓使用者能夠設定定期檢查的時間，
    這樣一來大家就不用常常打開Ceiba在那邊檢查，
    作業是不是快到期，或是有沒有什麼消息沒有接收到，更不用整天提心吊膽成績公佈了沒，
    
    是不是很心動啊，心動不如馬上行動，就是現在，開放大家斗內，你的支持是我開發的最大動力（Ｘ

==================

## 目的/功能說明（約500字即可）

各位台大的少年少女們，一定都對ntu ceiba又愛又恨。
一方面ceiba算是台大提供的一個很方便的平台，但另一方面，ntu ceiba卻又有許多的不便，
這個程式會有以下幾項主要目的，以及其他還在思考中的想法：

(1)主動通知使用者ceiba上面有更新，以及其更新的科目及項目，目前更新的項目分類方式暫定沿用ceiba上左邊按鈕。

(2)主動通知即將到期的待繳交作業

(3)主動通知ceiba上的成績公布

(4)作業上傳成功通知，避免有時候作業沒傳成功，發生悲劇


## 你覺得可能會遇到的困難，請盡量清楚地條列敘述。

(1)涉及登入、多頁面的爬蟲技術

(2)主動通知的形式，不同形式會影響程式運作的方式，目前想到的方法有背景執行、和信件提醒，實際的方法還沒想好
    (a) 如果是背景執行會太耗資源
    
    (b) 如果是信件寄送會要考慮如何送出信件，目前還沒有想法，會再繼爬文

## 如何達成此專案的功能
1. 輸入介面
    (1)暫定使用純文字介面，使用者初次使用時需輸入自己的 ntu ceiba 帳號密碼，來滿足後面需要登入的爬蟲帳號密碼
    (2)其他還有例如 主動停止程式 或是 主動檢查更新了沒 這兩個還在想要怎麼做，但目前排在最後面，打算等主要程式結束，再來完成這部分

2. 爬蟲

    從 ceiba 上面爬資料下來，主要目前待處理的問題為：
        (1) 多頁面的爬蟲
        (2) 需要登入的爬蟲
    
    基本上這部分問題不大，網路上有很多教程，目前正進行中，
    其中目前我正在處理 Configure Chromedriver for Selenium webdriver on MAC and Window 的部分：(也就是判別不同os，讓他們都適用)
        這個網址中有我正在處理的方式：https://www.youtube.com/watch?v=S-h56366d98

3. 資料儲存

    目前想到要存兩種東西：
        (1)網頁的hash值，用在後面"資料比對"的部分去確定後面網頁有沒有變動
        (2)分 dict 跟 list 的方式去存各項內容，但是這樣網頁內容一多很容易造成空間複雜度太大，還在找套件來解決這件事

4. 資料比對

    目前想到的方式是：
        (1)先比對網頁的hash值，若hash一樣就不比對
        (2)若發現hash值不同，再去比對內容，找確切不同的地方，然後分類以通知使用者，改變的是哪些項目、或是成績是否公布、或剛剛上傳的作業是否有上傳成功
    
5. 通知使用者

    背景執行：
        目前想到的方法是使用 daemon 在客戶端電腦內背景執行，然後每一段時間間隔對 ntu ceiba 爬一次，儲存資料，比對內容，如果內容有改變就通知使用者

    
## 實作時間表

### W14 12/12  Checkpoint 1

* 寫出爬蟲自動登入、抓取部分

    使用者可透過文字輸入帳號密碼。程式會主動登入ntu ceiba並且抓取網頁內容。

    在我的專案中分成數個.py檔案，每個.py檔案分別處理不同的功能，要使用其他功能時再呼叫其他檔案，這樣會把檔案處理的比較乾淨。
    這週的進度內容為，完成爬蟲自動登入並且抓取網頁內容的部分，也就是專案其中的crawl.py：
    
    目前完成的部分為：
    def login_main() :處理自動登入的部分，這裡採用selenium來完成自動登入，並且能夠隱藏瀏覽器在背景執行。
    def crawl_web(driver) :分成多個分頁爬取網頁內容，並解決遇到frame會爬不到內容的部分

    本週進度要完成上述2個函式中爬取網頁的function，目前還在微調內容。
    下面是部分程式內容。但所有真正的程式檔案存取、分析工作將會在之後的checkpoints完成。

```python
def login_main() : 
    """
    account = input("請輸入Ceiba帳號：")
    passcode = input("請輸入Ceiba密碼：")

    options = webdriver.ChromeOptions() #to hide the browser
    options.add_argument("headless")

    chromedriver = "./chromedriver" #open a browser
    driver = webdriver.Chrome(executable_path = chromedriver)#, chrome_options = options)
    driver.get('https://ceiba.ntu.edu.tw/')

    login_click = driver.find_element_by_xpath("//*[@id=\"obj1\"]/form/p/input")
    login_click.click()

    username = driver.find_element_by_xpath("//*[@id=\"myTable\"]/td/input")
    password = driver.find_element_by_xpath("//*[@id=\"myTable2\"]/td/input")

    username.clear()    #to confirm there's no value in the input column
    password.clear()

    username.send_keys(account) 
    password.send_keys(passcode)

    login_click = driver.find_element_by_xpath("//*[@id=\"content\"]/form/table/tbody/tr[3]/td[2]/input")
    login_click.click()
    
    
    current_url = driver.current_url
    if (current_url != "https://ceiba.ntu.edu.tw/student/index.php"):
        print ("帳號密碼錯誤！")
    elif (current_url == "https://ceiba.ntu.edu.tw/student/index.php"):
        print ("登入成功！")
        crawl_web(driver)
    """

def crawl_web(driver) :
    """
    current_url = driver.current_url

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    class_link = re.findall("<a.+\"(https://ceiba.ntu.edu.tw.+)\" .+\".+?>", str(soup)) #待修正：不用正規 用bs4
    

    for obj in class_link:
        
        newpage = driver.get(obj)

        driver.switch_to.frame("Main")
        driver.switch_to.frame("leftFrame")
        
        page_html = driver.page_source
        page_soup = BeautifulSoup(page_html, "html.parser")
        print(page_soup)
        current_url = driver.current_url
        
        #抓到 frame 裡面

        '''
        page_class_link_to_be_replace = re.findall(".+fun=(.+)&.+", current_url)
        
        pages = []

        driver.switch_to.frame("mainFrame")
        page_contain_html = driver.page_source
        page_contain_pasoup = BeautifulSoup(html, "html.parser")


        print (soup)'''
        break
    """
```

### W15 12/19  Checkpoint 2

* 完成資料儲存、讀取與比對

    儲存檔案：會另外開一個.py來處理這部分的問題
    比對檔案：會和儲存檔案function寫在同一個.py檔


```python
    def load_data_from_file(file_path):
        pass  # function to be implemented
        
    def save_data_to_file(file_path):
        pass  # function to be implemented
    
    def file_compare():
        pass  # function to be implemented

```

* 完成自動在背景執行

    使用工作排程讓客戶端本身能夠定時自動執行這整個程式，來達到能夠定期檢查ntu ceiba是否有所更新

```python
    def work_in_background (ev_dict, ev_info):
        pass #後面會寫
```

### W16 12/26  Checkpoint 3

* 優化輸入介面、完成使用者通知的部分

    內容正在構想，稍後會補上

## W17 01/02  口頭報告 / beta release

* 測試程式功能

* 調整其他程式小問題

## 未來開發計畫

* 待主程式完成再來規劃

    

