from pyvirtualdisplay import Display

from selenium import webdriver
import selenium.webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import requests 
from bs4 import BeautifulSoup

import os
import re
import time
import json

import tkinter as tk
import tkinter.font as tkFont
from PIL import ImageTk
from PIL import Image
from itertools import count


class NotifyControl(tk.Tk):
    """control the pages, to let multiple pages appear in the same window"""

    def __init__(self):
        """Constructor
        show the login page first

        """
        tk.Tk.__init__(self)
        self.login = True
        self.update_dict = {}
        self.update_cat = []
        # get all updated categories in a list

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # put all frames in a dictionary
        self.frames = {}

        # create all windows
        
        page_name = WinInputUserPassword.__name__
        frame = WinInputUserPassword(parent=self.container, controller=self)
        
        # put the frame in the dictionary
        self.frames[page_name] = frame

        # put all of the pages in the same location;
        # the one on the top of the stacking order
        # will be the one that is visible.
        frame.grid(row=0, column=0, sticky="nsew")

        # Show the First Window, WinInputUserPassword
        #self.show_frame("WinNotification")
        self.show_frame("WinInputUserPassword")
        #self.show_frame("WinLoading")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class WinInputUserPassword(tk.Frame):
    """class for creating the UserPassword Window"""

    def __init__(self, parent, controller):
        """Constructor"""
        tk.Frame.__init__(self, parent)
        self.Controller = controller
        self.grid()
        self.createUserPassword()

    def createUserPassword(self):
        """create the UserPassword Window"""

        # font for the text:NTU-CEIPA
        font1 = tkFont.Font(size=46, family="手札體-繁")
        # font for the text:"使用上次登入的帳號"、"登入新帳號"、"登入"
        font2 = tkFont.Font(size=28, family="手札體-繁")
        # font for the text:"帳號："、"密碼"
        font3 = tkFont.Font(size=24, family="手札體-繁")

        # Color Hex code
        hex1_green = "#84C324"
        hex2_brown = "#AB8937"
        hex3_gray  = "#D3D3D3"
        hex4_white = "#FFFFFF"
        hex5_dark_gray = "#94856B"

        # green label at the top
        self.lblGreen = tk.Label(self, height=6, width=120, bg=hex1_green)
        self.lblGreen.grid(row=0, column=0, rowspan=4, columnspan=29)

        # brown label under the green label
        self.lblBrown = tk.Label(self, height=1, width=120, bg=hex2_brown)
        self.lblBrown.grid(row=5, column=0, rowspan=1, columnspan=29)

        # white background in the middle of the window
        self.lblWhite = tk.Label(self, height=29, width=1)
        self.lblWhite.grid(row=6, column=0, rowspan=16)

        # gray label at the bottom
        self.lblGray = tk.Label(self, height=3, width=120, bg=hex3_gray)
        self.lblGray.grid(row=21, column=0, rowspan=2, columnspan=29)

        # Text:NTU-CEIPA
        self.lblNTU = tk.Label(self, text="NTU-CEIPA", font=font1, fg="white", bg=hex1_green)
        self.lblNTU.grid(row=1, column=1, rowspan=2, columnspan=18, sticky=tk.W)

        # Text: 帳號
        self.var_account = tk.StringVar(self, value='')
        self.lblUser = tk.Label(self, text = "帳號：", font=font2, fg=hex5_dark_gray)
        self.lblUser.grid(row=13, column=4, sticky=tk.E)
        self.txtUser = tk.Entry(self, width=12, font=font2, bg=hex3_gray, textvariable=self.var_account)
        self.txtUser.grid (row=13, column=5, columnspan=10, sticky=tk.W)

        # Text: 密碼
        self.var_password = tk.StringVar(self, value='')
        self.lblPassword = tk.Label(self, text = "密碼：", font=font2, fg=hex5_dark_gray)
        self.lblPassword.grid(row=15, column=4, sticky=tk.E)
        self.txtPassword = tk.Entry(self, show="*", width=12, font=font2, bg=hex3_gray, textvariable=self.var_password)
        self.txtPassword.grid (row=15, column=5, columnspan=10, sticky=tk.W)

        # CheckBottom: "記住我"
        self.var1 = tk.BooleanVar()  # use .get() to get the value
        self.var1.set(False)
        self.checkRemeber = tk.Checkbutton(self, text='記住我', variable=self.var1, onvalue=1, offvalue=0, font=font2, fg=hex5_dark_gray, command=self.clickCheckboxRemember)    # 傳值原理類似於radiobutton部件
        self.checkRemeber.grid(row=16, column=5, columnspan=10, sticky=tk.W)

        # SignUp
        self.imageLogin = tk.PhotoImage(file = "./pics/sing_up.png")
        self.btnSignup = tk.Button(self, image = self.imageLogin, command = self.clickBtnSignup)
        self.btnSignup.grid(row=13, column=13, rowspan=3, sticky=tk.W)

        try:
            account_info = {}
            with open ("account_info.json", "r") as f:
                account_info = json.load(f)

            self.var_account.set(account_info["account"])
            self.var_password.set(account_info["passcode"])
            self.var1.set(True)
        except:
            pass

    def clickBtnSignup(self): # suppose to sign up and run python
        
        font3 = tkFont.Font(size=24, family="手札體-繁")

        user = self.txtUser.get()
        password = self.txtPassword.get()
        checkbox = self.clickCheckboxRemember()
        #print(checkbox)
        global sample        
        #sample.show_frame("WinLoading")


        result = login_main(user, password, checkbox, 0)  # login or not

        if result:
            
            diff_dict = login_main(user, password, checkbox, 1)  # to login 

            if checkbox: 
                account_info = {"account":user, "passcode":password}
                with open ("account_info.json", "w+") as f:
                    json.dump(account_info, f, ensure_ascii = 0)
          
            
            # 程式Load完之後會產生一個更新資訊的dictionary
            
            
            diff_dict = category_classify(diff_dict)
            sample.update_cat = list(diff_dict.keys())
        

            # create Notification Window
            name = WinNotification.__name__
            page = WinNotification(parent=sample.container, controller=sample, category=diff_dict)
            sample.frames[name] = page
            page.grid(row=0, column=0, sticky="nsew")

            # create Update Info Window for updated categories
            for cat in sample.update_cat:
                name = cat
                page = WinUpdateInfo(parent=sample.container, controller=sample, category=cat, course=diff_dict[cat])
                sample.frames[name] = page
                page.grid(row=0, column=0, sticky="nsew")

            # show the Notification Window
            sample.show_frame("WinNotification")
            
        else:

            sample.lblFail = tk.Label(self, text="帳號或密碼錯誤", height=1, width=15, font=font3, fg="#FF0000")
            sample.lblFail.grid(row=11, column=5, columnspan=15, sticky=tk.W)

            
    def clickCheckboxRemember(self):
        return self.var1.get()
        
        
        
