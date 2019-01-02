import json

print("你可以在下面開始重設您的帳號密碼\n")
account = input("請鍵入您的帳號: ")
passcode = input("請鍵入您的密碼: ")
print ("\n")

info = {"account" : account, "passcode": passcode}

with open ("account_info.json", "w+") as f:
            json.dump(info, f, ensure_ascii = 0)

print ("密碼更改成功 系統將為您紀錄下帳號密碼")
print ("此次修改後 您仍可手動更改您的帳號密碼")