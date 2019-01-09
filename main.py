from datetime import datetime
import time
import os
from apscheduler.schedulers.blocking import BlockingScheduler

from account_login_saver import *
from crawl import *

scheduler = BlockingScheduler()# 


def status_judgement():
    with open ("program_status", "r") as f:
        status = f.read()

    if status == "1":
        pass

    else:
        scheduler.remove_all_jobs()
        scheduler.shutdown()#爆炸 
        

def shut_down():
    a = input("請問您是否確定要停止程式？(Y/N)")

    if a == "Y" or a == "y" :
        with open ("program_status", "w+") as f:
            f.write("0")
        
        print('程式停止囉!')
    
    elif a == "N" or a == "n" :
        print("沒事 沒事 考慮清楚還是可以關掉喔！")
        
    else:
        print("還敢亂輸入啊 就你最特別！")
        shut_down()


def work_in_bg():
    with open ("program_status", "w+") as f:
        f.write("1")

    scheduler.add_job(status_judgement, trigger = "interval", seconds = 2)#seconds = )
    login_main()
    scheduler.add_job(login_main, "interval", minutes = 10)
    
    scheduler.start()
    


#-----
def main_func():
    print("若要停用持續運行的程式 請另外執行程式並選功能2 來停止")
    work_or_not = input("請選擇您要的功能：\n(1) 啟動 NTU Ceiba update informer\
    \n(2) 停止當前背景運作的 NTU Ceiba update informer\n(3) 更改 NTU Ceiba 的帳號密碼\n")


    try:
        with open ("program_status", "r") as f:
            status = f.read()
    except OSError:
        with open ("program_status", "w") as f:
            f.write("0")
        with open ("program_status", "r") as f:
            status = f.read()


    if (work_or_not == "1" or work_or_not == "(1)"):
        if status == "0" :
            account_saver_tool()
            work_in_bg()
            
        
        elif status == "1":
            a = input("偵測到錯誤 請問你上次是否有直接關閉程式？(Y/N)")
            if a == "Y" or a == "y":
                with open ("program_status", "w+") as f:
                    f.write("0")
                print("已替您解決\n")
                main_func()
            if a == "N" or a == "n":
                print("程式正在運行中囉，若找不到正在運行的程式，可能您上次直接關閉程式，而非透過功能2關閉")


    elif (work_or_not == "2" or work_or_not == "(2)"):
        if status == "1":
            shut_down()

        elif status == "0":
            print("程式現在就沒有在運行喔～")
    
    elif (work_or_not == "3" or work_or_not == "(3)"):
        account_info_change()
    
    else:
        print("還敢亂輸入啊 就你最特別！")
        main_func()


main_func()