class WinNotification(tk.Frame):
    """class for creating the Notification Window"""

    def __init__(self, parent, controller, category):
        """Constructor"""
        tk.Frame.__init__(self, parent)
        self.Controller = controller
        self.update_category = category
        self.all_category = ["課程內容", "學習成績", "投票區", "討論看板", "作業區", "資源共享", "公布欄"]
        self.grid()
        self.createBackground()
        self.createWidgets()

    def createBackground(self):
        """create the background of the Window"""
        # font for the text:NTU-CEIPA
        font1 = tkFont.Font(size=46, family="手札體-繁")
        # Color Hex code
        hex1_green = "#84C324"
        hex2_brown = "#AB8937"
        hex3_gray = "#D3D3D3"

        # green label at the top
        self.lblGreen = tk.Label(self, height=6, width=90, bg=hex1_green)
        self.lblGreen.grid(row=0, column=0, rowspan=4, columnspan=29)

        # brown label under the green label
        self.lblBrown = tk.Label(self, height=1, width=90, bg=hex2_brown)
        self.lblBrown.grid(row=5, column=0, rowspan=1, columnspan=29)

        # white background in the middle of the window
        self.lblWhite = tk.Label(self, height=29, width=90, bg="white")
        self.lblWhite.grid(row=6, column=0, rowspan=16, columnspan=29)

        # gray label at the bottom
        self.lblGray = tk.Label(self, height=3, width=90, bg=hex3_gray)
        self.lblGray.grid(row=21, column=0, rowspan=2, columnspan=29)

        # Text:NTU-CEIPA
        self.lblNTU = tk.Label(self, text="NTU-CEIPA", font=font1, fg="white", bg=hex1_green)
        self.lblNTU.grid(row=1, column=1, rowspan=2, columnspan=6, sticky=tk.W)

    def createWidgets(self):
        """create images in label widgets in the center of the window"""

        # save references for each image in a list
        self.images = []

        for cat in self.all_category:
            # if the category has been updated, then insert a Button with image
            if cat in self.update_category:
                if cat == "課程內容":
                    self.btn_insert_image("./pics/h_content.jpg", 13, 1, cat)
                elif cat == "學習成績":
                    self.btn_insert_image("./pics/h_score.jpg", 13, 5, cat)
                elif cat == "討論看板":
                    self.btn_insert_image("./pics/h_discuss.jpg", 13, 9, cat)
                elif cat == "資源共享":
                    self.btn_insert_image("./pics/h_resource.jpg", 13, 13, cat)
                elif cat == "作業區":
                    self.btn_insert_image("./pics/h_hw.jpg", 18, 3, cat)
                elif cat == "公布欄":
                    self.btn_insert_image("./pics/h_board.jpg", 18, 7, cat)
                elif cat == "投票區":
                    self.btn_insert_image("./pics/h_vote.jpg", 18, 11, cat)

            # if the category is NOT updated, then insert a Label with image
            else:
                if cat == "課程內容":
                    self.lbl_insert_image("./pics/empty_content.jpg", 13, 1)
                elif cat == "學習成績":
                    self.lbl_insert_image("./pics/empty_score.jpg", 13, 5)
                elif cat == "討論看板":
                    self.lbl_insert_image("./pics/empty_discuss.jpg", 13, 9)
                elif cat == "資源共享":
                    self.lbl_insert_image("./pics/empty_resource.jpg", 13, 13)
                elif cat == "作業區":
                    self.lbl_insert_image("./pics/empty_hw.jpg", 18, 3)
                elif cat == "公布欄":
                    self.lbl_insert_image("./pics/empty_board.jpg", 18, 7)
                elif cat == "投票區":
                    self.lbl_insert_image("./pics/empty_vote.jpg", 18, 11)

    def lbl_insert_image(self, file, row, col):
        """insert image in a Label"""
        self.imageContent = ImageTk.PhotoImage(Image.open(file).resize((160, 170)))
        self.lblContent = tk.Label(self, image=self.imageContent, padx=8)
        self.lblContent.grid(row=row, column=col, columnspan=4, sticky=tk.W + tk.E)
        self.images.append(self.imageContent)

    def btn_insert_image(self, file, row, col, page):
        """insert image in a Button"""
        self.imageContent = ImageTk.PhotoImage(Image.open(file).resize((160, 170)))
        self.btn = tk.Button(self, image=self.imageContent, padx=8, bd=0, command=lambda: self.Controller.show_frame(page))
        self.btn.grid(row=row, column=col, columnspan=4, sticky=tk.W + tk.E)
        self.images.append(self.imageContent)


