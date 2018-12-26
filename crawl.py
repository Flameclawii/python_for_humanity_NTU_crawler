from pyvirtualdisplay import Display

from selenium import webdriver
import selenium.webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import requests 
from bs4 import BeautifulSoup

import re

import time

import json

def login_main() : 
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


def left_tag_link_getter(driver, class_link):
    newpage = driver.get(class_link)

    #抓到 frame 裡面 -----
    try: 
        driver.switch_to.frame("Main")
        try:
            driver.switch_to.frame("leftFrame")
    # ----- #
            page_html = driver.page_source
            page_soup = BeautifulSoup(page_html, "html.parser")
            
            class_name = page_soup.find_all("title")
            matched_name = re.findall(r"<title>.+：(.+)</title>", str(class_name))
            matched_name = matched_name[0]
            #to prepare the link -----

            allpages = page_soup.find_all("a")
            
            match = re.findall(r"\('(\w+)?','(\w+)?'?\)", str(allpages))
            links = []
            nametag = []
            for parts_of_links in match:
                if (parts_of_links[0] != "logout"):
                    link = "https://ceiba.ntu.edu.tw/modules/index.php?csn={}&default_fun={}&current_lang=chinese"\
                    .format(parts_of_links[1], parts_of_links[0])

                    links.append(link) 
                    nametag.append(parts_of_links[0])
                else:
                    pass

            
            return links, nametag , matched_name
            # ----- #

        except BaseException:
            return 0, 0, 0
            pass

    except BaseException:
        return 0, 0, 0
        pass


def crawl_web(driver) :

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    class_links = re.findall("<a.+\"(https://ceiba.ntu.edu.tw.+)\" .+\".+?>", str(soup)) #待修正：不用正規 用bs4
    
    # 科目名稱 和 網址爬完後 要拿來存取的容器 跟變數 設置
    difference_class_content = {} # 等待存取

    website_content_saver = {}

    for class_link in class_links: ##一直被最後一個蓋過去
        
        # to decide whether or not let links, nametag, matched_name = left_tag_link_getter(driver, class_link)
        # in case that left_tag_link_getter return None
        
        test0, test1, test2 = left_tag_link_getter(driver, class_link)

        if (test0 == 0 and test1 == 0 and test2 == 0):
            pass
        else:
            class_subproject_links, nametag, matched_name = left_tag_link_getter(driver, class_link)##nametag 左邊標籤 ##match_name 課程名稱

        # ----- #
        
            
            number_of_nametag = 0 #record the number of the nametag

            for link in class_subproject_links:
                
                driver.get(link)
                
                try:
                    driver.switch_to.frame("mainFrame")
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    print("test00_frame")

                except BaseException:
                    pass

                    
                website_content_saver[nametag[number_of_nametag]] = str(soup)
                
                number_of_nametag += 1

                
            difference_class_content[str(matched_name)] = website_content_saver
            website_content_saver = {}

            print (matched_name)
    
            

            

    #print (difference_class_content)
    
    
    try:
        with open('saver.json', 'r+') as f:
            all_content = json.load(f)
            print(type(all_content))
            if (difference_class_content == all_content):
                print("Nothing change!")
                pass
            else: ##細部比較還沒做
                print("something change!")
                json.dump(difference_class_content, f, ensure_ascii = 0)

    except BaseException:
        with open('saver.json', 'w') as f:
            json.dump(difference_class_content, f, ensure_ascii = 0)

    
    #driver.close()
        



login_main()