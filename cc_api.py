import base64
import json
import logging
import time
from datetime import datetime

from config import APP_CODE as app_code, SECRET_KEY as app_secret
from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from blueapps.utils.logger import logger



class CC_API:
    def __init__(self,username):
        self.bk_token = ''
        self.client = get_client_by_user(username)

    def reload(self, bk_token, request):
        self.bk_token = bk_token
        self.client = get_client_by_request(request)


    def search_business(self, condition={}):
        """
        查询业务
        :param condition:
        :return:
        """
        kwargs = {
            "bk_token": self.bk_token,
            "fields": [
                "bk_biz_id",
                "bk_biz_name"
            ],
            "condition": condition
        }
        data = self.client.cc.search_business(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['info']
        else:
            logger.warning(f"{get_now_time()} 查询业务失败：{data['message']} 接口名称(search_business) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def list_biz_hosts(self, bk_biz_id: int, bk_obj_id, bk_inst_ids=[]):
        """
        查询业务下主机
        """

        kwargs = {
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "page": {
                "start": 0,
                "limit": 500,
                "sort": "bk_host_id"
            },
            f"bk_{bk_obj_id}_ids": bk_inst_ids,
        }
        data = self.client.cc.list_biz_hosts(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result["result"] = data['result']
            result["data"] = data['data']['info']
        else:
            logger.warning(f"{get_now_time()} 获取业务下主机失败：{data['message']} 接口名称(list_biz_hosts) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def search_host(self, bk_biz_id: int, bk_obj_id, bk_inst_id: int):
        """
        查询主机
        :param bk_biz_id:
        :param bk_obj_id:
        :param bk_inst_id:
        :return:
        """
        kwargs = {
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "condition": [
                {
                    "bk_obj_id": bk_obj_id,
                    "fields": [],
                    "condition": [
                        {
                            "field": f"bk_{bk_obj_id}_id",
                            "operator": "$eq",
                            "value": bk_inst_id
                        }
                    ]
                }
            ]
        }
        data = self.client.cc.search_host(kwargs)
        result = {'result': False, 'message': 'Nothing', 'data': []}

        if data.get('result', False):
            result['result'] = data['result']
            for i in data['data']['info']:
                result['data'].append(i['host'])
        else:
            logger.warning(f"{get_now_time()} 查询主机列表失败：{data['message']} 接口名称(search_host) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']
        return result

    def search_biz_inst_topo(self, bk_biz_id: int):
        """
        查询业务下拓扑
        :param bk_biz_id:
        :return:
        """
        kwargs = {
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id
        }
        data = self.client.cc.search_biz_inst_topo(kwargs)
        result = {"result": False, "message": "nothing", "data": []}
        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = [make_topo(data['data'])]
        else:
            logger.warning(f"{get_now_time()} 获取业务实例拓扑失败：{data['message']} 接口名称(search_biz_inst_topo) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']
        return result

    def search_set(self, bk_biz_id: int, condition={}):
        """
        查询集群
        :param bk_biz_id:
        :param condition:
        :return:
        """
        kwargs = {
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "fields": [
                "bk_set_name",
                "bk_set_id"
            ],
            "condition": condition,
        }
        data = self.client.cc.search_set(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result["result"] = data['result']
            result['data'] = data['data']['info']
        else:
            logger.warning(f"{get_now_time()} 获取集群失败：{data['message']} 接口名称(search_set) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']
        return result

    def search_module(self, bk_biz_id: int, bk_set_id, condition={}):
        """
        查询模块
        :param bk_biz_id:
        :param bk_set_id:
        :param condition:
        :return:
        """
        kwargs = {
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_set_id": bk_set_id,
            "fields": [
                "bk_biz_id",
                "bk_set_id",
                "bk_module_id",
                "bk_module_name",
            ],
            "condition": condition,
            "page": {
                "start": 0,
                "limit": 500,
                "sort": "create_time"
            }
        }
        data = self.client.cc.search_module(kwargs)
        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result["result"] = data['result']
            result['data'] = data['data']['info']
        else:
            logger.warning(f"{get_now_time()} 获取模块失败：{data['message']} 接口名称(search_module) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']
        return result

    def find_host_by_module(self, bk_biz_id: int, bk_module_id):
        """
        获取模块下主机
        :param bk_biz_id:
        :param bk_module_id:
        :return:
        """
        kwargs = {
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_module_ids": [bk_module_id],
        }
        data = self.client.cc.find_host_by_module(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result["result"] = data['result']
            for i in data['data']['info']:
                result['data'].append(i['host'])
        else:
            logger.warning(f"{get_now_time()} 获取模块下主机失败：{data['message']} 接口名称(find_host_by_module) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']
        return result


cc_api = CC_API("liujiqing")

def save_json(filename, data):
    with open(f"{filename}.json", "w", encoding="utf-8")as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))


def make_topo(data):
    for topo in data:
        chiled = []

        if topo['child']:
            for i in topo['child']:
                chiled.append(make_topo([i]))

            return {"bk_obj_name": topo["bk_obj_name"],
                    "bk_obj_id": topo["bk_obj_id"],
                    "id": topo['bk_inst_id'],
                    "name": topo['bk_inst_name'],
                    "title": topo["bk_inst_name"],
                    "expanded": True,
                    "children": chiled,
                    }
        else:
            return {"bk_obj_name": topo["bk_obj_name"], "bk_obj_id": topo["bk_obj_id"], "id": topo['bk_inst_id'],
                    "name": topo['bk_inst_name'], "title": topo["bk_inst_name"]}


def make_time(time_str):
    return time_str[:time_str.rfind("+") - 1]

def get_now_time():
    return datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")