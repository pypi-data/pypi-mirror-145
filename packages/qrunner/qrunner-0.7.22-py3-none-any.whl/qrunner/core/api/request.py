# @Time    : 2022/2/22 9:35
# @Author  : kang.yang@qizhidao.com
# @File    : request.py
import requests
import allure
import json as json_util
from qrunner.utils.config import conf
from qrunner.utils.log import logger

IMG = ["jpg", "jpeg", "gif", "bmp", "webp"]


class ApiConfig:
    login_key = ['accessToken', 'signature']


def request(func):
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        print("\n")
        logger.info('-------------- Request -----------------[🚀]')
        try:
            url = list(args)[1]
        except IndexError:
            url = kwargs.get("url", "")
        m = func_name.upper()
        allure.dynamic.title(f'[{m}]{url}')
        allure.dynamic.feature(url.split('/')[1])
        base_url = conf.get_name('api', 'base_url')
        if (base_url is not None) and ("http" not in url):
            url = base_url + list(args)[1]

        img_file = False
        file_type = url.split(".")[-1]
        if file_type in IMG:
            img_file = True

        logger.debug("[method]: {m}      [url]: {u} \n".format(m=func_name.upper(), u=url))
        auth = kwargs.get("auth", "")
        headers = kwargs.pop("headers", {})
        conf_headers = conf.get_name('api', 'headers')
        conf_headers_dict = json_util.loads(conf_headers)
        login_status = kwargs.get('login', True)
        if conf_headers != 'None':
            if not login_status:
                for key in ApiConfig.login_key:
                    conf_headers_dict.pop(key)
            headers.update(conf_headers_dict)
            # print(headers)
        kwargs['headers'] = headers
        cookies = kwargs.get("cookies", "")
        params = kwargs.get("params", "")
        data = kwargs.get("data", "")
        json = kwargs.get("json", "")
        if auth != "":
            logger.debug(f"[auth]:\n {auth} \n")
        if headers != "":
            # logger.debug(type(headers))
            logger.debug(f"[headers]:\n {headers} \n")
        if cookies != "":
            logger.debug(f"[cookies]:\n {cookies} \n")
        if params != "":
            logger.debug(f"[params]:\n {params} \n")
        if data != "":
            logger.debug(f"[data]:\n {data} \n")
        if json != "":
            logger.debug(f"[json]:\n {json} \n")

        # running function
        r = func(*args, **kwargs)

        ResponseResult.status_code = r.status_code
        logger.info("-------------- Response ----------------")
        try:
            resp = r.json()
            logger.debug(f"[type]: json \n")
            logger.debug(f"[response]:\n {resp} \n")
            ResponseResult.response = resp
        except BaseException as msg:
            logger.debug("[warning]: {} \n".format(msg))
            if img_file is True:
                logger.debug("[type]: {}".format(file_type))
                ResponseResult.response = r.content
            else:
                logger.debug("[type]: text \n")
                logger.debug(f"[response]:\n {r.text} \n")
                ResponseResult.response = r.text

    return wrapper


class ResponseResult:
    status_code = 200
    response = None


class HttpRequest(object):

    # def http_req(self, url, method=None, params=None, login=True, **kwargs):
    #     if method == 'get':
    #         self.get(url, params=params, login=login, **kwargs)
    #     elif method == 'post':
    #         self.post(url, json=params, login=login, **kwargs)
    #     elif method == 'put':
    #         self.put(url, data=params, login=login, **kwargs)
    #     elif method == 'delete':
    #         self.delete(url, login=login, **kwargs)
    #     else:
    #         print(f'不支持的请求方式: {method}')

    @request
    def get(self, url, params=None, login=True, **kwargs):
        base_url = conf.get_name('api', 'base_url')
        if (base_url is not None) and ("http" not in url):
            url = base_url + url
        return requests.get(url, params=params, **kwargs)

    @request
    def post(self, url, data=None, json=None, login=True, **kwargs):
        base_url = conf.get_name('api', 'base_url')
        if (base_url is not None) and ("http" not in url):
            url = base_url + url
        return requests.post(url, data=data, json=json, **kwargs)

    @request
    def put(self, url, data=None, login=True, **kwargs):
        base_url = conf.get_name('api', 'base_url')
        if (base_url is not None) and ("http" not in url):
            url = base_url + url
        return requests.put(url, data=data, **kwargs)

    @request
    def delete(self, url, login=True, **kwargs):
        base_url = conf.get_name('api', 'base_url')
        if (base_url is not None) and ("http" not in url):
            url = base_url + url
        return requests.delete(url, **kwargs)

    @property
    def response(self):
        """
        Returns the result of the response
        :return: response
        """
        return ResponseResult.response

    @property
    def session(self):
        """
        A Requests session.
        """
        s = requests.Session()
        return s

    @staticmethod
    def request(method=None, url=None, headers=None, files=None, data=None,
                params=None, auth=None, cookies=None, hooks=None, json=None):
        """
        A user-created :class:`Request <Request>` object.
        """
        req = requests.Request(method, url, headers, files, data,
                               params, auth, cookies, hooks, json)
        return req
