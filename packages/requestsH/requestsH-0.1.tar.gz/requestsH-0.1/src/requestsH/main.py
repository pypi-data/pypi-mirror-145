import requests

headers = {
    "chrome_win": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/99.0.4844.84 Safari/537.36"},
    "chrome_mac": {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, "
                                 "like Gecko) Chrome/17.0.963.56 Safari/535.11"},
    "safari_ios": {"User-Agent": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) "
                                 "AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"},
    "safari_ipad": {"User-Agent": "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 ("
                                  "KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"},
    "android": {"User-Agent": "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 "
                              "(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"}
}


# 简化get方法的过程，该函数直接输出返回的html
def get(url, encoding=None, proxies=None, params=None, json=False, ua="chrome_win"):
    # 用户可以自行输入ua
    if type(ua) == str:
        header = headers[ua]
    else:
        header = ua
    # get请求
    response = requests.get(url, headers=header, proxies=proxies, params=params)
    # 判断输出格式,或设置编码，编码默认为None
    if json:
        result = response.json()
    elif encoding is None:
        result = response.content.decode()
    else:
        result = response.content.decode(encoding=encoding)
    return result


# 简化post方法的过程，该函数直接输出返回的html
def post(url, data=None, encoding=None, proxies=None, json=False, ua="chrome_win"):
    # 用户可以自行输入ua
    if type(ua) == str:
        header = headers[ua]
    else:
        header = ua
    # post请求
    response = requests.post(url, headers=header, data=data, proxies=proxies)
    # 判断输出格式,或设置编码，编码默认为None
    if json:
        result = response.json()
    elif encoding is None:
        result = response.content.decode()
    else:
        result = response.content.decode(encoding=encoding)
    return result
