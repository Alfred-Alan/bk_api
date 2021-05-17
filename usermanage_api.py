import base64
import json
import time
from datetime import datetime
from config import APP_CODE as app_code, SECRET_KEY as app_secret
from blueking.component.shortcuts import get_client_by_request
from blueapps.utils.logger import logger


class UserManage_API:
    def __init__(self, bk_token, client):
        self.bk_token = bk_token
        self.client = client

    def reload(self, bk_token, request):
        self.bk_token = bk_token
        self.client = get_client_by_request(request)

    def list_departments(self, page=0, page_size=0, fields=None, lookup_field='', exact_lookups='', fuzzy_lookups=''):
        """
        获取部门列表
        :param page: int 	页码
        :param page_size: int 	每页结果数量
        :param fields: string 返回值字段, 例如"username,id"
        :param lookup_field: string  查找字段, 默认值为 'id'
        :param exact_lookups: string 精确查找内容列表, 例如"jack,pony" 需和lookup_field 搭配
        :param fuzzy_lookups: string 模糊查找内容列表, 例如"jack,pony" 需和lookup_field 搭配
        :return: result
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "lookup_field": lookup_field,
            "page": page,
            "page_size": page_size,
            "fields": fields,
            "exact_lookups": exact_lookups,
            "fuzzy_lookups": fuzzy_lookups
        }

        for param_key in list(kwargs.keys()):
            if not kwargs[param_key]:
                kwargs.pop(param_key)

        data = self.client.usermanage.list_departments(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['results']
        else:
            logger.warning(f"{get_now_time()} 获取部门列表失败：{data['message']} 接口名称(list_departments) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def list_department_profiles(self, department_id=0, lookup_field='id', recursive=False, no_page=False):
        """
        请求某部门的用户信息
        :param department_id: int 	部门 ID
        :param lookup_field: string  查找字段, 默认值为 'id'
        :param recursive: bool 是否级联查询部门用户,默认为否
        :param fuzzy_lookups: bool 是否不分页一次性返回所有结果，默认为否（注意：当使用 no_page=true 时，结果返回内容会根据 leader 关联情况平铺展开，可能出现 username 重复情况）
        :return: result
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "id": department_id,
            "lookup_field": lookup_field,
            "recursive": recursive,
            "no_page": no_page
        }

        data = self.client.usermanage.list_department_profiles(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['results']
        else:
            logger.warning(f"{get_now_time()} 请求部门的用户信息失败：{data['message']} 接口名称(list_department_profiles) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def list_profile_departments(self, user_id=0, lookup_field='username', with_family=False):
        """
        请求某个用户的部门信息
        :param user_id: int 	用户 ID
        :param lookup_field: string  查询字段, 默认为 'username'
        :param with_family: bool 结果是否返回部门树, 默认为否
        :return: result
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "id": user_id,
            "lookup_field": lookup_field,
            "with_family": with_family
        }

        data = self.client.usermanage.list_profile_departments(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 请求用户的部门信息失败：{data['message']} 接口名称(list_profile_departments) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def list_users(self, page=0, page_size=0, fields=None, lookup_field='', exact_lookups='', fuzzy_lookups=''):
        """
        获取用户列表
        :param page: int 	页码
        :param page_size: int 	每页结果数量
        :param fields: string 返回值字段, 例如"username,id"
        :param lookup_field: string  查找字段, 默认值为 'id'
        :param exact_lookups: string 精确查找内容列表, 例如"jack,pony" 需和lookup_field 搭配
        :param fuzzy_lookups: string 模糊查找内容列表, 例如"jack,pony" 需和lookup_field 搭配
        :return: result
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "lookup_field": lookup_field,
            "page": page,
            "page_size": page_size,
            "fields": fields,
            "exact_lookups": exact_lookups,
            "fuzzy_lookups": fuzzy_lookups
        }

        data = self.client.usermanage.list_users(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 获取用户列表失败：{data['message']} 接口名称(list_users) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def retrieve_department(self, department_id, fields=None):
        """
        查询部门具体信息
        :param department_id: string 	查询目标组织的 id，例如 1122
        :param fields: string 返回字段, 例如 "name,id"
        :return: result
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "id": department_id,
            "fields": fields
        }

        data = self.client.usermanage.retrieve_department(kwargs)
        result = {"result": False, "message": "nothing", "data": {}}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 查询部门具体信息失败：{data['message']} 接口名称(retrieve_department) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def retrieve_user(self, user_id=0, user_name='',lookup_field='id', fields=None):
        """
        查询用户具体详情
        :param user_id: string 	用户id 需要搭配lookup_field
        :param user_name: string  用户名称 需要搭配lookup_field
        :param lookup_field: string 查询字段, 默认为 'id', 可选的唯一字段：'username'、'id'
        :param fields: string 返回字段, 例如 "name,id"
        :return: result
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "id": user_id,
            "name": user_name,
            "lookup_field": lookup_field,
            "fields": fields
        }

        for param_key in list(kwargs.keys()):
            if not kwargs[param_key]:
                kwargs.pop(param_key)

        data = self.client.usermanage.retrieve_user(kwargs)
        result = {"result": False, "message": "nothing", "data": {}}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 查询用户具体详情失败：{data['message']} 接口名称(retrieve_user) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result


def save_json(filename, data):
    with open(f"{filename}.json", "w", encoding="utf-8")as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))


def get_now_time():
    return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
