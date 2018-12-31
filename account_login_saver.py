import json

def account_saver_tool():

    try:
        with open ("account_info.json", "r") as f:
            account_info = json.load(f)
        
        return account_info

    except OSError:
        print("There's no info of your NTU-ceiba account")
        account = input("Plz key in your account: ")
        passcode = input("Plz key in your passcode: ")
        info = {"account" : account, "passcode": passcode}
        
        with open ("account_info.json", "w") as f:
            json.dump(info, f, ensure_ascii = 0)

        print("we've already remembered yor account!")
        
        with open ("account_info.json", "r") as f:
            account_info = json.load(f)

        return account_info