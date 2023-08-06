# -*- coding: utf-8 -*-

import requests
import json
import time

class HEADER(object):
    __headers = {}

    def init(self, header):
        if not self.__headers:
            self.__headers = header
        return self

    def add(self, key, val):
        self.__headers[key] = val
        return self.__value()

    def delete(self, name):
        self.__headers.pop(name)
        return self.__value()

    def clear(self):
        self.__headers = None
        return self.__value()

    def __value(self):
        return self.to_string(self.__headers)
     
    def to_string(self, json_dict):
        return json.dumps(json_dict)

    def update(self, json):
        for key, val in json:
            self.__headers[key]=val
        return self.__value()

    def get_headers(self):
        return self.__headers
    pass

class COOKIES(object):
    """ 初始化 key_vals_str """
    """ 维护 key_vals_json """
    """ 呈现使用 key_vals_str """

    key_vals_str=None
    key_vals_json={}

    def length(self):
        return len(self.key_vals_json)

    def init(self, cookie):
        if not self.key_vals_str:
            self.key_vals_str = cookie
        self.key_vals_json = self.to_json(self.key_vals_str)
        self.__value()
        return self

    def init_json(self, key_vals_json):
        self.key_vals_json = key_vals_json
        self.__value()
        return self

    def add(self, key, val):
        key = key.strip()
        self.key_vals_json[key]=val
        return self.__value()

    def delete(self, name):
        self.key_vals_json.pop(name)
        return self.__value()

    def clear(self):
        self.key_vals_json = None
        return self.__value()

    def __value(self):
        if None ==self.key_vals_json:
            self.key_vals_str =""
            return self.key_vals_str
        self.key_vals_str = self.to_string(self.key_vals_json)
        return self.key_vals_str
     
    def to_string(self, key_vals_json_tmp):
        tmp_string = ""
        if not json:
            return tmp_string
        for key, val in key_vals_json_tmp.items():
            tmp_string = tmp_string + key + "=" + val +";"
        return tmp_string

    def to_json(self, key_vals_str_tmp):
        key_vals_json_tmp={}
        key_val_list = key_vals_str_tmp.split(";")
        for key_val in key_val_list:
            co_list = key_val.split("=")
            if len(co_list) >1:
                key_tmp = co_list[0].strip()
                val_tmp = co_list[1].strip()
                if key_tmp: 
                    key_vals_json_tmp[key_tmp]=val_tmp
            elif len(co_list) >0:
                key_tmp = co_list[0].strip()
                if key_tmp: 
                    key_vals_json_tmp[key_tmp]=""
        return key_vals_json_tmp

    def update_json(self, key_vals_json_new):
        for key, val in key_vals_json_new:
            key = key.strip()
            self.key_vals_json[key]=val
        return self.__value()

    def update_str(self, key_vals_str_new):
        key_vals_json_new_tmp = self.to_json(key_vals_str_new)
        for key, val in key_vals_json_new_tmp.items():
            self.key_vals_json[key]=val
        return self.__value()

    def cookie(self):
        return self.__value()

    def cookie_show_json(self):
        return self.to_json(self.key_vals_str)

