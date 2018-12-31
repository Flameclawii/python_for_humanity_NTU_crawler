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

from account_login_saver import *

import os

account_info = account_saver_tool()

def login_main() : 
    account = account_info["account"]
    passcode = account_info["passcode"]

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
    
    try:
        current_url = driver.current_url
    except BaseException:
        current_url = 0

    if (current_url == "https://ceiba.ntu.edu.tw/student/index.php"):
        crawl_web(driver)
    else:
        print ("帳號密碼錯誤 請在重開程式後 重新設定帳號密碼！")
        os.remove("./account_info.json")
        driver.close()
        exit()


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
            website_content_saver = {}

            for link in class_subproject_links:
                
                driver.get(link)
                
                try:
                    driver.switch_to.frame("mainFrame")
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")

                except BaseException:
                    pass

                    
                website_content_saver[nametag[number_of_nametag]] = str(soup)
                
                number_of_nametag += 1

                
            difference_class_content[str(matched_name)] = website_content_saver
            

            ###print (matched_name) 
            

    #print (difference_class_content)
    
    """read in and compare"""

    num_of_changes = 0

    try:
        with open('saver.json', 'r+') as f:
            all_content = json.load(f)
            #print(type(all_content))
        
        with open('saver.json', 'w+') as f:

            if (difference_class_content == all_content):##初步比較
                print("Nothing change!")
                pass

            else:##細部比較
                for classes_ in difference_class_content:
                    for content_tag in difference_class_content[classes_]:
                        try:
                            if (difference_class_content[classes_][content_tag] != all_content[classes_][content_tag]):
                                all_content[classes_][content_tag] = difference_class_content[classes_][content_tag]

                                print("The class : {} has something changed about {}".format(classes_, content_tag))
                                        
                                
                                num_of_changes += 1
                        except KeyError: ##原先tag不存在，更新的時候加了tag
                            all_content[classes_][content_tag] = difference_class_content[classes_][content_tag]

                            print("The class : {} had been added a new tag : {}".format(classes_, content_tag))
                                
                               
                            num_of_changes += 1
                
                json.dump(all_content, f, ensure_ascii = 0)
                        

    except OSError:
        with open('saver.json', 'w') as f:
            json.dump(difference_class_content, f, ensure_ascii = 0)
            print("There's no database now, yet never mind , we make a now one for you!")

    if (num_of_changes != 0):
        print ("There' {} change in this time update!".format(num_of_changes))
    
    driver.close()
        
"""
待辦：

1. background working
2. 手動更改ceiba account
3. improve user interface 
4. pip install ?

"""

login_main()