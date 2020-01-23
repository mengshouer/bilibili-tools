import requests, time, json

try:
    f= open("F:/bilibili/login/login-TV/output/LoginResult1.txt","r")  #cookies文件位置
except:
    print("file path error")

senduid = 3817291   #赠送的uid
tsleep = 0.2    #延迟(s)


s = requests.Session()
ua = "User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"

def extract_cookies(cookie):
    cookies = dict([l.split("=", 1) for l in cookie.split("; ")])
    return cookies

def main():
    url = "https://api.live.bilibili.com/xlive/web-room/v1/userRenewCard/send?"
    for i in f:
        cookie = i.strip()
        cookies_dict = extract_cookies(cookie)
        csrf = cookies_dict['bili_jct'][:-1]
        t = int(round(time.time()*1000))
        headers = {
            "Referer": "https://live.bilibili.com/1",
            "User-Agent": ua,
            "Cookie": cookie
            }
        bagurl = "https://api.live.bilibili.com/xlive/web-room/v1/gift/bag_list"
        web = s.get(bagurl,headers=headers).text
        carddata = json.loads(web)
        carddata = carddata["data"]
        cardlist = carddata["list"]
        card_record_id = 0
        for item in cardlist:
            for key in item:
                if(key == "card_record_id" and item[key] != 0):
                    card_record_id = item[key]
                    data = {
                            "card_record_id": card_record_id,
                            "recv_uid": senduid,
                            "num": "1",
                            "t": t
                            }
                    web = s.get(url,params=data,headers=headers)
                    #web = s.post(url,data=data,headers=headers)
                    print(web.text)
        if(card_record_id == 0):
            print("没有续期卡")
        time.sleep(tsleep)

if __name__ == "__main__":
    main()