class ParamTool(object):
    __params = {} # inner data dict
    __params_dict = {} # dict: {"name":"xiaoming","age":10}
    __params_dictstr = "" # dict_string: """ {"name":"xiaoming","age":10} """
    __params_keystr = "" # key_value_string: """ {"name":"xiaoming","age":10} """

    def init_dict(self, p_dict):
        params = p_dict
        if isinstance(params, dict):
            self.__params_dict = params
            self.__params = self.__params_dict
            self.sync()
            return self
        raise Exception("[ERROR] init param type is not dict, e.g.: {\"name\":\"xiaoming\",\"age\":10}") 

    def init_dictstr(self, p_dictstr):
        params = p_dictstr.strip()
        if isinstance(params, str):
            if params.startswith("{") and params.endswith("}"):
                self.__params_dictstr = params
                self.__params = self.from_dictstr(params) 
                self.sync()
                return self
        raise Exception("[ERROR] init param type is not dict, e.g.: \"\"\"{\"name\":\"xiaoming\",\"age\":10}\"\"\"") 

    def init_keystr(self, p_keystr):
        params = p_keystr.strip()
        self.__params_keystr = params
        self.__params = self.from_keystr(params) 
        self.sync()
        return self

    def sync(self):
        self.__params_dict = self.to_dict()
        self.__params_dictstr = self.to_dictstr()
        self.__params_keystr = self.to_keystr()
        return self

    def to_dict(self):
        return self.__params
    def to_dictstr(self):
        return json.dumps(self.__params)
    def to_keystr(self):
        tmp_str = ""
        # print(self.__params)
        for key, val in self.__params.items():
            # print( key, val)
            if val is None : val = "null"
            val = str(val)
            tmp_str = tmp_str + key + "=" + val
            tmp_str = tmp_str + "&"
        if tmp_str.endswith("&"):
            tmp_str = tmp_str[:-1]
        return tmp_str

    def from_dictstr(self, p_dictstr):
        json_dict= {}
        tmp_dict = json.loads(p_dictstr)
        json_dict = tmp_dict
        return json_dict 
    def from_keystr(self, p_keystr):
        json_dict= {}
        params_list = p_keystr.split("&")
        for key_val in params_list:
            param_list = key_val.split("=")
            key = param_list[0]
            val = "" if len(param_list)<2 else param_list[1]
            json_dict[key] = val
        return json_dict        

    # self.sync()
    def add(self, key, val,sync=False):
        self.__params[key] = val
        if sync: self.sync()
        return self

    def update(self, p_dict,sync=False):
        for key, val in p_dict:
            self.__params[key]=val
        if sync: self.sync()
        return self

    def delete(self, key,sync=False):
        self.__params.pop(name)
        if sync: self.sync()
        return self

    def clear(self):
        self.__params = {}
        self.__params_dict = {}
        self.__params_dictstr = ""
        self.__params_keystr = ""
        return self

    def log(self):
        print(">> [INFO] {}".format( self.get_dictstr() ))
        return self

    def get_dict(self):
        return self.__params_dict

    def get_dictstr(self):
        return self.__params_dictstr

    def get_keystr(self):
        return self.__params_keystr
    pass

class WBrowser(object):
 
    __url = ""
    __data = None  # post请求数据类型， 
    __json = None  # post请求json类型， 输入类型dict
    __headers_dict = None  # 类型字典 dict
    __method = 'get'
    __params = None # url后面的参数, 

    __response = None
    __trans_time = 0
    __transaction_point_start = None


    def transaction(self):
        _transaction_point_end = time.time()
        if not self.__transaction_point_start:
            self.__transaction_point_start = time.time()
        self.__trans_time = _transaction_point_end - self.__transaction_point_start
        return self

    def transaction_point(self):
        self.__transaction_point_start = time.time()
        return self

    def show_trans_time(self):
        return self.__trans_time

        
    def __init__(self,headers=None):
        self.__headers_dict = headers
        pass

    def url(self, url):
        self.__url = url
        return self

    def method(self, method):
        self.__method = method
        return self

    def header(self, header_dict):
        self.__headers_dict = header_dict
        return self

    def get_header(self):
        return self.__headers_dict

    def body_json(self, json):
        self.__json = json
        return self

    def body_data(self, data):
        self.__data = data
        return self

    def body_params(self, params):
        self.__params = params
        return self

    def __visit(self):
        self.transaction_point()
        method_name = self.__method.lower()
        if self.__params: self.__url = "{}?{}".format(self.__url, self.__params) 
        # 注意request的 **kwargs可用于扩展
        if('get' == method_name):
            print(">> {} {}".format(self.__method, self.__url ))
            response = requests.get(self.__url, headers=self.__headers_dict)
            pass

        if('post' == method_name):
            # 
            print(">> {} {} {} {}".format(self.__method, self.__url,  self.__data,  self.__json ))
            
            response = requests.post(self.__url, 
            data=self.__data, 
            json=self.__json, 
            headers=self.__headers_dict)
            pass
        self.__response = response
        
        self.transaction()
        print("[INFO] visit at: {}\t[ Status:{}]".format(  time.strftime("%Y-%m-%d %X",time.localtime()), self.__response.status_code  ))
        return self.__response

    def visit(self):
        """
        :: request
        request.post(url, data=None, json=None, file=None, **kwargs):
        request.get(url, params=None, **kwargs):

        :: response
        response.status_code
        response.text
        response.encoding
        response.apparent_encoding
        response.content
        response.headers
        """

        return self.__visit()
    pass

browser = WBrowser()