class WinUpdateInfo(tk.Frame):
    """class for creating the windows of updated Information"""

    def __init__(self, parent, controller, category, course):
        """Constructor"""
        tk.Frame.__init__(self, parent)
        self.Controller = controller
        self.category = category  # a string that specify the category
        self.course = course  # a list that consist of courses that have been updated
        self.grid()
        self.createBackground()
        self.createWidgets()

    def createBackground(self):
        """create the background of the Window"""
        # font for the text:NTU-CEIPA
        font1 = tkFont.Font(size=46, family="手札體-繁")
        # Color Hex code
        hex1_green = "#84C324"
        hex2_brown = "#AB8937"
        hex3_gray = "#D3D3D3"

        # green label at the top
        self.lblGreen = tk.Label(self, height=6, width=90, bg=hex1_green)
        self.lblGreen.grid(row=0, column=0, rowspan=4, columnspan=29)

        # brown label under the green label
        self.lblBrown = tk.Label(self, height=1, width=90, bg=hex2_brown)
        self.lblBrown.grid(row=5, column=0, rowspan=1, columnspan=29)

        # white background in the middle of the window
        self.lblWhite = tk.Label(self, height=29, width=1)
        self.lblWhite.grid(row=6, column=0, rowspan=16)

        # gray label at the bottom
        self.lblGray = tk.Label(self, height=3, width=90, bg=hex3_gray)
        self.lblGray.grid(row=21, column=0, rowspan=2, columnspan=29)

        # Text:NTU-CEIPA
        self.lblNTU = tk.Label(self, text="NTU-CEIPA", font=font1, fg="white", bg=hex1_green)
        self.lblNTU.grid(row=1, column=1, rowspan=2, sticky=tk.W)

    def createWidgets(self):

        # save references for each image in a list
        self.images = []
        font1 = tkFont.Font(size=28, family="手札體-繁")

        # create the window based on its category
        if self.category == "課程內容":
            self.insert_title("./pics/title_content.JPG")
            self.insert_talk("./pics/talk_content.png")
        elif self.category == "學習成績":
            self.insert_title("./pics/title_score.JPG")
            self.insert_talk("./pics/talk_score.png")
        elif self.category == "討論看板":
            self.insert_title("./pics/title_discuss.JPG")
            self.insert_talk("./pics/talk_discuss.png")
        elif self.category == "資源共享":
            self.insert_title("./pics/title_resource.JPG")
            self.insert_talk("./pics/talk_resource.png")
        elif self.category == "作業區":
            self.insert_title("./pics/title_hw.JPG")
            self.insert_talk("./pics/talk_hw.png")
        elif self.category == "公布欄":
            self.insert_title("./pics/title_billboard.JPG")
            self.insert_talk("./pics/talk_board.png")
        elif self.category == "投票區":
            self.insert_title("./pics/title_vote.JPG")
            self.insert_talk("./pics/talk_vote.png")

        # Strings that will show in the middle of the window
        self.output = ""
        for c in self.course:
            self.output += "%s 更新囉！\n" % c

        # create the label in the middle of the window
        self.lblText = tk.Label(self, text=self.output, font=font1, height=5, width=20)
        self.lblText.grid(row=7, column=1, rowspan=12, columnspan=24, sticky=tk.E+tk.W+tk.S)

        # create Home button or back button
        self.imageContent = ImageTk.PhotoImage(Image.open("./pics/green_back.jpg").resize((105, 94)))
        self.btnHome = tk.Button(self, image=self.imageContent, command=self.click_btn)
        self.btnHome.grid(row=1, column=21, rowspan=2, columnspan=4, sticky=tk.E)
        self.images.append(self.imageContent)

    def insert_title(self, file):
        """create the title image in a label"""
        self.imageContent = ImageTk.PhotoImage(Image.open(file).resize((140, 55)))
        self.lblContent = tk.Label(self, image=self.imageContent, padx=20)
        self.lblContent.grid(row=6, column=1, columnspan=4, sticky=tk.W + tk.S)
        self.images.append(self.imageContent)

    def insert_talk(self, file):
        """create the image in the bottom of the window"""
        self.imageContent = ImageTk.PhotoImage(Image.open(file).resize((475, 90)))
        self.lblContent = tk.Label(self, image=self.imageContent)
        self.lblContent.grid(row=19, column=1, columnspan=25, sticky=tk.S)
        self.images.append(self.imageContent)

    def click_btn(self):
        """return to Notification Window"""
        self.Controller.show_frame("WinNotification")

