import json
from datetime import datetime

from config import APP_CODE as app_code, SECRET_KEY as app_secret
from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from blueapps.utils.logger import logger


class MONITOR_API:
    def __init__(self, bk_token, client):
        self.bk_token = bk_token
        self.client = client

    def reload(self, bk_token, request):
        self.bk_token = bk_token
        self.client = get_client_by_request(request)

    def add_shield(self, bk_biz_id: int, category, description, begin_time, end_time, cycle_config, dimension_config, shield_notice=True,
                   notice_config={}):
        """
        创建屏蔽配置
        :param bk_biz_id: 业务ID
        :param category: 屏蔽类型
        :param description: 说明
        :param begin_time: 开始时间
        :param end_time: 结束时间
        :param cycle_config: 屏蔽配置
        :param shield_notice: 是否发送屏蔽通知
        :param notice_config: 通知配置
        :param dimension_config: 屏蔽维度
        :return:
        """

        # cycle_config={
        #     "begin_time": "",
        #     "end_time": "",
        #     "day_list": [],
        #     "week_list": [],
        #     "type": 1
        # }
        # notice_config={
        #     "notice_time": 5,
        #     "notice_way": ["weixin"],
        #     "notice_receiver": [
        #         {
        #             "id": "user1",
        #             "type": "user"
        #         }
        #     ]
        # }

        # dimension_config={  # 基于范围的屏蔽
        #     "scope_type":"instance",
        #     "target":[8]
        # }
        # dimension_config={  # 基于策略的屏蔽
        #     "id": 1,
        #     "level": [1]
        # }

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "category": category,
            "description": description,
            "begin_time": begin_time,
            "end_time": end_time,
            "cycle_config": cycle_config,
            "shield_notice": shield_notice,
            "notice_config": notice_config,
            "dimension_config": dimension_config,
        }
        data = self.client.monitor.add_shield(kwargs)
        result = {"result": False, "message": "nothing", "id": 0}

        if data.get("result", False):
            result['result'] = data['result']
            result['id'] = data['data']["id"]
        else:
            logger.warning(f"{get_now_time()} 创建屏蔽配置失败：{data['message']} 接口名称(add_shield) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def delete_alarm_strategy(self, bk_biz_id: int, id: int):
        """
        删除告警策略
        :param bk_biz_id: 业务ID
        :param id: 告警ID
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "id": id
        }
        data = self.client.monitor.delete_alarm_strategy(kwargs)
        result = {"result": False, "message": "nothing","data":{}}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 删除告警策略失败：{data['message']} 接口名称(delete_alarm_strategy) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def delete_notice_group(self,ids: list):
        """
        删除通知组
        :param ids: 通知组 ID
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "ids": ids
        }
        data = self.client.monitor.delete_notice_group(kwargs)
        result = {"result": False, "message": "nothing","data":{}}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 删除通知组失败：{data['message']} 接口名称(delete_notice_group) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def disable_shield(self, id:int):
        """
        删除屏蔽配置
        :param id: 告警ID
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "id": id
        }
        data = self.client.monitor.disable_shield(kwargs)
        result = {"result": False, "message": "nothing","data":{}}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 删除屏蔽配置失败：{data['message']} 接口名称(disable_shield) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def edit_shield(self, bk_biz_id: int,id, category, description, begin_time, end_time, cycle_config, shield_notice=True,
                   notice_config={},level=None):
        """
        编辑屏蔽配置
        :param bk_biz_id: 业务ID
        :param id: 告警ID
        :param category: 屏蔽类型
        :param description: 说明
        :param begin_time: 开始时间
        :param end_time: 结束时间
        :param cycle_config: 屏蔽配置
        :param shield_notice: 是否发送屏蔽通知
        :param notice_config: 通知配置
        :param level: 屏蔽策略的等级
        :return:
        """
        # cycle_config={
        #     "begin_time": "",
        #     "end_time": "",
        #     "day_list": [],
        #     "week_list": [],
        #     "type": 1
        # }
        # notice_config={
        #     "notice_time": 5,
        #     "notice_way": ["weixin"],
        #     "notice_receiver": [
        #         {
        #             "id": "user1",
        #             "type": "user"
        #         }
        #     ]
        # }

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "id": id,
            "category": category,
            "description": description,
            "begin_time": begin_time,
            "end_time": end_time,
            "cycle_config": cycle_config,
            "shield_notice": shield_notice,
            "notice_config": notice_config,
            "level": level,
        }
        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key]:
                kwargs.pop(param_key)

        data = self.client.monitor.edit_shield(kwargs)
        result = {"result": False, "message": "nothing", "id": 0}

        if data.get("result", False):
            result['result'] = data['result']
            result['id'] = data['data']["id"]
        else:
            logger.warning(f"{get_now_time()} 编辑屏蔽配置失败：{data['message']} 接口名称(edit_shield) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def export_uptime_check_task(self, bk_biz_id: int, task_ids="", protocol="TCP", node_conf_needed=1):
        """
        拨测任务配置导出
        :param bk_biz_id:int	是	业务id
        :param task_ids:str	否	任务ID，多个任务以逗号分隔
        :param protocol:str	否	协议类型(TCP、UDP、HTTP)
        :param node_conf_needed:int	否	是否导出任务相关的节点配置信息，0或1,默认为1
        :return:result
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "task_ids": task_ids,
            "protocol": protocol,
            "node_conf_needed": node_conf_needed,
        }
        data = self.client.monitor.export_uptime_check_task(kwargs)

        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 拨测任务配置导出失败：{data['message']} 接口名称(export_uptime_check_task) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def get_collect_config_list(self):
        """
        采集配置列表
        :param:

        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token
        }
        data = self.client.monitor.get_collect_config_list(kwargs)

        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result['result'] = data['result']
        else:
            logger.warning(f"{get_now_time()} 采集配置列表失败：{data['message']} 接口名称(get_collect_config_list) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def get_collect_status(self):
        """
        查询采集配置节点状态
        :param:

        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token
        }
        data = self.client.monitor.get_collect_status(kwargs)

        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result['result'] = data['result']
        else:
            logger.warning(f"{get_now_time()} 查询采集配置节点状态失败：{data['message']} 接口名称(get_collect_status) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def get_es_data(self):
        """
        获取监控链路时序数据
        :param:

        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token
        }
        data = self.client.monitor.get_es_data(kwargs)

        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result['result'] = data['result']
        else:
            logger.warning(f"{get_now_time()} 获取监控链路时序数据失败：{data['message']} 接口名称(get_es_data) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def get_event_log(self, id: int):
        """
        查询事件流转记录
        :param id: 事件ID
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "id": id
        }
        data = self.client.monitor.get_event_log(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 查询事件流转记录失败：{data['message']} 接口名称(get_event_log) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def get_shield(self,bk_biz_id: int, id: int):
        """
        获取告警屏蔽
        :param bk_biz_id: 业务ID
        :param id: 屏蔽ID
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "id": id,
            "bk_biz_id": bk_biz_id
        }
        data = self.client.monitor.get_shield(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 获取告警屏蔽失败：{data['message']} 接口名称(get_shield) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def get_ts_data(self, sql, bk_username, prefer_storage="influxdb"):
        """
        图表数据查询
        :param sql:string	是	SQL查询语句
        :param prefer_storage:string	否	查询引擎(默认influxdb)
        :param bk_username:string	否	白名单的app_code必填
        :return:result
        """
        kwargs = {
            "bk_token": self.bk_token,
            "sql": sql,
            "prefer_storage": prefer_storage,
            "bk_username": bk_username,
        }

        data = self.client.monitor.get_ts_data(kwargs)
        save_json("1",data)
        result = {"result": False, "message": "nothing"}
        if data.get("result", False):
            result['result'] = data['result']
            result['device'] = data['data']['device']
            result['list'] = data['data']['list']
            result['timetaken'] = data['data']['timetaken']
        else:
            logger.warning(f"{get_now_time()} 图表数据查询失败：{data['message']} 接口名称(get_ts_data) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    # todo
    def get_uptime_check_node_list(self):
        """
        拨测节点列表
        :param:

        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token
        }
        data = self.client.monitor.get_uptime_check_node_list(kwargs)

        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result['result'] = data['result']
        else:
            logger.warning(f"{get_now_time()} 拨测节点列表失败：{data['message']} 接口名称(get_uptime_check_node_list) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def get_uptime_check_task_list(self):
        """
        拨测任务列表
        :param:

        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token
        }
        data = self.client.monitor.get_uptime_check_task_list(kwargs)

        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result['result'] = data['result']
        else:
            logger.warning(f"{get_now_time()} 拨测任务列表失败：{data['message']} 接口名称(get_uptime_check_task_list) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def import_uptime_check_node(self, conf_list=[]):
        """
        导入拨测节点配置
        :param conf_list:list	是	节点列表
        :return:result
        """
        # conf_list=[{
        #     "node_conf": {
        #         "carrieroperator": "电信",
        #         "location": {
        #             "country": "中国",
        #             "city": "广东"
        #         },
        #         "name": "中国广东电信",
        #         "is_common": False
        #     },
        #     "target_conf": {
        #         "bk_biz_id": 2,
        #         "bk_cloud_id": 0,
        #         "ip": "172.27.1.63"
        #     }
        # }]
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "conf_list": conf_list
        }

        data = self.client.monitor.import_uptime_check_node(kwargs)
        result = {"result": False, "message": "nothing", "failed": {}, "success": {}}
        if data.get("result", False):
            result['result'] = data['result']
            result['failed'] = data['data']['failed']['detail']
            result['success'] = data['data']['success']['detail']
        else:
            logger.warning(f"{get_now_time()} 导入拨测节点配置失败：{data['message']} 接口名称(import_uptime_check_node) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    def import_uptime_check_task(self, bk_biz_id: int, conf_list=[]):
        """
        导入拨测任务配置
        :param bk_biz_id:int 是	业务ID
        :param conf_list:list 是 节点列表
        :return:result
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "conf_list": conf_list
        }

        data = self.client.monitor.import_uptime_check_task(kwargs)

        result = {"result": False, "message": "nothing", "failed": {}, "success": {}}
        if data.get("result", False):
            result['result'] = data['result']
            result['failed'] = data['data']['failed']['detail']
            result['success'] = data['data']['success']['detail']
        else:
            logger.warning(f"{get_now_time()} 导入拨测任务配置失败：{data['message']} 接口名称(import_uptime_check_task) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    def list_shield(self, bk_biz_id: int, is_active, time_start, time_end, page=1, page_size=10):
        """
        获取告警屏蔽列表
        :param bk_biz_id: 	业务ID
        :param is_active: 是否生效
        :param time_start: 	开始时间
        :param time_end: 结束时间
        :param page:    页数
        :param page_size: 每页数量
        :return:result
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "is_active": is_active,
            "time_range": f"{time_start} -- {time_end}",
            "page": page,
            "page_size": page_size
        }

        data = self.client.monitor.list_shield(kwargs)
        result = {"result": False, "message": "nothing", "data":[]}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']['shield_list']
        else:
            logger.warning(f"{get_now_time()} 获取告警屏蔽列表失败：{data['message']} 接口名称(list_shield) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    def metadata_create_cluster_info(self, cluster_name, cluster_type, domain_name, port, operator, description="",
                                     auth_info={}, version="", custom_label="", schema="", is_ssl_verify=False):
        """
        创建存储集群信息
        :param cluster_name: 	存储集群名
        :param cluster_type: 存储集群类型, 目前可以支持 influxDB, kafka, redis, elasticsearch
        :param domain_name: 	存储集群域名（可以填入 IP）
        :param port:    存储集群端口
        :param operator: 创建者
        :param description: 存储集群描述信息
        :param auth_info: 集群身份验证信息
        :param version: 集群版本信息
        :param custom_label: 自定义标签
        :param schema: 强行配置 schema，可用于配置 https 等情形
        :param is_ssl_verify: 是否需要跳过 SSL\TLS 认证
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "cluster_name": cluster_name,
            "cluster_type": cluster_type,
            "domain_name": domain_name,
            "operator": operator,
            "auth_info": auth_info,
            "port": port,
            "description": description,
            "version": version,
            "custom_label": custom_label,
            "schema": schema,
            "is_ssl_verify": is_ssl_verify
        }
        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key]:
                kwargs.pop(param_key)

        data = self.client.monitor.metadata_create_cluster_info(kwargs)
        result = {"result": False, "message": "nothing", "data":[]}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 创建存储集群信息失败：{data['message']} 接口名称(metadata_create_cluster_info) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    # todo error: interface response is not the JSON format, please try again later or contact component developer to handle this
    def metadata_create_data_id(self, data_name, etl_config,operator, source_label, type_label,mq_cluster=0,
                                data_description="", is_custom_source=True, custom_label="", option=""):
        """
        创建监控数据源
        :param data_name: 	数据源名称
        :param etl_config: 清洗模板配置，prometheus exportor 对应"prometheus"
        :param operator: 操作者
        :param mq_cluster: 数据源使用的消息集群
        :param data_description: 数据源的具体描述
        :param is_custom_source: 是否用户自定义数据源，默认为是
        :param source_label: 数据来源标签，例如：计算平台(bk_data)，监控采集器(bk_monitor_collector)
        :param type_label: 数据类型标签，例如：时序数据(time_series)，事件数据(event)，日志数据(log)
        :param custom_label: 自定义标签配置信息
        :param option: 数据源配置选项内容，格式为{option_name: option_value}
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "data_name": data_name,
            "etl_config": etl_config,
            "operator": operator,
            "mq_cluster": mq_cluster,
            "data_description": data_description,
            "is_custom_source": is_custom_source,
            "source_label": source_label,
            "type_label": type_label,
            "custom_label": custom_label,
            "option": option
        }
        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key]:
                kwargs.pop(param_key)
        data = self.client.monitor.metadata_create_data_id(kwargs)

        result = {"result": False, "message": "nothing", "bk_data_id": 0}
        if data.get("result", False):
            result['result'] = data['result']
            result['bk_data_id'] = data['data']['bk_data_id']
        else:
            logger.warning(f"{get_now_time()} 创建监控数据源失败：{data['message']} 接口名称(metadata_create_data_id) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    # todo
    def metadata_create_event_group(self, bk_data_id, bk_biz_id,event_group_name, label, operator,event_info_list):
        """
        创建事件分组
        :param bk_data_id: 	数据源 ID
        :param bk_biz_id: 业务 ID
        :param event_group_name: 事件分组名
        :param label: 事件分组标签，用于表示事件监控对象，应该复用【result_table_label】类型下的标签
        :param operator: 操作者
        :param event_info_list: 事件列表
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_data_id": bk_data_id,
            "bk_biz_id": bk_biz_id,
            "event_group_name": event_group_name,
            "label": label,
            "operator": operator,
            "event_info_list": event_info_list
        }
        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key]:
                kwargs.pop(param_key)

        data = self.client.monitor.metadata_create_event_group(kwargs)

        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 创建事件分组失败：{data['message']} 接口名称(metadata_create_event_group) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    # todo
    def metadata_create_result_table(self, bk_biz_id: int, bk_data_id: int, table_id, table_name_zh,
                                     is_custom_table=True,
                                     schema_type="fixed", operator="admin", default_storage="influxdb",
                                     default_storage_config={}, field_list=[]):
        """
        创建监控结果表
        :param bk_biz_id:int	否	业务ID，默认是0全局
        :param bk_data_id:int	是	数据源ID
        :param table_id:string	是	结果表ID，格式应该为 库.表(例如，system.cpu)
        :param table_name_zh:string	是	结果表中文名
        :param is_custom_table:boolean	是	是否用户自定义结果表
        :param schema_type:string	是	结果表字段配置方案, free(无schema配置), fixed(固定schema)
        :param operator:string	是	操作者
        :param default_storage:string	是	默认存储类型，目前支持influxdb
        :param default_storage_config:object	否	默认的存储信息, 根据每种不同的存储会有不同的配置内容
        :param field_list:array	否	字段信息，数组元素为dict，例:field_name(字段名), field_type(字段类型), tag(字段类型, metirc -- 指标, dimension -- 维度)
        :return:result
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_data_id": bk_data_id,
            "table_id": table_id,
            "table_name_zh": table_name_zh,
            "is_custom_table": is_custom_table,
            "schema_type": schema_type,
            "operator": operator,
            "default_storage": default_storage,
            "default_storage_config": default_storage_config,
            "field_list": field_list
        }

        data = self.client.monitor.metadata_create_result_table(kwargs)
        result = {"result": False, "message": "nothing", "table_id": ""}

        if data.get("result", False):
            result['result'] = data['result']
            result['table_id'] = data['data']['table_id']

        else:
            logger.warning(
                f"{get_now_time()} 创建监控结果表失败：{data['message']} 接口名称(metadata_create_result_table) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result
    # todo
    def metadata_create_result_table_metric_split(self, table_id, cmdb_level,operator="admin"):
        """
        创建结果表的维度拆分配置
        :param table_id:string	是	结果表ID
        :param cmdb_level:string 是	CMDB 拆分层级名
        :param operator:string	是	操作者
        :return:result
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "table_id": table_id,
            "cmdb_level": cmdb_level,
            "operator": operator
        }

        data = self.client.monitor.metadata_create_result_table_metric_split(kwargs)
        result = {"result": False, "message": "nothing", "bk_data_id": None, "table_id": None}

        if data.get("result", False):
            result['result'] = data['result']
            result['bk_data_id'] = data['data']['bk_data_id']
            result['table_id'] = data['data']['table_id']

        else:
            logger.warning(f"{get_now_time()} 创建结果表的维度拆分配置失败：{data['message']} 接口名称(metadata_create_result_table_metric_split) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def metadata_create_time_series_group(self):
        """
        创建自定义时序分组
        :param:

        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token
        }
        data = self.client.monitor.metadata_create_time_series_group(kwargs)

        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result['result'] = data['result']
        else:
            logger.warning(f"{get_now_time()} 创建自定义时序分组失败：{data['message']} 接口名称(metadata_create_time_series_group) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def metadata_delete_event_group(self, event_group_id: int, operator="admin"):
        """
        删除事件分组
        :param:event_group_id:	事件分组 ID
        :param:operator:操作者

        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "event_group_id": event_group_id,
            "operator": operator
        }
        data = self.client.monitor.metadata_delete_event_group(kwargs)

        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 删除事件分组失败：{data['message']} 接口名称(metadata_delete_event_group) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def metadata_delete_time_series_group(self):
        """
        删除自定义时序分组
        :param:

        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token
        }
        data = self.client.monitor.metadata_delete_time_series_group(kwargs)

        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 删除自定义时序分组失败：{data['message']} 接口名称(metadata_delete_time_series_group) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def metadata_get_cluster_info(self):
        """
        查询指定存储集群信息
        :param:

        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token
        }
        data = self.client.monitor.metadata_get_cluster_info(kwargs)

        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 查询指定存储集群信息失败：{data['message']} 接口名称(metadata_get_cluster_info) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def metadata_get_data_id(self, bk_data_id: int, data_name=""):
        """
        获取监控数据源具体信息
        :param bk_data_id:int	否	数据源ID
        :param data_name:string	否	数据源名称
        :return:result
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_data_id": bk_data_id,
            "data_name": data_name
        }

        data = self.client.monitor.metadata_get_data_id(kwargs)
        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(
                f"{get_now_time()} 获取监控数据源具体信息失败：{data['message']} 接口名称(metadata_get_data_id) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def metadata_get_event_group(self, event_group_id: int, with_result_table_info=True):
        """
        查询事件分组具体内容
        :param event_group_id:int	否	事件分组 ID
        :param with_result_table_info:bool	否	事件分组存储信息
        :return:result
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "event_group_id": event_group_id,
            "with_result_table_info": with_result_table_info
        }

        data = self.client.monitor.metadata_get_event_group(kwargs)
        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 查询事件分组具体内容失败：{data['message']} 接口名称(metadata_get_event_group) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def metadata_get_result_table(self, table_id: str):
        """
        获取监控结果表具体信息
        :param table_id:string	是	结果表ID
        :return:result
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "table_id": table_id
        }

        data = self.client.monitor.metadata_get_result_table(kwargs)
        result = {"result": False, "message": "nothing", "data": {}}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 获取监控结果表具体信息失败：{data['message']} 接口名称(metadata_get_result_table) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def metadata_get_result_table_storage(self, result_table_list: str,storage_type: str):
        """
        查询指定结果表的指定存储信息
        :param result_table_list:string	是	结果表 ID
        :param storage_type:string	是	存储类型
        :return:result
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "result_table_list": result_table_list,
            "storage_type": storage_type
        }

        data = self.client.monitor.metadata_get_result_table_storage(kwargs)
        result = {"result": False, "message": "nothing", "data": {}}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 查询指定结果表的指定存储信息失败：{data['message']} 接口名称(metadata_get_result_table_storage) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def metadata_get_time_series_group(self):
        """
        获取自定义时序分组具体内容
        :param:

        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token
        }
        data = self.client.monitor.metadata_get_time_series_group(kwargs)

        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 获取自定义时序分组具体内容失败：{data['message']} 接口名称(metadata_get_time_series_group) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def metadata_get_time_series_metrics(self):
        """
        获取自定义时序结果表的 metrics 信息
        :param:

        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token
        }
        data = self.client.monitor.metadata_get_time_series_metrics(kwargs)

        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 获取自定义时序结果表的 metrics 信息失败：{data['message']} 接口名称(metadata_get_time_series_metrics) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def metadata_list_result_table(self, bk_biz_id: int, is_public_include=0, datasource_type="",is_config_by_user=False):
        """
        查询监控结果表
        :param bk_biz_id:int false	获取指定业务下的结果表信息
        :param is_public_include:int false	是否包含全业务结果表, 0为不包含, 非0为包含全业务结果表
        :param datasource_type:string false	需要过滤的结果表类型, 如system
        :param is_config_by_user:string false		是否需要包含非用户配置的结果表内容
        :return:result
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "is_public_include": is_public_include,
            "datasource_type": datasource_type,
            "is_config_by_user": is_config_by_user
        }

        data = self.client.monitor.metadata_list_result_table(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 查询监控结果表失败：{data['message']} 接口名称(metadata_list_result_table) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def metadata_modify_cluster_info(self,cluster_id,cluster_name, operator, description="",auth_info={}, custom_label="", schema="", is_ssl_verify=False):
        """
        修改存储集群信息
        :param cluster_id: 	集群 ID
        :param cluster_name: 	存储集群名
        :param operator: 修改者
        :param description: 存储集群描述信息
        :param auth_info: 集群身份验证信息
        :param custom_label: 自定义标签
        :param schema: 强行配置 schema，可用于配置 https 等情形
        :param is_ssl_verify: 是否需要跳过 SSL\TLS 认证
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "cluster_id": cluster_id,
            "cluster_name": cluster_name,
            "operator": operator,
            "description": description,
            "auth_info": auth_info,
            "custom_label": custom_label,
            "schema": schema,
            "is_ssl_verify": is_ssl_verify
        }
        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key]:
                kwargs.pop(param_key)

        data = self.client.monitor.metadata_modify_cluster_info(kwargs)

        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 修改存储集群信息失败：{data['message']} 接口名称(metadata_modify_cluster_info) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def metadata_modify_data_id(self,data_name,data_id, operator, source_label,type_label):
        """
        修改存储集群信息
        :param data_name: 数据源名称
        :param data_id: 数据源 ID
        :param operator: 操作者
        :param source_label: 数据来源标签，例如：计算平台(bk_data)，监控采集器(bk_monitor_collector)
        :param type_label: 数据类型标签，例如：时序数据(time_series)，事件数据(event)，日志数据(log)
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "data_name":data_name,
            "data_id": data_id,
            "operator": operator,
            "source_label": source_label,
            "type_label": type_label
        }
        data = self.client.monitor.metadata_modify_data_id(kwargs)

        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 修改存储集群信息失败：{data['message']} 接口名称(metadata_modify_data_id) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def metadata_modify_event_group(self,event_group_id,event_group_name, label="", operator="admin",event_info_list=[],is_enable=False):
        """
        修改事件分组
        :param event_group_id: 事件组 ID
        :param event_group_name: 事件分组名
        :param label: 事件分组标签，用于表示事件监控对象，应该复用【result_table_label】类型下的标签
        :param operator: 操作者
        :param event_info_list: 事件列表
        :param is_enable: 是否停用事件组
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "event_group_id":event_group_id,
            "event_group_name": event_group_name,
            "label": label,
            "operator": operator,
            "event_info_list": event_info_list,
            "is_enable": is_enable
        }
        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key]:
                kwargs.pop(param_key)

        data = self.client.monitor.metadata_modify_event_group(kwargs)

        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 修改事件分组失败：{data['message']} 接口名称(metadata_modify_event_group) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def metadata_modify_result_table(self, table_id, table_name_zh, field_list, operator="admin",
                                     default_storage="influxdb"):
        """
        修改监控结果表
        :param table_id:string	是	结果表ID，格式应该为 库.表(例如，system.cpu)
        :param table_name_zh:string	是	结果表中文名
        :param operator:string	是	操作者
        :param default_storage:string	是	默认存储类型，目前支持influxdb
        :param field_list:array	否	字段信息，数组元素为dict，例:field_name(字段名), field_type(字段类型), tag(字段类型, metirc -- 指标, dimension -- 维度)
        :return:result
        """
        kwargs = {
            "bk_token": self.bk_token,
            "table_id": table_id,
            "operator": operator,
            "field_list": field_list,
            "table_name_zh": table_name_zh,
            "default_storage": default_storage
        }

        data = self.client.monitor.metadata_modify_result_table(kwargs)
        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 修改监控结果表失败：{data['message']} 接口名称(metadata_modify_result_table) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result
    # todo
    def metadata_modify_time_series_group(self):
        """
        修改自定义时序分组
        :param:

        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token
        }
        data = self.client.monitor.metadata_modify_time_series_group(kwargs)

        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 修改自定义时序分组失败：{data['message']} 接口名称(metadata_modify_time_series_group) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def metadata_query_event_group(self,bk_biz_id=0,label="",event_group_name=""):
        """
        批量查询事件分组信息
        :param:bk_biz_id:	业务 ID
        :param:label:	事件分组标签（监控对象）
        :param:event_group_name:事件分组名称
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "label": label,
            "event_group_name": event_group_name
        }
        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key]:
                kwargs.pop(param_key)
        data = self.client.monitor.metadata_query_event_group(kwargs)

        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 批量查询事件分组信息败：{data['message']} 接口名称(metadata_query_event_group) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def metadata_query_tag_values(self):
        """
        获取自定义时序分组具体内容
        :param:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token
        }
        data = self.client.monitor.metadata_query_tag_values(kwargs)

        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
        else:
            logger.warning(f"{get_now_time()} 批量查询事件分组信息败：{data['message']} 接口名称(metadata_query_tag_values) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def metadata_query_time_series_group(self):
        """
        查询事件分组
        :param:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token
        }
        data = self.client.monitor.metadata_query_time_series_group(kwargs)

        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
        else:
            logger.warning(f"{get_now_time()} 查询事件分组失败：{data['message']} 接口名称(metadata_query_time_series_group) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def metadata_upgrade_result_table(self,table_id,operator):
        """
        将指定的监控单业务结果表升级为全业务结果表
        :param table_id: 结果表 ID
        :param operator: 操作者
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "table_id": table_id,
            "operator": operator
        }
        data = self.client.monitor.metadata_upgrade_result_table(kwargs)

        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
        else:
            logger.warning(f"{get_now_time()} 将指定的监控单业务结果表升级为全业务结果表失败：{data['message']} 接口名称(metadata_upgrade_result_table) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def query_collect_config(self):
        """
        查询采集配置
        :param:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token
        }
        data = self.client.monitor.query_collect_config(kwargs)

        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
        else:
            logger.warning(f"{get_now_time()} 查询采集配置失败：{data['message']} 接口名称(query_collect_config) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def save_alarm_strategy(self, bk_biz_id: str, action_list:list,target:list,item_list:list,name:str,scenario:str):
        """
        创建/更新监控策略
        :param bk_biz_id:int	业务ID
        :param action_list:list	动作列表(Action)
        :param target:list	监控目标
        :param item_list:list	监控项(Item)
        :param name:string	策略名称
        :param scenario:string	监控对象
        :return:result
        """
        kwargs = {
            "bk_biz_id": bk_biz_id,
            "item_list": item_list,
            "target": target,
            "scenario": scenario,
            "action_list": action_list,
            "name": name
        }
        data = self.client.monitor.save_alarm_strategy(kwargs)
        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 保存告警策略失败：{data['message']} 接口名称(save_alarm_strategy) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo
    def save_collect_config(self):

        """
        创建/保存采集配置
        :param:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token
        }
        data = self.client.monitor.save_collect_config(kwargs)

        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
        else:
            logger.warning(f"{get_now_time()} 创建/保存采集配置失败：{data['message']} 接口名称(save_collect_config) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def save_notice_group(self,bk_biz_id,name,message,notice_way,notice_receiver,webhook_url="",id=0,):
        """
        保存通知组
        :param bk_biz_id:业务 ID
        :param name: 名称
        :param message: 说明
        :param webhook_url: 回调地址
        :param notice_way:	各个级别的通知方式
        :param id: 告警组 ID，如果没有则创建
        :param notice_receiver:通知对象列表
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id":bk_biz_id,
            "notice_receiver": notice_receiver,
            "name": name,
            "notice_way": notice_way,
            "webhook_url": webhook_url,
            "message": message,
            "id": id
        }
        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key]:
                kwargs.pop(param_key)

        data = self.client.monitor.save_notice_group(kwargs)
        save_json("1",data)

        result = {"result": False, "message": "nothing", "id": 0}
        if data.get("result", False):
            result['result'] = data['result']
            result['id'] = data['data']['id']
        else:
            logger.warning(f"{get_now_time()} 保存通知组失败：{data['message']} 接口名称(save_notice_group) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def search_alarm_strategy(self,bk_biz_id:int,ids=[], metric_id="", fields=[],page=0, page_size=0):
        """
        查询告警策略
        :param bk_biz_id:	业务 ID
        :param ids: 策略 ID 列表
        :param metric_id: 指标 ID
        :param fields: 所需字段
        :param page:页码
        :param page_size: 每页条数
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id":bk_biz_id,
            "ids": ids,
            "metric_id": metric_id,
            "fields": fields,
            "page": page,
            "page_size": page_size
        }

        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key]:
                kwargs.pop(param_key)

        data = self.client.monitor.search_alarm_strategy(kwargs)

        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 查询告警策略失败：{data['message']} 接口名称(search_alarm_strategy) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def search_event(self,bk_biz_ids:list, time_start="", time_end="", days=0, conditions={}):
        """
        查询事件
        :param bk_biz_ids:	业务 ID 列表
        :param time_start: 事件启动的时间
        :param time_end: 事件结束的时间
        :param days:    查询最近几天内的时间，这个参数存在，time_range 则失效
        :param conditions: 查询条件
        :return:
        """
        # conditions=[
        #     {
        #         "key": "event_status",
        #         "value": ["RECOVERED"]
        #     }
        # ]
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_ids":bk_biz_ids,
            "days": days,
            "conditions": conditions
        }
        if time_start and time_end:
            kwargs["time_range"] = f"{time_start} -- {time_end}"

        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key]:
                kwargs.pop(param_key)

        data = self.client.monitor.search_event(kwargs)

        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 查询事件失败：{data['message']} 接口名称(search_event) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def search_notice_group(self,bk_biz_ids=[], ids=[]):
        """
        查询告警组
        :param bk_biz_ids:	业务 ID 列表
        :param ids:	通知组 ID
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_ids": bk_biz_ids,
            "ids": ids
        }

        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key]:
                kwargs.pop(param_key)

        data = self.client.monitor.search_notice_group(kwargs)

        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 查询告警组失败：{data['message']} 接口名称(search_notice_group) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def switch_alarm_strategy(self, is_enabled, ids):
        """
        启停告警策略
        :param is_enabled: bool	是否开启
        :param ids: list	策略 ID 列表
        :return:
        """

        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "is_enabled": is_enabled,
            "ids": ids
        }
        data = self.client.monitor.switch_alarm_strategy(kwargs)

        result = {"result": False, "message": "nothing", "ids": []}
        if data.get("result", False):
            result['result'] = data['result']
            result['ids'] = data['data']['ids']
        else:
            logger.warning(f"{get_now_time()} 启停告警策略失败：{data['message']} 接口名称(switch_alarm_strategy) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

def save_json(filename, data):
    with open(f"{filename}.json", "w", encoding="utf-8")as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))


def make_time(time_str):
    return time_str[:time_str.rfind("+")]


def get_now_time():
    return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")


def make_monitor_time(time_str):
    return time_str[:time_str.rfind("+")]
