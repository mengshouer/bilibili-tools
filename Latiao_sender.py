import requests, time, json

try:
    f= open("F:/bilibili/login/login-TV/output/LoginResult1.txt","r")  #cookies文件位置
except:
    print("file path error")


send_room_id = 5595553
send_uid = 3817291   #赠送的uid
tsleep = 0.2    #延迟(s)


s = requests.Session()
ua = "User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"

def extract_cookies(cookie):
    cookies = dict([l.split("=", 1) for l in cookie.split("; ")])
    return cookies

def sender():
    url = f"https://api.live.bilibili.com/gift/v2/live/bag_send"
    for i in f:
        cookie = i.strip()
        cookies_dict = extract_cookies(cookie)
        csrf = cookies_dict['bili_jct'][:-1]
        uid = cookies_dict['DedeUserID']
        #t = int(round(time.time()*1000))
        t = int(time.time())
        headers = {
            'Accept': "application/json, text/plain, */*",
            'Origin': "https://live.bilibili.com",
            'Referer': "https://live.bilibili.com/"+ str(send_room_id),
            "User-Agent": ua,
            "Cookie": cookie
            }
        bagurl = f"https://api.live.bilibili.com/xlive/web-room/v1/gift/bag_list"
        web = s.get(bagurl,headers=headers).text
        bagdata = json.loads(web)
        baglist = bagdata["data"]["list"]
        bag_num = int(len(baglist))
        for item in range(0, bag_num):
            print(baglist[item])
            if(baglist[item]["gift_name"] == "辣条"):
                bag_id = baglist[item]["bag_id"]
                gift_num = baglist[item]["gift_num"]
                data = {
                    'uid': uid,
                    'gift_id': 1,
                    'ruid': send_uid,
                    'gift_num': gift_num,
                    'bag_id': bag_id,
                    'platform': "pc",
                    'biz_code': "live",
                    'biz_id': send_room_id,
                    'rnd': t,
                    'storm_beat_id': 0,
                    'metadata' : "",
                    'price': 0,
                    'csrf_token': csrf,
                    'csrf': csrf
                        }
                #web = s.get(url,params=data,headers=headers)
                web = s.post(url,data=data,headers=headers).text
                senddata = json.loads(web)
                if(senddata["code"] == 0):
                    print("赠送", gift_num, "根辣条成功")
                time.sleep(tsleep)

if __name__ == "__main__":
    sender()