'''
class ImageGIF(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)
'''
'''
class WinLoading(tk.Frame):
    """class for creating the Loading Window"""

    def __init__(self, parent):
        """Constructor"""
        tk.Frame.__init__(self, parent)
        self.grid()
        self.createBackground()

    def createBackground(self):
        """create the background of the Window"""
        # font for the text:NTU-CEIPA
        font1 = tkFont.Font(size=46, family="手札體-繁")
        # Color Hex code
        hex1_green = "#84C324"
        hex2_brown = "#AB8937"
        hex3_gray  = "#D3D3D3"
        hex4_white = "#FFFFFF"

        # green label at the top
        self.lblGreen = tk.Label(self, height=6, width=90, bg=hex1_green)
        self.lblGreen.grid(row=0, column=0, rowspan=4, columnspan=29)

        # brown label under the green label
        self.lblBrown = tk.Label(self, height=1, width=90, bg=hex2_brown)
        self.lblBrown.grid(row=5, column=0, rowspan=1, columnspan=29)

        # white background in the middle of the window
        self.lblWhite = tk.Label(self, height=25, width=90, bg=hex4_white)
        self.lblWhite.grid(row=6, column=0, rowspan=15, columnspan=29)

        #GIF:Loading
        self.lblLoading = ImageGIF(self, height=100, width=500, bg=hex4_white)
        self.lblLoading.load('./pics/loading.gif')
        self.lblLoading.grid(row=11, column=0, rowspan=5, columnspan=29)

        # gray label at the bottom
        self.lblGray = tk.Label(self, height=3, width=90, bg=hex3_gray)
        self.lblGray.grid(row=21, column=0, rowspan=2, columnspan=29)

        # Text:NTU-CEIPA
        self.lblNTU = tk.Label(self, text="NTU-CEIPA", font=font1, fg="white", bg=hex1_green)
        self.lblNTU.grid(row=1, column=1, rowspan=2, sticky=tk.W)
'''

def category_classify(dict_to_classify):
    transdict = {"syllabus":"課程內容",
                 "grade":"學習成績", 
                 "vote":"投票區", 
                 "board":"討論看板", 
                 "hw":"作業區", 
                 "share":"資源分享", 
                 "bulletin":"公布欄"}
    after_transdict = {}
    for category in dict_to_classify:
        if category in transdict.keys():
            after_transdict[transdict[category]] = dict_to_classify[category]
    
    return after_transdict


