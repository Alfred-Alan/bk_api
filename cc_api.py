import json
from datetime import datetime

from config import APP_CODE as app_code, SECRET_KEY as app_secret
from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from blueapps.utils.logger import logger


class CC_API:
    def __init__(self, bk_token, client):
        self.bk_token = bk_token
        self.client = client

    def reload(self, bk_token, request):
        self.bk_token = bk_token
        self.client = get_client_by_request(request)

    def add_host_lock(self, id_list: []):
        """
        新加主机锁
        :param id_list: 主机id
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "id_list": id_list
        }
        data = self.client.cc.add_host_lock(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("新加主机锁失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def add_host_to_resource(self, host_innerips: [], bk_supplier_account="", bk_biz_id=""):
        """
        新增主机到资源池
        :param bk_supplier_account: 开发商账号
        :param bk_biz_id: 	业务ID
        :param host_innerips: 主机内网ip
        :return:
        """
        host_info = {str(index): {"bk_host_innerip": ip, "bk_cloud_id": 0, "import_from": "3"} for index, ip in
                     enumerate(host_innerips)}

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_supplier_account": bk_supplier_account,
            "host_info": host_info
        }
        data = self.client.cc.add_host_to_resource(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("新增主机到资源池失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    # todo
    def add_instance_association(self, bk_biz_id, bk_obj_asst_id, bk_inst_id, bk_asst_inst_id):
        """
        新增模型实例之间的关联关系
        :param bk_obj_asst_id: 模型之间关系关系的唯一 id
        :param bk_inst_id: 	源模型实例 id
        :param bk_asst_inst_id: 目标模型实例 id
        :param bk_biz_id: 	业务 id
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,

            "bk_obj_asst_id": bk_obj_asst_id,
            "bk_inst_id": bk_inst_id,
            "bk_asst_inst_id": bk_asst_inst_id,
            "metadata": {
                "label": {
                    "bk_biz_id": bk_biz_id
                }
            }
        }
        data = self.client.cc.add_instance_association(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("新增模型实例之间的关联关系失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    # todo
    def add_label_for_service_instance(self, bk_biz_id, instance_ids: [], labels: {}):
        """
        根据服务实例 id 和设置的标签为服务实例添加标签
        :param bk_biz_id：业务id
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "instance_ids": instance_ids,
            "labels": labels
        }
        data = self.client.cc.add_label_for_service_instance(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("根据服务实例 id 和设置的标签为服务实例添加标签失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def clone_host_property(self, bk_biz_id, bk_org_ip, bk_dst_ip):
        """
        克隆主机属性
        :param bk_biz_id：业务id
        :param bk_org_ip：源主机ip, 只支持传入单ip
        :param bk_dst_ip：目标主机ip, 多个ip用","分割
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_org_ip": bk_org_ip,
            "bk_dst_ip": bk_dst_ip,
            "bk_cloud_id": 0
        }
        data = self.client.cc.clone_host_property(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("克隆主机属性失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def create_business(self, bk_biz_name, time_zone, language):
        """
        新建业务
        :param bk_biz_name：业务名
        :param time_zone：时区
        :param language：语言, "1"代表中文, "2"代表英文
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_supplier_account": "0",
            "data": {
                "bk_biz_name": bk_biz_name,
                "bk_biz_maintainer": "admin",
                "bk_biz_productor": "admin",
                "bk_biz_developer": "admin",
                "bk_biz_tester": "admin",
                "time_zone": time_zone,
                "language": language
            }
        }
        data = self.client.cc.create_business(kwargs)

        result = {"result": False, "message": "nothing", "bk_biz_id": 0}

        if data.get("result", False):
            result['result'] = data['result']
            result['bk_biz_id'] = data['data']['bk_biz_id']
        else:
            logger.error("新建业务失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def create_classification(self, bk_classification_id, bk_classification_name):
        """
        添加模型分类
        :param bk_classification_id：业务名
        :param bk_classification_name：时区
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_classification_id": bk_classification_id,
            "bk_classification_name": bk_classification_name
        }
        data = self.client.cc.create_classification(kwargs)

        result = {"result": False, "message": "nothing", "id": 0}

        if data.get("result", False):
            result['result'] = data['result']
            result['id'] = data['data']['id']
        else:
            logger.error("添加模型分类失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def create_cloud_area(self, bk_cloud_name):
        """
        根据云区域名字创建云区域
        :param bk_cloud_name：云区域名称
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_cloud_name": bk_cloud_name
        }
        data = self.client.cc.create_cloud_area(kwargs)

        result = {"result": False, "message": "nothing", "created": {}}

        if data.get("result", False):
            result['result'] = data['result']
            result['created'] = data['data']['created']
        else:
            logger.error("根据云区域名字创建云区域失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def find_host_biz_relations(self, bk_biz_id, bk_host_id: []):
        """
        根据主机ID查询业务相关信息
        :param bk_host_id：主机ID数组，ID个数不能超过500
        :param bk_biz_id：业务id
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_host_id": bk_host_id,
            "bk_biz_id": bk_biz_id
        }
        data = self.client.cc.find_host_biz_relations(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("根据主机ID查询业务相关信息失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def find_host_by_service_template(self, bk_biz_id, bk_service_template_ids: [], bk_module_ids=[]):
        """
        获取服务模板下的主机
        :param bk_biz_id：业务id
        :param bk_service_template_ids：服务模板ID列表，最多可填500个
        :param bk_module_ids：模块ID列表, 最多可填500个
        :param fields：主机属性列表
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_service_template_ids": bk_service_template_ids,
            "bk_module_ids": bk_module_ids,
            "fields": [
                "bk_host_id",
                "bk_host_innerip"
            ],
            "page": {
                "start": 0,
                "limit": 500
            }
        }
        data = self.client.cc.find_host_by_service_template(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("根据主机ID查询业务相关信息失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def find_host_by_set_template(self, bk_biz_id, bk_set_template_ids: [], bk_set_ids=[]):
        """
        获取集群模板下的主机
        :param bk_biz_id：业务id
        :param bk_service_template_ids：集群模板ID列表
        :param bk_set_ids：集群ID列表,
        :param fields：主机属性列表
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_set_template_ids": bk_set_template_ids,
            "bk_set_ids": bk_set_ids,
            "fields": [
                "bk_host_id",
                "bk_host_innerip"
            ],
            "page": {
                "start": 0,
                "limit": 500
            }
        }
        data = self.client.cc.find_host_by_set_template(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['info']
        else:
            logger.error("获取集群模板下的主机失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def find_host_by_topo(self, bk_biz_id, bk_obj_id, bk_inst_id):
        """
        获取集群模板下的主机
        :param bk_biz_id：业务id
        :param bk_obj_id：集群模板ID列表
        :param bk_inst_id：集群ID列表
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_obj_id": bk_obj_id,
            "bk_inst_id": bk_inst_id,
            "fields": [
                "bk_host_id",
                "bk_host_innerip"
            ],
            "page": {
                "start": 0,
                "limit": 500
            }
        }
        data = self.client.cc.find_host_by_topo(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['info']
        else:
            logger.error("获取集群模板下的主机失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def find_host_snapshot_batch(self, bk_host_ids):
        """
        根据主机实例ID列表和想要获取的主机快照属性列表批量获取主机快照
        :param bk_host_ids：主机实例ID列表, 即bk_host_id列表
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_ids": bk_host_ids,
            "fields": [
                "bk_host_id",
                "bk_all_ips"
            ]
        }
        data = self.client.cc.find_host_snapshot_batch(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("根据主机实例ID列表和想要获取的主机快照属性列表批量获取主机快照：%s" % data['message'])

        result['message'] = data['message']

        return result

    def find_host_topo_relation(self, bk_biz_id, bk_host_ids=[], bk_set_ids=[], bk_module_ids=[]):
        """
        获取主机与拓扑的关系
        :param bk_biz_id：业务id
        :param bk_host_ids：主机id
        :param bk_set_ids：集群id
        :param bk_module_ids：模块id
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "page": {
                "start": 0,
                "limit": 500
            },
            "bk_biz_id": bk_biz_id,
            "bk_set_ids": bk_set_ids,
            "bk_module_ids": bk_module_ids,
            "bk_host_ids": bk_host_ids
        }
        data = self.client.cc.find_host_topo_relation(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['data']
        else:
            logger.error("获取主机与拓扑的关系：%s" % data['message'])

        result['message'] = data['message']

        return result

    def find_module_batch(self, bk_biz_id, bk_module_ids: []):
        """
        根据业务ID和模块实例ID列表，加上想要返回的模块属性列表，批量获取指定业务下模块实例的属性信息
        :param bk_biz_id：业务id
        :param bk_ids：模块实例ID列表, 即bk_module_id列表，最多可填500个
        :param fields：模块属性列表
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_ids": bk_module_ids,
            "fields": [
                "bk_module_id",
                "bk_module_name",
                "create_time"
            ]
        }
        data = self.client.cc.find_module_batch(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("根据业务ID和模块实例ID列表，加上想要返回的模块属性列表，批量获取指定业务下模块实例的属性信息：%s" % data['message'])

        result['message'] = data['message']

        return result

    def find_module_host_relation(self, bk_biz_id, bk_module_ids: []):
        """
        根据模块ID查询主机和模块的关系
        :param bk_biz_id：业务id
        :param bk_module_ids：模块实例ID列表
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_module_ids": bk_module_ids,
            "module_fields": [
                "bk_module_id",
                "bk_module_name"
            ],
            "host_fields": [
                "bk_host_innerip",
                "bk_host_id"
            ],
            "page": {
                "start": 0,
                "limit": 500
            }
        }
        data = self.client.cc.find_module_host_relation(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['relation']
        else:
            logger.error("根据模块ID查询主机和模块的关系失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def find_module_with_relation(self, bk_biz_id, bk_set_ids: [], bk_service_template_ids=[]):
        """
        根据条件查询业务下的模块
        :param bk_biz_id：业务id
        :param bk_set_ids：集群ID列表
        :param bk_service_template_ids：服务模板ID列表
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_set_ids": bk_set_ids,
            "bk_service_template_ids": bk_service_template_ids,
            "fields": ["bk_module_id", "bk_module_name"],
            "page": {
                "start": 0,
                "limit": 500
            }
        }
        data = self.client.cc.find_module_with_relation(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['info']
        else:
            logger.error("根据条件查询业务下的模块失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def find_object_association(self, bk_asst_id, bk_obj_id, bk_asst_obj_id):
        """
        查询模型的实例之间的关联关系。
        :param bk_asst_id：模型的关联类型唯一id
        :param bk_obj_id：源模型id
        :param bk_asst_id：目标模型id
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "condition": {
                "bk_asst_id": bk_asst_id,
                "bk_obj_id": bk_obj_id,
                "bk_asst_obj_id": bk_asst_obj_id
            }
        }
        data = self.client.cc.find_object_association(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("查询模型的实例之间的关联关系失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def find_set_batch(self, bk_biz_id, bk_set_ids: []):
        """
        根据业务id和集群实例id列表，以及想要获取的属性列表，批量获取指定业务下集群的属性详情
        :param bk_biz_id：业务id
        :param bk_set_ids：集群ID列表
        :param bk_service_template_ids：服务模板ID列表
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_ids": bk_set_ids,
            "fields": [
                "bk_set_id",
                "bk_set_name",
                "create_time"
            ]
        }
        data = self.client.cc.find_set_batch(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("根据业务id和集群实例id列表，以及想要获取的属性列表，批量获取指定业务下集群的属性详情失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def find_topo_node_paths(self, bk_biz_id, bk_obj_id, bk_inst_id):
        """
        根据业务拓扑层级中的节点实例 查询该节点的父层级一直到业务顶点的路径信息
        :param bk_biz_id：业务id
        :param bk_obj_id：业务拓扑节点模型名称
        :param bk_inst_id：该业务拓扑节点的实例ID
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_nodes": [{"bk_obj_id": bk_obj_id, "bk_inst_id": bk_inst_id}
                         ]
        }
        data = self.client.cc.find_topo_node_paths(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("根据业务拓扑层级中的某个节点实例(包括自定义节层级实例)，查询该节点的父层级一直到业务顶点的路径信息失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def get_biz_internal_module(self, bk_biz_id):
        """
        根据业务ID获取业务空闲机, 故障机和待回收模块
        :param bk_biz_id：业务id
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_supplier_account": "0"
        }
        data = self.client.cc.get_biz_internal_module(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("根据业务ID获取业务空闲机, 故障机和待回收模块失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def get_host_base_info(self, bk_host_id):
        """
        获取主机基础信息详情
        :param bk_host_id：	主机ID
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_host_id": bk_host_id,
            "bk_supplier_account": "0"
        }
        data = self.client.cc.get_host_base_info(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("获取主机基础信息详情失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def get_mainline_object_topo(self):
        """
        获取主线模型的业务拓扑
        :param
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_supplier_account": "0"
        }
        data = self.client.cc.get_mainline_object_topo(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("获取主线模型的业务拓扑失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def get_proc_template(self, process_template_id):
        """
        获取单个进程模板信息
        :param process_template_id： 进程模板ID
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "process_template_id": process_template_id,
            "bk_supplier_account": "0"
        }
        data = self.client.cc.get_proc_template(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['info']
        else:
            logger.error("获取单个进程模板信息失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def get_service_template(self, service_template_id):
        """
        根据服务模板ID获取服务模板
        :param process_template_id： 服务模板ID
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "service_template_id": service_template_id,
            "bk_supplier_account": "0"
        }
        data = self.client.cc.get_service_template(kwargs)

        result = {"result": False, "message": "nothing", "data": {}}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("根据服务模板ID获取服务模板失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def list_biz_hosts(self, bk_biz_id: int, bk_obj_id, bk_inst_ids=[]):
        """
        查询业务下主机
        :param bk_biz_id:
        :param bk_obj_id:
        :param bk_inst_ids:
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
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
            logger.error("获取业务下主机失败 %s" % data['message'])

        result['message'] = data['message']

        return result

    def list_biz_hosts_topo(self, bk_biz_id: int):
        """
        查询业务id业务下的主机和拓扑信息,可附带一些查询条件
        :param bk_biz_id: 业务ID
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "fields": [
                "bk_host_id",
                "bk_cloud_id",
                "bk_host_innerip",
                "bk_os_type",
                "bk_mac"
            ],
            "page": {
                "start": 0,
                "limit": 500,
                "sort": "bk_host_id"
            },
        }
        data = self.client.cc.list_biz_hosts_topo(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result["result"] = data['result']
            result["data"] = data['data']['info']
        else:
            logger.error("查询业务id业务下的主机和拓扑信息,可附带一些查询条件失败 %s" % data['message'])

        result['message'] = data['message']

        return result

    def list_hosts_without_biz(self):
        """
        没有业务信息的主机查询
        :param
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "fields": [
                "bk_host_id",
                "bk_cloud_id",
                "bk_host_innerip",
                "bk_os_type",
                "bk_mac"
            ],
            "page": {
                "start": 0,
                "limit": 500
            },
        }
        data = self.client.cc.list_hosts_without_biz(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result["result"] = data['result']
            result["data"] = data['data']['info']
        else:
            logger.error("没有业务信息的主机查询失败 %s" % data['message'])

        result['message'] = data['message']

        return result

    def list_process_detail_by_ids(self, bk_biz_id, bk_process_ids):
        """
        查询某业务下进程ID对应的进程详情
        :param bk_biz_id  进程所在的业务ID
        :param bk_process_ids  进程ID列表
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_process_ids": bk_process_ids,
            "fields": [
                "bk_process_id",
                "bk_process_name",
                "bk_func_id",
                "bk_func_name"
            ]
        }
        data = self.client.cc.list_process_detail_by_ids(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result["result"] = data['result']
            result["data"] = data['data']
        else:
            logger.error("查询某业务下进程ID对应的进程详情失败 %s" % data['message'])

        result['message'] = data['message']

        return result

    def list_process_instance(self, bk_biz_id, service_instance_id):
        """
        根据服务实例ID查询进程实例列表
        :param bk_biz_id  进程所在的业务ID
        :param service_instance_id  服务实例ID
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "service_instance_id": service_instance_id
        }
        data = self.client.cc.list_process_instance(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result["result"] = data['result']
            result["data"] = data['data']
        else:
            logger.error("根据服务实例ID查询进程实例列表失败 %s" % data['message'])

        result['message'] = data['message']

        return result

    def list_proc_template(self, bk_biz_id, service_template_id):
        """
        根据服务模板ID查询进程模板信息
        :param bk_biz_id： 业务ID
        :param service_template_id： 服务模板ID
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "service_template_id": service_template_id
        }
        data = self.client.cc.list_proc_template(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['info']
        else:
            logger.error("根据服务模板ID查询进程模板信息失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def list_resource_pool_hosts(self):
        """
        查询资源池中的主机
        :param
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "page": {
                "start": 0,
                "limit": 500,
                "sort": "bk_host_id"
            },
            "fields": [
                "bk_host_id",
                "bk_cloud_id",
                "bk_host_innerip",
                "bk_os_type",
                "bk_mac"
            ],
        }
        data = self.client.cc.list_resource_pool_hosts(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['info']
        else:
            logger.error("查询资源池中的主机失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def list_service_category(self, bk_biz_id):
        """
        查询服务分类列表
        :param bk_biz_id： 业务ID
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id
        }
        data = self.client.cc.list_service_category(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['info']
        else:
            logger.error("查询服务分类列表失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def list_service_instance(self, bk_biz_id, bk_module_id):
        """
        根据业务id查询服务实例列表
        :param bk_biz_id  进程所在的业务ID
        :param bk_module_id 模块ID
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_module_id": bk_module_id,
            "page": {
                "start": 0,
                "limit": 500
            }
        }
        data = self.client.cc.list_service_instance(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result["result"] = data['result']
            result["data"] = data['data']['info']
        else:
            logger.error("根据业务id查询服务实例列表失败 %s" % data['message'])

        result['message'] = data['message']

        return result

    def list_service_instance_by_host(self, bk_biz_id, bk_host_id):
        """
        根据主机id获取绑定到主机上的服务实例列表
        :param bk_biz_id  进程所在的业务ID
        :param bk_host_id 主机ID
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_host_id": bk_host_id,
            "page": {
                "start": 0,
                "limit": 500
            }
        }
        data = self.client.cc.list_service_instance_by_host(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result["result"] = data['result']
            result["data"] = data['data']['info']
        else:
            logger.error("根据主机id获取绑定到主机上的服务实例列表失败 %s" % data['message'])

        result['message'] = data['message']

        return result

    def list_service_instance_by_set_template(self, bk_biz_id, set_template_id):
        """
        根据集群模版id获取服务实例列表
        :param bk_biz_id  进程所在的业务ID
        :param set_template_id 集群模版ID
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "set_template_id": set_template_id,
            "page": {
                "start": 0,
                "limit": 500
            }
        }
        data = self.client.cc.list_service_instance_by_set_template(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result["result"] = data['result']
            result["data"] = data['data']['info']
        else:
            logger.error("根据集群模版id获取服务实例列表失败 %s" % data['message'])

        result['message'] = data['message']

        return result

    def list_service_instance_detail(self, bk_biz_id, bk_module_id=None, bk_host_id=None, service_instance_ids=None):
        """
        根据业务id查询服务实例列表
        :param bk_biz_id  进程所在的业务ID
        :param bk_module_id 集群模版ID
        :param bk_host_id 集群模版ID
        :param service_instance_ids 集群模版ID
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_module_id": bk_module_id,
            "bk_host_id": bk_host_id,
            "service_instance_ids": service_instance_ids,
            "page": {
                "start": 0,
                "limit": 500
            }
        }
        data = self.client.cc.list_service_instance_detail(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result["result"] = data['result']
            result["data"] = data['data']['info']
        else:
            logger.error("根据业务id查询服务实例列表失败 %s" % data['message'])

        result['message'] = data['message']

        return result

    def list_service_template(self, bk_biz_id, service_category_id=None):
        """
        根据业务id查询服务模板列表,可加上服务分类id进一步查询
        :param bk_biz_id：业务id
        :param service_category_id：服务分类ID
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "service_category_id": service_category_id
        }
        print()
        data = self.client.cc.list_service_template(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['info']
        else:
            logger.error("根据业务id查询服务模板列表,可加上服务分类id进一步查询失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def list_set_template(self, bk_biz_id):
        """
        根据业务id查询集群模板
        :param bk_biz_id：业务id
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id
        }

        data = self.client.cc.list_set_template(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['info']
        else:
            logger.error("根据业务id查询集群模板失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def list_set_template_related_service_template(self, bk_biz_id, set_template_id):
        """
        根据业务id和集群模板id,获取指定业务下某集群模版的服务模版列表
        :param bk_biz_id：业务id
        :param set_template_id：集群模版ID
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "set_template_id": set_template_id
        }

        data = self.client.cc.list_set_template_related_service_template(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("根据业务id和集群模板id,获取指定业务下某集群模版的服务模版列表失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def search_biz_inst_topo(self, bk_biz_id):
        """
        查询业务实例拓扑
        :param bk_biz_id：业务id
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
        }
        data = self.client.cc.search_biz_inst_topo(kwargs)

        result = {"result": False, "message": "nothing", "data": []}
        print(result)
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("查询业务实例拓扑失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def search_business(self, condition={}):
        """
        查询业务
        :param condition:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
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
            logger.error("查询业务失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def search_classifications(self):
        """
        查询模型分类
        :param
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_supplier_account": "0"
        }
        data = self.client.cc.search_classifications(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("查询模型分类失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def search_cloud_area(self, condition={}):
        """
        查询云区域
        :param condition: 查询条件
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "condition": condition,
            "page": {
                "start": 0,
                "limit": 500
            }
        }
        data = self.client.cc.search_cloud_area(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['info']
        else:
            logger.error("查询云区域失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def search_custom_query(self, bk_biz_id, condition=None):
        """
        查询自定义查询
        :param bk_biz_id: 查询条件
        :param condition: 查询条件
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_supplier_account": "0",
            "bk_biz_id": bk_biz_id,
            "condition": condition,
            "start": 0,
            "limit": 200
        }
        data = self.client.cc.search_custom_query(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['info']
        else:
            logger.error("查询自定义查询失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def search_dynamic_group(self, bk_biz_id, condition=None):
        """
        查询动态分组列表
        :param bk_biz_id: 查询条件
        :param condition: 查询条件
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "disable_counter": True,
            "condition": condition,
            "page": {
                "start": 0,
                "limit": 200
            }
        }
        data = self.client.cc.search_dynamic_group(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['info']
        else:
            logger.error("查询动态分组列表失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def search_hostidentifier(self, ips: []):
        """
        根据条件查询主机身份
        :param ips: 主机ip列表
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "ip": {
                "data": ips,
                "bk_cloud_id": 0
            },
            "page": {
                "start": 0,
                "limit": 500,
                "sort": "bk_host_id"
            }
        }
        data = self.client.cc.search_hostidentifier(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['info']
        else:
            logger.error("根据条件查询主机身份失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def search_host_lock(self, id_list: []):
        """
        根据主机id列表查询主机锁
        :param id_list: 主机id列表
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "id_list": id_list
        }
        data = self.client.cc.search_host_lock(kwargs)

        result = {"result": False, "message": "nothing", "data": {}}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("根据主机id列表查询主机锁失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def search_inst(self, bk_obj_id):
        """
        根据关联关系实例查询模型实例
        :param bk_obj_id: 模型ID
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_obj_id": bk_obj_id,
            "bk_supplier_account": "0",
            "page": {
                "start": 0,
                "limit": 500,
                "sort": "bk_inst_id"
            },
        }
        data = self.client.cc.search_inst(kwargs)

        result = {"result": False, "message": "nothing", "data": {}}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['info']
        else:
            logger.error("根据关联关系实例查询模型实例失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def search_inst_association_topo(self, bk_obj_id, bk_inst_id):
        """
        查询实例关联拓扑
        :param bk_obj_id：模型id
        :param bk_inst_id：实例id
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_supplier_account": "0",
            "bk_obj_id": bk_obj_id,
            "bk_inst_id": bk_inst_id
        }
        data = self.client.cc.search_inst_association_topo(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("查询实例关联拓扑失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def search_inst_asst_object_inst_base_info(self, bk_obj_id, bk_inst_id, association_obj_id, is_target_object=False):
        """
        查询实例关联模型实例基本信息
        :param bk_obj_id：模型id
        :param bk_inst_id：实例ID
        :param association_obj_id：关联对象的模型ID
        :param is_target_object：bk_obj_id 是否为目标模型， 默认false， 关联关系中的源模型，否则是目标模型
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_supplier_account": "0",
            "condition": {
                "bk_obj_id": bk_obj_id,
                "bk_inst_id": bk_inst_id,
                "association_obj_id": association_obj_id,
                "is_target_object": is_target_object
            },
            "page": {
                "start": 0,
                "limit": 500,
            }
        }
        data = self.client.cc.search_inst_asst_object_inst_base_info(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['info']
        else:
            logger.error("查询实例关联模型实例基本信息失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def search_inst_by_object(self, bk_obj_id):
        """
        查询给定模型的实例信息
        :param bk_obj_id：模型id
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_supplier_account": "0",
            "bk_obj_id": bk_obj_id,
            "fields": [
            ],
            "condition": {
            },
            "page": {
                "start": 0,
                "limit": 500,
            }
        }
        data = self.client.cc.search_inst_by_object(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['info']
        else:
            logger.error("查询给定模型的实例信息失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def search_module(self, bk_biz_id: int, bk_set_id=None, condition={}):
        """
        查询模块
        :param bk_biz_id:
        :param bk_set_id:
        :param condition:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
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
            logger.error("获取模块失败 %s" % data['message'])

        result['message'] = data['message']
        return result

    def search_objects(self, creator="", modifier="", bk_classification_id="", bk_obj_id="", bk_supplier_account=""):
        """
        根据可选条件查询模型
        :param creator: 本条数据创建者
        :param modifier: 	最后修改人员
        :param bk_classification_id: 对象模型的分类ID
        :param bk_obj_id: 	对象模型的ID，
        :param bk_supplier_account: 对象模型的名字
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "creator": creator,
            "modifier": modifier,
            "bk_classification_id": bk_classification_id,
            "bk_obj_id": bk_obj_id,
            "bk_supplier_account": bk_supplier_account
        }

        # 清除空值key
        for key in list(kwargs.keys()):
            if not kwargs[key]:
                kwargs.pop(key)

        data = self.client.cc.search_objects(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("根据可选条件查询模型失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def search_object_attribute(self, bk_biz_id, bk_obj_id):
        """
        可通过可选参数根据模型id或业务id查询对象模型属性
        :param bk_biz_id: 业务ID
        :param bk_obj_id: 对象模型的ID，
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_obj_id": bk_obj_id,
            "bk_supplier_account": "0",
            "bk_biz_id": bk_biz_id
        }

        data = self.client.cc.search_object_attribute(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("可通过可选参数根据模型id或业务id查询对象模型属性失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def search_object_topo(self, bk_classification_id):
        """
        通过对象模型的分类ID查询普通模型拓扑
        :param bk_classification_id：对象模型的分类ID
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_classification_id": bk_classification_id
        }
        data = self.client.cc.search_object_topo(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("通过对象模型的分类ID查询普通模型拓扑失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def search_related_inst_asso(self, bk_inst_id, bk_obj_id):
        """
        查询某实例所有的关联关系
        :param bk_inst_id：实例id
        :param bk_obj_id：模型id
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "condition": {
                "bk_inst_id": bk_inst_id,
                "bk_obj_id": bk_obj_id
            },
            "fields": [
                "id",
                "bk_inst_id",
                "bk_obj_id",
                "bk_asst_inst_id",
                "bk_asst_obj_id",
                "bk_obj_asst_id",
                "bk_asst_id"
            ]
        }
        data = self.client.cc.search_related_inst_asso(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['info']
        else:
            logger.error("查询某实例所有的关联关系失败：%s" % data['message'])

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
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
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
            logger.error("获取集群失败 %s" % data['message'])

        result['message'] = data['message']
        return result

    def search_subscription(self, condition={}):
        """
        查询事件订阅
        :param condition:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_supplier_account": "0",
            "page": {
                "start": 0,
                "limit": 200,
                "sort": "HostName"
            },
            "condition": condition,
        }
        data = self.client.cc.search_subscription(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result["result"] = data['result']
            result['data'] = data['data']['info']
        else:
            logger.error("查询事件订阅失败 %s" % data['message'])

        result['message'] = data['message']
        return result

    def search_topo_tree(self, bk_biz_id, bk_biz_name, bk_set_name="", bk_module_name="", bk_level={}):
        """
        根据业务名、自定义层级名、集群、模块名模糊搜索业务的拓扑树。

        主机规则包括： - 在多业务搜索下，如果扫描的业务数量超过一定数量，可以直接拒绝搜索，直接返回，报查询数据过多的错误，暂定为20个业务。
         - 可以支持业务名、自定义层级名、集群、模块组合的查询方式进行模糊搜索。
        - 除主机、模块外，其它的这些可以提供当前层级或者下一层级的拓扑信息，但是总的搜索的节点数量不能超过50个。如果超过50个，则直接拒绝搜索，报查询数据过多的错误。

        注意： - 该接口仅用于web页面搜索使用，不建议后台使用。
        - 该接口有5分钟的缓存，在最极端的情况下，5分钟内的数据可能会不对。
         - 每次搜索会自动触发缓存更新，所以在数据不对的情况下，第二次搜索数据即准确。
        :param bk_biz_id:业务ID
        :param bk_biz_name : 业务名称
        :param bk_set_name : 集群名称
        :param bk_module_name : 模块名称
        :param bk_level : 自定义层级描述
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_biz_name": bk_biz_name,
            "bk_set_name": bk_set_name,
            "bk_module_name": bk_module_name,
            "bk_level": bk_level
        }
        # 清除空值key
        for key in list(kwargs.keys()):
            if not kwargs[key]:
                kwargs.pop(key)

        data = self.client.cc.search_topo_tree(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result["result"] = data['result']
            result['data'] = data['data']
        else:
            logger.error("模糊搜索业务的拓扑树失败 %s" % data['message'])

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
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
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
            logger.error(u'查询主机列表失败：%s' % result.get('message'))

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
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
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
            logger.error("获取模块下主机失败：%s" % data['message'])
        result['message'] = data['message']
        return result

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
    return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
