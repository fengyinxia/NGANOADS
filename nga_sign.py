'''
cron: 0 1 * * * nga_sign.py
new Env('NGA自动签到');
'''

import requests
import json
import os,time

from io import StringIO

requests.packages.urllib3.disable_warnings()
sio = StringIO()


class Nga_signin:
    def __init__(self, num, uid, token):
        self.num = num
        self.url = 'https://ngabbs.com/nuke.php'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; NOH-AN00 Build/HUAWEINOH-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 Nga_Official/90021",
            "X-Requested-With": "gov.pianzong.androidnga",
            "X-USER-AGENT": "Nga_Official/90021(HUAWEI NOH-AN00;Android 10)"
        }
        self.uid = uid
        self.token = token

    def signin(self):
        data = {"access_token": self.token,
                "t": round(time.time()),
                "access_uid": self.uid,
                "app_id": "1010",
                "__act": "check_in",
                "__lib": "check_in",
                "__output": "12"
                }
          #N币
        data1 = {"access_token": self.token,
                "t": round(time.time()),
                "access_uid": self.uid,
                "app_id": "1010",
                "mid": "30",
                "__act": "checkin_count_add",
                "__lib": "mission",
                "__output": "11"
                }
                
        res = requests.post(self.url, headers=self.headers, data=data1, verify=False).content
      
        req = requests.post(self.url, headers=self.headers, data=data, verify=False).content
      
        return json.loads(req)
        
    def watchad(self):
        data = {"access_token": self.token,
                "t": round(time.time()),
                "access_uid": self.uid,
                "app_id": "1010",
                "__act": "video_view_task_counter_add_v2_for_adfree",
                "__lib": "mission",
                "__output": "11"
                }
        data1 = {"access_token": self.token,
                "t": round(time.time()),
                "access_uid": self.uid,
                "app_id": "1010",
                "__act": "video_view_task_counter_add_v2_for_adfree_sp1",
                "__lib": "mission",
                "__output": "11"
                }
        data2 = {"access_token": self.token,
                 "t": round(time.time()),
                 "access_uid": self.uid,
                 "app_id": "1010",
                 "__act": "video_view_task_counter_add_v2",
                 "__lib": "mission",
                 "__output": "11"
                 }
        for i in range(4):
         res = requests.post(self.url, headers=self.headers, data=data, verify=False)
         time.sleep(1)
         res2 = requests.post(self.url, headers=self.headers, data=data2, verify=False)
        for i in range(2):
         time.sleep(1)
         res1 = requests.post(self.url, headers=self.headers, data=data1, verify=False)
        return "已经看过了"

    def get_stat(self):
       
        data = {"access_token": self.token,
                "t": round(time.time()),
                "access_uid": self.uid,
                "sign": "",
                "app_id": "1010",
                "__act": "get_stat",
                "__lib": "check_in",
                "__output": "14"
                }
        
        res = requests.post(self.url, headers=self.headers, data=data, verify=False).content
  
        
        res = json.loads(res)
        result = res['result'][0]
        continued = result['continued']
        total = result['sum']
        return continued, total

    def get_user(self):
        data = {"access_token": self.token,
                "t": round(time.time()),
                "access_uid": self.uid,
                "uid": self.uid,
                "app_id": "1010"
                }
        req = requests.post("https://ngabbs.com/app_api.php?__lib=user&__act=detail&", headers=self.headers, data=data, verify=False).content
        adtimes= json.loads(req)['result']['adfree']
        timeArray = time.localtime(adtimes)
        adtimess = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
        username = json.loads(req)['result']['username']
        money = json.loads(req)['result']['money']
        fuckmoney = json.loads(req)['result']['fuck_money']
        return adtimess,username,money,fuckmoney

    def start(self):
        req = self.signin()
        try:
                continued, total = self.get_stat()
                adtime = self.watchad()
                adtimes,username,money,fuckmoney = self.get_user()
                print(f'账号{self.num}:当前已连续签到{continued}天，总共签到{total}天，{adtime}，目前免广告时间直到{adtimes}，拥有铜币{money}个，N币{fuckmoney}个')
        except Exception as result:
            print(str(result))


if __name__ == '__main__':
    uid = os.getenv('NGA_UID')
    token = os.getenv('NGA_TOKEN')
    if uid and token:
        uid = uid.split('&')
        token = token.split('&')
        if len(uid) != len(token):
            msg = "签到失败，UID和token个数不相等"
       
            raise Exception
        for i in range(len(uid)):
            n = Nga_signin(i + 1, uid[i], token[i])
            n.start()
