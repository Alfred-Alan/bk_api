import copy
import json
import logging
import requests
import datetime

import datetime

from iam import IAM
from iam.api import client
from iam import IAM, Request, Subject, Action, Resource
from iam.apply.models import ActionWithoutResources, ActionWithResources, Application, RelatedResourceType
from iam.apply.models import ResourceInstance, ResourceNode

from config import APP_CODE as app_code, SECRET_KEY as app_secret, IAM_BASE_URL as iam_url, BK_URL
from blueking.component.shortcuts import get_client_by_request

logger = logging.getLogger(__name__)


class IAM_API:

    def __init__(self, bk_token, client):
        self.bk_token = bk_token
        self.client = client
        self.headers = {
            "X-Bk-App-Code": app_code,
            "X-Bk-App-Secret": app_secret,
            "X-Bk-IAM-Version": "1"
        }
        # self.headers = {
        #     "X-Bk-App-Code": "bk_iam",
        #     "X-Bk-App-Secret": "cc506e22-e186-49b4-a2f8-4d5a1260c5b3",
        #     "X-Bk-IAM-Version": "1"
        # }

    def reload(self, bk_token, request):
        self.bk_token = bk_token
        self.client = get_client_by_request(request)

    def add_system(self, id, name, name_en, clients, provider_config: dict, description="", description_en=""):
        """
        新增权限系统
        :param id: string 系统 id，全局唯一
        :param name: string 系统名称，全局唯一
        :param name_en: string 系统英文名，国际化时切换到英文版本显示
        :param description: string 系统描述，全局唯一
        :param description_en: string 系统描述英文，国际化时切换到英文版本显示
        :param clients: string 有权限调用的客户端，即有权限调用的 app_code 列表，多个使用英文逗号分隔
        :param provider_config: Object 权限中心回调接入系统的配置文件
        :return:
        """
        kwargs = {
            "id": id,
            "name": name,
            "name_en": name_en,
            "description": description,
            "description_en": description_en,
            "clients": clients,
            "provider_config": provider_config
        }
        url = "/api/v1/model/systems"
        data = request_url(method="post", url=iam_url + url, data=json.dumps(kwargs), headers=self.headers)

        result = {"result": False, 'message': 'Nothing', 'id': ''}

        if data.get('result', False):
            result['result'] = data['result']
            result['id'] = data['data'].get('id', id)
        else:
            logger.warning(f"{get_now_time()} 新增权限系统失败：{data['message']} 接口名称({url}) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def update_system(self, id, name, name_en, clients, provider_config: dict, description="", description_en=""):
        """
        更新权限系统
        :param id: string 系统 id，全局唯一
        :param name: string 系统名称，全局唯一
        :param name_en: string 系统英文名，国际化时切换到英文版本显示
        :param description: string 系统描述，全局唯一
        :param description_en: string 系统描述英文，国际化时切换到英文版本显示
        :param clients: string 有权限调用的客户端，即有权限调用的 app_code 列表，多个使用英文逗号分隔
        :param provider_config: Object 权限中心回调接入系统的配置文件
        :param is_update: bool 是否为更新操作
        :return:
        """
        kwargs = {
            "id": id,
            "name": name,
            "name_en": name_en,
            "description": description,
            "description_en": description_en,
            "clients": clients,
            "provider_config": provider_config
        }
        url = f"/api/v1/model/systems/{id}"
        data = request_url(method="put", url=iam_url + url, data=json.dumps(kwargs), headers=self.headers)

        result = {"result": False, 'message': 'Nothing', 'id': ''}

        if data.get('result', False):
            result['result'] = data['result']
            result['id'] = data['data'].get('id', id)
        else:
            logger.warning(f"{get_now_time()} 更新权限系统失败：{data['message']} 接口名称({url}) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def add_resource_type(self, system_id, id, name, name_en, provider_config: dict, version=1, parents=[],
                          description="", description_en=""):
        """
        新增资源类型
        :param system_id: string 权限系统id
        :param id: string 资源类型 id全局唯一
        :param name: string 资源类型名称，全局唯一
        :param name_en: string 资源类型英文名，国际化时切换到英文版本显示
        :param description: string 资源类型系统描述，全局唯一
        :param description_en: string 系统描述英文，国际化时切换到英文版本显示
        :param parents: Array 资源类型的直接上级，可多个直接上级，可以是自身系统的资源类型或其他系统的资源类型, 可为空列表，不允许重复
        :param provider_config: Object 权限中心调用查询资源实例接口的配置文件，与 system.provider_config.host
        :param version: int 版本号，允许为空
        :return:
        """
        kwargs = [{
            "id": id,
            "name": name,
            "name_en": name_en,
            "description": description,
            "description_en": description_en,
            "parents": parents,
            "provider_config": provider_config,
            "version": version
        }]

        url = f"/api/v1/model/systems/{system_id}/resource-types"
        data = request_url(method="post", url=iam_url + url, data=json.dumps(kwargs), headers=self.headers)

        result = {"result": False, 'message': 'Nothing', 'data': {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 新增资源类型失败：{data['message']} 接口名称({url}) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def update_resource_type(self, system_id, id, name, name_en, provider_config: dict, version=1, parents=[],
                             description="", description_en=""):
        """
        修改资源类型
        :param system_id: string 权限系统id
        :param id: string 资源类型 id全局唯一
        :param name: string 资源类型名称，全局唯一
        :param name_en: string 资源类型英文名，国际化时切换到英文版本显示
        :param description: string 资源类型系统描述，全局唯一
        :param description_en: string 系统描述英文，国际化时切换到英文版本显示
        :param parents: Array 资源类型的直接上级，可多个直接上级，可以是自身系统的资源类型或其他系统的资源类型, 可为空列表，不允许重复
        :param provider_config: Object 权限中心调用查询资源实例接口的配置文件，与 system.provider_config.host
        :param version: int 版本号，允许为空
        :return:
        """
        kwargs = {
            "name": name,
            "name_en": name_en,
            "description": description,
            "description_en": description_en,
            "parents": parents,
            "provider_config": provider_config,
            "version": version
        }

        url = f"/api/v1/model/systems/{system_id}/resource-types/{id}"
        data = request_url(method="put", url=iam_url + url, data=json.dumps(kwargs), headers=self.headers)

        result = {"result": False, 'message': 'Nothing', 'data': {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 修改资源类型失败：{data['message']} 接口名称({url}) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def delete_resource_type(self, system_id, id):
        """
        删除资源类型
        :param system_id: string 权限系统id
        :param id: string 资源类型 id全局唯一
        :return:
        """
        kwargs = {}
        url = f"/api/v1/model/systems/{system_id}/resource-types/{id}"
        data = request_url(method="delete", url=iam_url + url, data=kwargs, headers=self.headers)

        save_json("delete_resource_type", data)

        result = {"result": False, 'message': 'Nothing', 'data': {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 删除资源类型失败：{data['message']} 接口名称({url}) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def add_instance_selection(self, system_id, id, name, name_en, resource_type_chain=[], is_dynamic=False):
        """
        新增实例视图
        :param system_id: string 权限系统id
        :param id: string 实例视图 id, 系统下唯一
        :param name: string 实例视图名称，系统下唯一
        :param name_en: string 实例视图的英文名
        :param is_dynamic: bool 是否是动态拓扑视图，默认为false
        :param resource_type_chain: Array 资源类型的层级链路
        :return:
        """
        kwargs = [{
            "id": id,
            "name": name,
            "name_en": name_en,
            "is_dynamic": is_dynamic,
            "resource_type_chain": resource_type_chain
        }]
        url = f"/api/v1/model/systems/{system_id}/instance-selections"
        data = request_url(method="post", url=iam_url + url, data=json.dumps(kwargs), headers=self.headers)

        result = {"result": False, 'message': 'Nothing', 'data': {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 新增实例视图失败：{data['message']} 接口名称({url}) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def update_instance_selection(self, system_id, id, name, name_en, resource_type_chain=[], is_dynamic=False):
        """
        修改实例视图
        :param system_id: string 权限系统id
        :param id: string 实例视图 id, 系统下唯一
        :param name: string 实例视图名称，系统下唯一
        :param name_en: string 实例视图的英文名
        :param is_dynamic: bool 是否是动态拓扑视图，默认为false
        :param resource_type_chain: Array 资源类型的层级链路
        :return:
        """
        kwargs = {
            "id": id,
            "name": name,
            "name_en": name_en,
            "is_dynamic": is_dynamic,
            "resource_type_chain": resource_type_chain
        }
        url = f"/api/v1/model/systems/{system_id}/instance-selections/{id}"
        data = request_url(method="put", url=iam_url + url, data=json.dumps(kwargs), headers=self.headers)

        result = {"result": False, 'message': 'Nothing', 'data': {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 修改实例视图失败：{data['message']} 接口名称({url}) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def delete_instance_selection(self, system_id, id):
        """
        删除实例视图
        :param system_id: string 权限系统id
        :param id: string 实例视图 id, 系统下唯一
        :return:
        """
        kwargs = {}
        url = f"/api/v1/model/systems/{system_id}/instance-selections/{id}"
        data = request_url(method="delete", url=iam_url + url, data=kwargs, headers=self.headers)

        result = {"result": False, 'message': 'Nothing', 'data': {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 删除实例视图失败：{data['message']} 接口名称({url}) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def add_action(self, system_id, id, name, name_en, description='', description_en='', type='',
                   related_resource_types=[], related_actions=[], version=1):
        """
        添加操作
        :param system_id: string 权限系统id
        :param id: string 操作 id 系统下唯一
        :param name: string 操作名称
        :param name_en: string 操作英文名
        :param description: string 操作描述
        :param description_en: string 操作描述英文
        :param type: string 操作的类型，枚举值包括create,delete,view,edit,list,manage,execute,use
        :param related_resource_types: Array 操作的对象，资源类型有序列表，列表顺序与产品展示、鉴权校验 顺序 必须保持一致。如果操作无需关联资源实例，这里为空即可
        :param related_actions: Array 操作的依赖操作, 由操作 ID 组成的字符串列表, 用于在申请权限时同时创建依赖权限 更多概念说明
        :param version: int 版本号
        :return:
        """

        kwargs = [{
            "id": id,
            "name": name,
            "name_en": name_en,
            "description": description,
            "description_en": description_en,
            "type": type,
            "related_resource_types": related_resource_types,
            "related_actions": related_actions,
            "version": version
        }]
        url = f"/api/v1/model/systems/{system_id}/actions"
        data = request_url(method="post", url=iam_url + url, data=json.dumps(kwargs), headers=self.headers)

        result = {"result": False, 'message': 'Nothing', 'data': {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 添加操作失败：{data['message']} 接口名称({url}) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def update_action(self, system_id, id, name, name_en, description='', description_en='', type='',
                      related_resource_types=[], related_actions=[], version=1):
        """
        修改操作
        :param system_id: string 权限系统id
        :param id: string 操作 id 系统下唯一
        :param name: string 操作名称
        :param name_en: string 操作英文名
        :param description: string 操作描述
        :param description_en: string 操作描述英文
        :param type: string 操作的类型，枚举值包括create,delete,view,edit,list,manage,execute,use
        :param related_resource_types: Array 操作的对象，资源类型有序列表，列表顺序与产品展示、鉴权校验 顺序 必须保持一致。如果操作无需关联资源实例，这里为空即可
        :param related_actions: Array 操作的依赖操作, 由操作 ID 组成的字符串列表, 用于在申请权限时同时创建依赖权限 更多概念说明
        :param version: int 版本号
        :return:
        """
        kwargs = {
            "name": name,
            "name_en": name_en,
            "description": description,
            "description_en": description_en,
            "type": type,
            "related_resource_types": related_resource_types,
            "related_actions": related_actions,
            "version": version
        }
        url = f"/api/v1/model/systems/{system_id}/actions/{id}"
        data = request_url(method="put", url=iam_url + url, data=json.dumps(kwargs), headers=self.headers)

        result = {"result": False, 'message': 'Nothing', 'data': {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 修改操作失败：{data['message']} 接口名称({url}) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def delete_action(self, system_id, id):
        """
        删除操作
        :param system_id: string 权限系统id
        :param id: string 实例视图 id, 系统下唯一
        :return:
        """
        kwargs = {}
        url = f"/api/v1/model/systems/{system_id}/actions/{id}"
        data = request_url(method="delete", url=iam_url + url, data=kwargs, headers=self.headers)

        result = {"result": False, 'message': 'Nothing', 'data': {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 删除操作失败：{data['message']} 接口名称({url}) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def add_action_group(self, system_id, name, name_en, actions=[], sub_groups=[]):
        """
        添加操作组
        :param system_id: string 权限系统id
        :param name: string 操作组名称
        :param name_en: string 操作组英文名
        :param actions: Array 操作列表
        :param sub_groups: Array 下一级操作组
        :return:
        """
        kwargs = [{
            "name": name,
            "name_en": name_en,
            "actions": actions,
            "sub_groups": sub_groups
        }]

        url = f"/api/v1/model/systems/{system_id}/configs/action_groups"
        data = request_url(method="post", url=iam_url + url, data=json.dumps(kwargs), headers=self.headers)

        result = {"result": False, 'message': 'Nothing', 'data': {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 添加操作组失败：{data['message']} 接口名称({url}) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def update_action_group(self, system_id, name, name_en, actions=[], sub_groups=[]):
        """
        更新(覆盖)操作组
        :param system_id: string 权限系统id
        :param name: string 操作组名称
        :param name_en: string 操作组英文名
        :param actions: Array 操作列表
        :param sub_groups: Array 下一级操作组
        :return:
        """
        kwargs = [{
            "name": name,
            "name_en": name_en,
            "actions": actions,
            "sub_groups": sub_groups
        }]

        url = f"/api/v1/model/systems/{system_id}/configs/action_groups"
        data = request_url(method="put", url=iam_url + url, data=json.dumps(kwargs), headers=self.headers)

        result = {"result": False, 'message': 'Nothing', 'data': {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 更新(覆盖)操作组失败：{data['message']} 接口名称({url}) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def common_query(self, system_id, fields=None):
        """
         查询系统注册的信息
        :param system_id: string 权限系统id
        :param fields: string 需要查询的信息类型，枚举值：.
                        base_info(基础信息),
                        resource_types(资源类型)，
                        actions(操作)，
                        action_groups (操作组),
                        instance_selections(实例视图),
                        resource_creator_actions(新建关联配置),
                        common_actions(常用操作) 多个以英文逗号分隔，空值时查询所有注册的信息
        :return:
        """
        kwargs = {
            "fields": fields
        }

        url = f"/api/v1/model/systems/{system_id}/query"
        data = request_url(method="get", url=iam_url + url, params=kwargs, headers=self.headers)

        result = {"result": False, 'message': 'Nothing', 'data': {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()}  查询系统注册的信息失败：{data['message']} 接口名称({url}) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def get_system_token(self, system_id):
        """
        查询系统 token 用于权限中心 调用 接入系统 拉取资源信息相关接口的鉴权
        :param system_id: string 权限系统id
        :return:
        """
        kwargs = {}

        url = f"/api/v1/model/systems/{system_id}/token"
        data = request_url(method="get", url=iam_url + url, params=kwargs, headers=self.headers)

        result = {"result": False, 'message': 'Nothing', 'data': {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 查询系统 token失败：{data['message']} 接口名称({url}) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def add_common_actions(self, system_id, name, name_en, actions):
        """
        添加常用操作配置
        :param system_id: string 权限系统id
        :param name: string 常用操作名称
        :param name_en: string 常用操作英文名，国际化时切换到英文版本显示
        :param actions: Arry 	操作  列表
        :return:
        """
        kwargs = [{
            "name": name,
            "name_en": name_en,
            "actions": actions
        }]

        url = f"/api/v1/model/systems/{system_id}/configs/common_actions"
        data = request_url(method="post", url=iam_url + url, data=json.dumps(kwargs), headers=self.headers)

        result = {"result": False, 'message': 'Nothing', 'data': {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 添加常用操作配置失败：{data['message']} 接口名称({url}) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def update_common_actions(self, system_id, name, name_en, actions):
        """
        修改常用操作配置
        :param system_id: string 权限系统id
        :param name: string 常用操作名称
        :param name_en: string 常用操作英文名，国际化时切换到英文版本显示
        :param actions: Arry 	操作  列表
        :return:
        """
        kwargs = [{
            "name": name,
            "name_en": name_en,
            "actions": actions
        }]

        url = f"/api/v1/model/systems/{system_id}/configs/common_actions"
        data = request_url(method="put", url=iam_url + url, data=json.dumps(kwargs), headers=self.headers)

        result = {"result": False, 'message': 'Nothing', 'data': {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 修改常用操作配置失败：{data['message']} 接口名称({url}) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def add_feature_shield_rules(self, system_id, effect, feature, action):
        """
        添加功能开关配置
        :param system_id: string 权限系统id
        :param effect: string 支持黑白名单，值为 deny 或 allow
        :param feature: string 	开启或关闭的功能
                application.custom_permission.grant	申请自定义权限
                application.custom_permission.renew	申请自定义权限续期
                user_permission.custom_permission.delete	自定义权限删除
        :param action: Object   操作
        :return:
        """
        kwargs = [{
            "effect": effect,
            "feature": feature,
            "action": action
        }]

        url = f"/api/v1/model/systems/{system_id}/configs/feature_shield_rules"
        data = request_url(method="post", url=iam_url + url, data=json.dumps(kwargs), headers=self.headers)

        result = {"result": False, 'message': 'Nothing', 'data': {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 添加功能开关配置失败：{data['message']} 接口名称({url}) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def update_feature_shield_rules(self, system_id, effect, feature, action):
        """
        修改功能开关配置
        :param system_id: string 权限系统id
        :param effect: string 支持黑白名单，值为 deny 或 allow
        :param feature: string 	开启或关闭的功能
                application.custom_permission.grant	申请自定义权限
                application.custom_permission.renew	申请自定义权限续期
                user_permission.custom_permission.delete	自定义权限删除
        :param action: Object   操作
        :return:
        """
        kwargs = [{
            "effect": effect,
            "feature": feature,
            "action": action
        }]

        url = f"/api/v1/model/systems/{system_id}/configs/feature_shield_rules"
        data = request_url(method="put", url=iam_url + url, data=json.dumps(kwargs), headers=self.headers)

        result = {"result": False, 'message': 'Nothing', 'data': {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 修改功能开关配置失败：{data['message']} 接口名称({url}) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def add_resource_creator_action(self, system_id, config):
        """
        新建新建关联配置
        :param system_id: string 权限系统id
        :param config: array 支持黑白名单，	新建关联的配置文件，包含了每种资源类型对应的创建时可以对创建者进行授权的 Action
        :return:
        """
        kwargs = {
            "config": config
        }

        url = f"/api/v1/model/systems/{system_id}/configs/resource_creator_actions"
        data = request_url(method="post", url=iam_url + url, data=json.dumps(kwargs), headers=self.headers)

        result = {"result": False, 'message': 'Nothing', 'data': {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 新建新建关联配置失败：{data['message']} 接口名称({url}) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def update_resource_creator_action(self, system_id, config):
        """
        修改新建关联配置
        :param system_id: string 权限系统id
        :param config: array 支持黑白名单，	新建关联的配置文件，包含了每种资源类型对应的创建时可以对创建者进行授权的 Action
        :return:
        """
        kwargs = {
            "config": config
        }

        url = f"/api/v1/model/systems/{system_id}/configs/resource_creator_actions"
        data = request_url(method="put", url=iam_url + url, data=json.dumps(kwargs), headers=self.headers)

        result = {"result": False, 'message': 'Nothing', 'data': {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 修改新建关联配置失败：{data['message']} 接口名称({url}) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def policy_query(self, username, action_id):
        """
        查看用户是否有该权限
        :param username: string 用户名称
        :param action_id: string 操作id
        :return:
        """
        permission = Permission()
        request = permission._make_request_without_resources(username, action_id)

        return permission._iam.is_allowed(request)

    def policy_query_actions(self, username, app_code, action_id):
        """
        查看用户是否有该权限
        :param username: string 用户名称
        :param app_code: string 应用id
        :param action_id: string 操作id
        :return:
        """
        permission = Permission()

        r = Resource(permission.system_id, 'app', app_code, {})
        resources = [r]
        request = permission._make_request_with_resources(username, action_id, resources)
        return permission._iam.is_allowed(request)

    def generate_apply_url(self, action_id, resource_id='', resource_type='', resource_name=''):
        """
        处理无权限 - 跳转申请列表
        :param action_id: string 操作id
        :param resource_id: string 资源id
        :param resource_type: string 资源类型
        :param resource_name: string 资源名称
        :return:
        """
        permission = Permission()
        if resource_id:
            application = Permission().make_resource_application(action_id, resource_type, resource_id, resource_name)
        else:
            application = Permission().make_no_resource_application(action_id)
        print(application.to_dict())
        # 2. get url
        ok, message, url = permission._iam.get_apply_url(application, self.bk_token)
        result = {"result": False, 'message': 'Nothing', 'url': url}
        if ok:
            result['result'] = ok
            result['url'] = url
        else:
            print(ok, message)
        result['message'] = message

        return result

class Permission(object):
    def __init__(self):
        self.system_id = app_code
        self._iam = IAM(app_code, app_secret, iam_url, BK_URL)
        self._client = client.Client(app_code, app_secret, iam_url, BK_URL)

    # 不带资源
    def _make_request_without_resources(self, username, action_id):
        request = Request(
            self.system_id,
            Subject("user", username),
            Action(action_id),
            None,
            None,
        )
        return request

    # 带资源
    def _make_request_with_resources(self, username, action_id, resources):
        request = Request(
            self.system_id,
            Subject("user", username),
            Action(action_id),
            resources,
            None,
        )
        return request

    # 申请不带资源实例的权限
    def make_no_resource_application(self, action_id):
        # 1. make application
        action = ActionWithoutResources(action_id)
        actions = [action]

        application = Application(self.system_id, actions)
        return application

    # 申请带资源实例的权限
    def make_resource_application(self, action_id, resource_type, resource_id, resource_name):
        # 1. make application
        # 这里支持带层级的资源, 例如 biz: 1/set: 2/host: 3
        # 如果不带层级, list中只有对应资源实例
        instance = ResourceInstance([ResourceNode(resource_type, resource_id, resource_name)])
        # 同一个资源类型可以包含多个资源
        related_resource_type = RelatedResourceType(self.system_id, resource_type, [instance])
        action = ActionWithResources(action_id, [related_resource_type])

        actions = [action, ]
        application = Application(self.system_id, actions)
        return application

def get_now_time():
    return datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")


def request_url(**kwargs):
    request_result = {"result": False, "code": 1, "request_id": "", "time": get_now_time(), "message": "Nothing", "data": {}}
    try:
        response = requests.request(**kwargs)
        response.encoding = "utf-8"
        if response.status_code == 200:
            res_json = response.json()
            request_result.update(**{
                "request_id": response.headers['X-Request-Id'],
                "code": res_json['code'],
                "message": res_json['message'],
                "data": res_json['data'] if res_json['data'] else {},
                "time": make_gmt_time(response.headers['Date'])
            })
            if res_json['code'] != 0:
                request_result['result'] = False
            else:
                request_result['result'] = True
    except Exception as e:
        request_result['message'] = str(e)
    return request_result


def make_gmt_time(gmt_str):
    time_obj = datetime.datetime.strptime(gmt_str, '%a, %d %b %Y %H:%M:%S GMT') + datetime.timedelta(hours=8)
    return time_obj.strftime("%Y-%m-%d %H:%M:%S")

def save_json(filename, data):
    with open(f"{filename}.json", "w", encoding="utf-8")as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))
