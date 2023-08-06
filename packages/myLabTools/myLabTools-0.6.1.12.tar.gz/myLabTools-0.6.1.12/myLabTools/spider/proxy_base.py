import sys
import random
import requests
import json
import datetime
import time

def conpute_time(time_str):
    timeArray = time.strptime(time_str, r"%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

class Proxy_manager(object):
    """代理管理器

    Args:
        object (_type_): _description_
    """    
    def __init__(self,
        Proxy_Server_URL =  "http://http.tiqu.letecs.com",
        min_interval = 30,
        clear_ips = True
        ):
        """

        Args:
            Proxy_Server_URL (str, optional): 获取代理的地址. Defaults to "http://http.tiqu.letecs.com".
            min_interval (int, optional): 更新代理列表的最短时间间隔. Defaults to 30.
            clear_ips (bool, optional): 是否保存已经失效的代理. Defaults to True.
        """        
        self.min_interval = min_interval
        self.clear_ips = clear_ips
        time.sleep(random.randint(15,30))

        self.nowtime = datetime.datetime.now() # 本次抓取代理的时间
        # 两次抓取间隔不能太短,最短抓取间隔为10分钟即600秒
        self.request_proxy_from_server(Proxy_Server_URL)
        random.shuffle(self.ips)
        self.i = 0
    def check_status(self):
        """检查代理池的状态
        """        
        if self.ips is None:
            query_server_flag = True
        elif self.i >= len(self.ips):
            this_time = datetime.datetime.now()  # 当前抓取时间
            if ((this_time - self.nowtime).seconds) >= self.min_interval:
                query_server_flag = True
                self.nowtime = this_time
            else:
                query_server_flag = False
                # print("request proxy too fast ,sleep {} seconds".format(self.min_interval * 0.5))
                time.sleep(self.min_interval * 0.1)
                self.i = 0
        else:
            query_server_flag = False
        if query_server_flag :
            print("request proxy from server")
            for i in range(6):
                try:
                    self.request_proxy_from_server()
                    break
                except :
                    time.sleep(10)

            self.i = 0
    def get_next_proxy(self):
        """从代理池中获取下一个代理

        Returns:
            Dict: {'http': "http://"+ip,'https': "https://"+ip}
        """        
        self.check_status()
        ip = self.ips[self.i]
        self.i = self.i + 1
        return {'http': "http://"+ip,'https': "https://"+ip}

    def request_proxy_from_server(self,Proxy_Server_URL):
        """从代理管理服务器中获取新的代理列表

        Args:
            Proxy_Server_URL (str): 获取代理列表的请求地址
        """        
        payload = {}
        files = {}
        headers = {}

        try:
            response = requests.request("POST", Proxy_Server_URL, headers=headers, data=payload, files=files)
            ips = json.loads(response.text.encode('utf8'))
            if self.clear_ips:
                
                self.ips = []
                self.clear_ips = False
            else:
                # 过期的代理还可以尝试着复用
                self.clear_ips = True
                pass

            self.ips_time = {}

            for proxy_msg in ips["data"]:
                ip_port = "{}:{}".format(proxy_msg["ip"],proxy_msg["port"])
                self.ips_time[ip_port] = conpute_time(proxy_msg["expire_time"])
                self.ips.append(ip_port)
        except Exception as e:
            self.ips = []
            print("Error : request_proxy_from_server {}".format(e))
    
if __name__ == '__main__':
    pm = Proxy_manager()
    print(pm.get_next_proxy())