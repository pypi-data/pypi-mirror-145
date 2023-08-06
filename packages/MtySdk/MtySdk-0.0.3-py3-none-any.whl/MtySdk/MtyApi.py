#coding=utf-8

from websocket import create_connection
import json
import time

class MtyAuth(object):
    """
    客户信息类
    """
    def __init__(self,user_name: str = "", password: str = ""):
        self.username=user_name;
        self.password=password;

class MtyApi(object):
    """
    API类
    """
    def __init__(self,auth: MtyAuth=""):
        """
        初始化通信管道
        :param auth:
        """
        self.ws = create_connection("ws://192.168.0.114:9999/mtyj/regres/%s/%s/" %(auth.username,auth.password))
        createresult = self.ws.recv()
        print(createresult)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    def is_having(self):
        """
        队列是否还有数据
        :return:
        """
        param = {
            'function': 'ishaving'
        }
        self.ws.send(json.dumps(param))
        result = self.ws.recv()
        result = json.loads(result)
        if (result['code'] == 200):
            return result['result']

    def query_math(self,name: str,starttime: str=None , endtime: str=None):
        """
        # 申请消费队列的消息
        ;param name:         名称
        :param starttime:   开始时间
        :param endtime:     结束时间
        :return:
        """
        param={
            'function':'registerserver',
            'name':name,
            'startDate':starttime,
            'endData':endtime
        }
        self.ws.send(json.dumps(param))
        result = self.ws.recv()
        result = json.loads(result)
        if (result['code'] == 200):
            result['name']=name
            return result

        self.close();
        return None;

    def get_math(self,math):

        if math is None: return;

        """
        队列消费数据
        :param order:
        :return:
        """
        param = {
            'function': 'queryqueue',
            'name':math['name']
        }
        self.ws.send(json.dumps(param))
        result = self.ws.recv()
        result = json.loads(result)
        return result;

    def close(self):
        self.ws.close();