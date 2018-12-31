import json

def account_saver_tool():

    try:
        with open ("account_info.json", "r") as f:
            account_info = json.load(f)
        
        return account_info

    except OSError:
        print("目前沒有您的 NTU-Ceiba 資料 請您為我們輸入您的資料\n")
        account = input("請鍵入您的帳號: ")
        passcode = input("請鍵入您的密碼: ")
        print ("\n")
        
        info = {"account" : account, "passcode": passcode}
        
        with open ("account_info.json", "w") as f:
            json.dump(info, f, ensure_ascii = 0)
        
        with open ("account_info.json", "r") as f:
            account_info = json.load(f)
        
        print ("若首次登入成功後 系統將自動為您紀錄下帳號密碼")
        print ("不過別擔心 您仍可在事後手動更改您的帳號密碼~")

        return account_info