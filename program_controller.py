from datetime import datetime
import time
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler


from hi import *

scheduler = BlockingScheduler()#BackgroundScheduler()

def status_judgement():
    with open ("program_status", "r") as f:
        status = f.read()

    if status == "0":
        scheduler.shutdown()#爆炸
        
        print('Exit The Job!')
        
    
    elif status == "1":
        pass
        

def shut_down():
    a = input("請問您是否確定要停止程式？(Y/N)")

    if a == "Y" or a == "y" :
        with open ("program_status", "w+") as f:
            f.write("0")
    
    elif a == "N" or a == "n" :
        print("沒事 沒事 考慮清楚還是可以關掉喔！")
        return 0
    else:
        print("還敢亂輸入啊 就你最特別！")
        shut_down()


def work_in_bg():
    

    with open ("program_status", "w+") as f:
        f.write("1")
    scheduler.add_job(status_judgement, id = 'status_judgement', trigger = "interval", seconds = 3)
    scheduler.add_job(hello, "interval", seconds = 3)#minute = 10)
    print (scheduler.get_job('status_judgement'))
    scheduler.start()
    


#-----
def main_func():
    work_or_not = input("請選擇您要的功能：\n(1) 啟動 NTU Ceiba update informer\
    \n(2) 停止當前背景運作的 NTU Ceiba update informer\n")


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
            work_in_bg()
            
        
        elif status == "1":
            print("程式正在執行中囉！ 目前不開放多重執行程式：）")

    elif (work_or_not == "2" or work_or_not == "(2)"):
        if status == "1":
            shut_down()

        elif status == "0":
            print("城市現在就沒有在運行喔～")

    else:
        print("還敢亂輸入啊 就你最特別！")



main_func()