''' login part '''


def login_main(user, password, checkbox, modetype) :  # type 0 to examine login or not, type 1 to do crawl

    account = user
    passcode = password

    options = webdriver.ChromeOptions()  # to hide the browser
    options.add_argument("headless")

    chromedriver = "./chromedriver"  # open a browser
    driver = webdriver.Chrome(executable_path = chromedriver, options = options)
    driver.get('https://ceiba.ntu.edu.tw/')

    login_click = driver.find_element_by_xpath("//*[@id=\"obj1\"]/form/p/input")
    login_click.click()

    username = driver.find_element_by_xpath("//*[@id=\"myTable\"]/td/input")
    password = driver.find_element_by_xpath("//*[@id=\"myTable2\"]/td/input")

    username.clear()  # to confirm there's no value in the input column
    password.clear()

    username.send_keys(account) 
    password.send_keys(passcode)

    login_click = driver.find_element_by_xpath("//*[@id=\"content\"]/form/table/tbody/tr[3]/td[2]/input")
    login_click.click()

    if modetype == 0:
        try:
            current_url = driver.current_url
        except BaseException:
            current_url = 0

        driver.close()
        if (current_url == "https://ceiba.ntu.edu.tw/student/index.php"):    
            return True
        
        else:
            return False  # to revise
    
    elif modetype == 1:
        difference_class_content = crawl_web(driver)
        diff_dict = content_comparison( difference_class_content )  # difference content
        
        return diff_dict


''' crawler part '''


def left_tag_link_getter(driver, class_link):
    newpage = driver.get(class_link)

    # 抓到 frame 裡面 -----
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
            # to prepare the link -----

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
    class_links = re.findall("<a.+\"(https://ceiba.ntu.edu.tw.+)\" .+\".+?>", str(soup))  # 待修正：不用正規 用bs4
    
    # 科目名稱 和 網址爬完後 要拿來存取的容器 跟變數 設置
    difference_class_content = {}  # 等待存取

    for class_link in class_links:  # 一直被最後一個蓋過去
        
        # to decide whether or not let links, nametag, matched_name = left_tag_link_getter(driver, class_link)
        # in case that left_tag_link_getter return None
        
        test0, test1, test2 = left_tag_link_getter(driver, class_link)

        if (test0 == 0 and test1 == 0 and test2 == 0):
            pass
        else:
            class_subproject_links, nametag, matched_name = test0, test1, test2  # nametag 左邊標籤  # match_name 課程名稱

        # ----- #

            number_of_nametag = 0  # record the number of the nametag
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
    #print(difference_class_content)
    return difference_class_content
            ###print (matched_name) 
            

    #print (difference_class_content)


''' comparison part '''


def content_comparison(difference_class_content):
    #print(difference_class_content)
    temp_record_dict = {}
    try:
        with open('saver.json', 'r+') as f:
            all_content = json.load(f)
            #print(type(all_content))

        if (difference_class_content == all_content):  # 初步比較
            return temp_record_dict

        else:  # 細部比較
            for classes_ in difference_class_content:
                for content_tag in difference_class_content[classes_]:
                    try:
                        if (difference_class_content[classes_][content_tag] != all_content[classes_][content_tag]):
                            all_content[classes_][content_tag] = difference_class_content[classes_][content_tag]
                            try:
                                temp_record_dict[content_tag].append(classes_)
                            except KeyError:
                                temp_record_dict[content_tag] = [classes_, ]
                            #print(temp_record_dict, 1)
                            #print("The class : {} has something changed about {}".format(classes_, content_tag))
                    
                    except KeyError:  # 原先tag不存在，更新的時候加了tag
                        all_content[classes_][content_tag] = difference_class_content[classes_][content_tag]
                        try:
                            temp_record_dict[content_tag].append(classes_)
                        except KeyError:
                            temp_record_dict[content_tag] = [classes_, ]
                        #print(temp_record_dict, 2)
                        #print("The class : {} had been added a new tag : {}".format(classes_, content_tag))
                            

            with open('saver.json', 'w+') as f:
                json.dump(all_content, f, ensure_ascii = 0)

            return temp_record_dict
                        

    except OSError:  # there's no database now
        with open('saver.json', 'w') as f:
            json.dump(difference_class_content, f, ensure_ascii = 0)
            #print("There's no database now, yet never mind , we make a now one for you!")
        return temp_record_dict


''' main part '''


sample = NotifyControl()
sample.title("New Notifications!")
sample.geometry("766x575+360+150")
sample.mainloop()
