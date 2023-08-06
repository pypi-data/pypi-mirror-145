import requests
from lxml import etree
from .proxy_base import Proxy_manager
from .logger_base import Logger
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
import os

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class SpiderBase():
    """爬虫的基础类
    """    
    def __init__(self,
                process_i = 0,
                log_dir = "./log",
                USE_PROXY = True,
                proxy:Proxy_manager = None,
                TIMEOUT = 2,
                TRY_MAX = 2):
        """构建一个爬虫实例

        Args:
            process_i (int, optional): 爬虫实例的id. Defaults to 0.
            log_dir (str, optional): 日志保存的文件夹. Defaults to "./log".
            USE_PROXY (bool, optional): 是否使用代理. Defaults to True.
            TIMEOUT (int, optional): 最大等待时间. Defaults to 2.
            TRY_MAX (int, optional): 最大重试次数. Defaults to 2.
        """        
        self.TRY_MAX = TRY_MAX
        self.TIMEOUT = TIMEOUT
        self.USE_PROXY = USE_PROXY
        T = time.strftime(r"%m月%d日 %H:%M")
        
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        log = Logger(filename = '{}/日志-{}_processor_{}.log'.format(log_dir,T,process_i), level='info')
        self.logger = log.logger
        self.proxy_manager = proxy
        if USE_PROXY:
            self.proxies = self.get_next_proxy()

    def get_next_proxy(self):
        """获取代理

        Returns:
            Dict: 代理， {'http': "http://"+ip,'https': "https://"+ip}
        """        
        proxy =  self.proxy_manager.get_next_proxy()
        
        return proxy

    def parse_html(
        self,
        url = "", 
        headers = 
            {'User-Agent':
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"}, 
        xpath_list=[],
        min_len = 100
        ):
        """获取网页代码  or 通过xpath获取指定的内容

        Args:
            url (str, optional): 访问的url. Defaults to "".
            headers (dict, optional): 请求头. Defaults to headers.
            xpath_list (list, optional): 解析网页中的目标内容. Defaults to [].
            min_len (int, optional): 网页的最小长度，小于这个长度就认为是获取失败了. Defaults to 100.

        Returns:
            _type_: 网页文本或 与xpath列表对应的内容的字典
        """   
             
        xpath_result = []
        for try_i in range(self.TRY_MAX):
            try:
                if self.USE_PROXY:
                    response = requests.get(url,
                    headers = headers,
                    proxies=self.proxies,
                    timeout = self.TIMEOUT, 
                    verify=False)
                    pass
                else:
                    response = requests.get(url, 
                    headers=headers,
                    timeout = self.TIMEOUT,
                    verify=False)

                if len(xpath_list) > 0:
                    tree = etree.HTML(response.text)
                    for xpath in xpath_list:
                        temp_result = tree.xpath(xpath)
                        if len(temp_result) == 0:
                            self.logger.error("SpiderBase：can not parse information from the url !, retry again.")
                        xpath_result.append(temp_result)
                    return xpath_result
                else:
                    if len(response.text) < min_len:
                        self.logger.error("SpiderBase：webpage length is too short !, retry again.")
                    if "404 Not Found" in response.text:
                        self.logger.error("SpiderBase：404 Not Found")
                    return response
            except Exception as e:
                self.logger.error(e)
                if self.USE_PROXY:
                    self.proxies = self.get_next_proxy()
                    self.logger.info("SpiderBase：chanege proxy")
                continue
        return None