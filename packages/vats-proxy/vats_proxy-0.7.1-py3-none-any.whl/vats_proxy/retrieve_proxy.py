#vats
import requests
from requests.exceptions import ProxyError
from fp.fp import FreeProxy


class ProxyManager:
    """ Simple ProxyManager Class, Returns array of proxies, each proxy is a dict, you can pop proxy from list
        You can initialize ProxyManager with ProxyManager(count=1), count must be 1 or greater.
        Written by #Vats

    :param count: int, how many proxies you want to get
    :type count: integer
    """
    def __init__(self, count, test_url="https://www.google.com"):
        self.count = count
        self.test_url = test_url
        self.proxies = []
        self.all_proxies = []
        if count == 1:
            self.proxies = self.get_one_proxy()
        elif count > 1:
            self.proxies = self.get_proxy_list(count)
        elif count <= 0:
            raise ValueError("count must be 1 or greater")
        # else:
        #     raise ValueError("You can initialize ProxyManager with ProxyManager(count=1) or ProxyManager(count=4)")
    def check_proxy(self, proxy):
        try:
            req = requests.get(self.test_url, proxies=proxy, timeout=5)
            if req.status_code == 200:
                return True
            else:
                return False
        except ProxyError:
            return False
        
    def get_proxy_list(self, count):
        """returns a list of proxies, each proxy is a dict, you can pop proxy from list"""
        proxies = FreeProxy().get_proxy_list()
        proxies_array = []
        forloop_counter = 0
        skip_check = None
        if len(proxies) < count:
            raise ValueError("There are not enough proxies. Proxy count: {}".format(len(proxies)))
        for proxy in proxies:
            if forloop_counter == count: # when desired count of proxies is reached break the for loop
                skip_check = True
            proxy_dict = {'http': "http://"+proxy}
            if skip_check:
                self.all_proxies.append(proxy_dict)
            else:
                check = self.check_proxy(proxy_dict)
                if check: # if proxy is working add it to the list
                    proxies_array.append(proxy_dict)
                    forloop_counter += 1
        return proxies_array

    def get_one_proxy(self):
        """ returns single proxy as dictionary, tries until finds working proxy"""
        while True:
            print("Running while loop till finding one working proxy")
            proxy = FreeProxy().get()
            proxy_dict = {'http': "http://"+proxy}
            check = self.check_proxy(proxy_dict)
            if check:
                return [proxy_dict]

    def request_proxy(self):
        """ returns single proxy as dictionary, tries until finds working proxy"""
        while True:
            try:
                proxy = self.all_proxies.pop()
            except IndexError:
                return [] # if there is no proxy left return empty list
            check = self.check_proxy(proxy)
            if check:
                return proxy
            