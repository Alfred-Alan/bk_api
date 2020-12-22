import base64
import json
import logging
import time
from datetime import datetime

from config import APP_CODE as app_code, SECRET_KEY as app_secret
from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from blueapps.utils.logger import logger


class MONITOR_API:
    def __init__(self, username):
        self.bk_token = ''
        self.client = get_client_by_user(username)

    def reload(self, bk_token, request):
        self.bk_token = bk_token
        self.client = get_client_by_request(request)

    def alarm_instance(self, id: int):
        """
        返回指定告警
        :param id:	int	是	告警ID
        :return:result
        """
        kwargs = {
            "bk_token": self.bk_token,
            "id": id
        }
        data = self.client.monitor.alarm_instance(kwargs)

        result = {"result": False, "message": "nothing", "data": {}}

        if data.get("result", False):
            result['result'] = data['result']
            result['data']["bk_biz_id"] = data['data']['bk_biz_id']  # 业务ID
            result['data']["bk_cloud_id"] = data['data']['bk_cloud_id']  # 云区域ID
            result['data']["bk_supplier_id"] = data['data']['bk_supplier_id']  # 开发商ID
            result['data']["alarm_attr_id"] = data['data']['alarm_attr_id']  # 监控ID
            result['data']["alarm_source_id"] = data['data']['alarm_source_id']  # 告警源ID
            result['data']["id"] = data['data']['id']  # 告警ID
            result['data']["ip"] = data['data']['ip']  # 主机IP
            result['data']["raw"] = data['data']['raw']  # 告警内容
            result['data']["level"] = data['data']['level']  # 告警等级
            result['data']["status"] = data['data']['status']  # 状态
            result['data']["comment"] = data['data']['comment']  # 备注
            result['data']["alarm_type"] = data['data']['alarm_type']  # 告警类型
            result['data']["source_type"] = data['data']['source_type']  # 告警源类型
            result['data']["origin_alarm"] = data['data']['origin_alarm']  # 告警源数据
            result['data']["alarm_content"] = data['data']['alarm_content']  # 告警内容
            result['data']["snap_alarm_source"] = data['data']['snap_alarm_source']  # 告警源配置快照

            result['data']["begin_time"] = make_time(data['data']['begin_time'])  # 处理开始时间
            result['data']["end_time"] = make_time(data['data']['end_time'])  # 处理结束时间
            result['data']["source_time"] = make_time(data['data']['source_time'])  # 告警发生时间

            result['data']["source_id"] = data['data']['source_id']  # 告警特征ID
            result['data']["event_id"] = data['data']['event_id']  # 关联事件ID
            result['data']["priority"] = data['data']['priority']  # 告警优先级
            result['data']["user_status"] = data['data']['user_status']  # 告警外部状态
        else:
            logger.warning(
                f"{get_now_time()} 返回指定告警失败：{data['message']} 接口名称(alarm_instance) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def component_instance(self, id: int):
        """
        返回指定id的组件实例
        :param id:int 是 组件ID
        :return:result
        """
        kwargs = {
            "bk_token": self.bk_token,
            "id": id
        }
        data = self.client.monitor.component_instance(kwargs)
        result = {"result": False, "message": "nothing", "data": {}}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']

        else:
            logger.warning(
                f"{get_now_time()} 返回指定组件失败：{data['message']} 接口名称(component_instance) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def delete_alarm_strategy(self):
        """
        删除监控策略
        :param :
        :return:
        """
        pass
        # kwargs = {
        #     "bk_token": self.bk_token,
        # }
        # data = self.client.monitor.delete_alarm_strategy(kwargs)
        # result = {"result": False, "message": "nothing", "data": {}}
        #
        # if data.get("result", False):
        #     result['result'] = data['result']
        #     result['data'] = data['data']
        #
        # else:
        #     logger.warning(
        #         f"{get_now_time()} 删除监控策略失败：{data['message']} 接口名称(delete_alarm_strategy) 请求参数({kwargs}) 返回参数({data})")
        #
        # result['message'] = data['message']
        #
        # return result

    def deploy_script_collector(self, config_id: int, target_conf: list):
        """
        脚本采集器任务下发
        :param config_id:int	是	脚本采集配置id
        :param target_conf:	list	是	脚本采集实例配置
        :return:result
        """
        # target_conf=[
        #     {
        #         "ip": "x.x.x.x",
        #         "bk_cloud_id": 0,
        #         "params": {}
        #     }
        # ]
        kwargs = {
            "bk_token": self.bk_token,
            "target_conf": target_conf,
            "config_id": config_id,
        }
        data = self.client.monitor.deploy_script_collector(kwargs)
        result = {"result": False, "message": "nothing"}

        if data.get("result", False):
            result['result'] = data['result']
            result['failed'] = data['data']['failed']
            result['success '] = data['data']['success']

        else:
            logger.warning(
                f"{get_now_time()} 脚本采集器任务下发失败：{data['message']} 接口名称(deploy_script_collector) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def export_alarm_strategy(self, bk_biz_id: int, monitor_ids=""):
        """
        监控策略导出
        :param bk_biz_id:string	是	需要导出的监控项ID列表，多个id使用半角逗号连接
        :param monitor_ids:string	是	通用业务ID
        :return:result
        """
        kwargs = {
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "monitor_ids": monitor_ids
        }
        data = self.client.monitor.export_alarm_strategy(kwargs)
        result = {"result": False, "message": "nothing"}
        if data.get("result", False):
            result['result'] = data['result']
            result['fail'] = data['data']['fail']
            result['success'] = data['data']['success']
        else:
            logger.warning(
                f"{get_now_time()} 监控策略导出失败：{data['message']} 接口名称(export_alarm_strategy) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def export_log_collector(self, bk_biz_id: int, ids=""):
        """
        日志采集器配置导出
        :param bk_biz_id:int	是	业务id
        :param ids:string	否	需要导出的配置id，多个id之间用英文逗号隔开
        :return:result
        """
        kwargs = {
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "ids": ids
        }
        data = self.client.monitor.export_log_collector(kwargs)
        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(
                f"{get_now_time()} 日志采集器配置导出失败：{data['message']} 接口名称(export_log_collector) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def export_script_collector(self, bk_biz_id: int, ids=""):
        """
        脚本采集器配置导出
        :param bk_biz_id:int	是	业务id
        :param ids:string	否	多个id用英文逗号隔开
        :return:result
        """
        kwargs = {
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "ids": ids
        }
        data = self.client.monitor.export_script_collector(kwargs)
        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(
                f"{get_now_time()} 脚本采集器配置导出失败：{data['message']} 接口名称(export_script_collector) 请求参数({kwargs}) 返回参数({data})")

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
            logger.warning(
                f"{get_now_time()} 拨测任务配置导出失败：{data['message']} 接口名称(export_uptime_check_task) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def get_alarms(self, bk_biz_id: int, start_time="", end_time="", id=None, alarm_type=None, level=None,
                   alarm_content__contains=dict(), user_status=None, status=None, extend_fields="",
                   ordering="-source_time",
                   page="", page_size=""):
        """
        通过筛选条件获取指定告警事件
        :param bk_biz_id:int 是	业务ID
        :param start_time:string 是 告警源时间，"YYYY-MM-DD hh:mm:ss"
        :param end_time:string 是 告警源时间，"YYYY-MM-DD hh:mm:ss"
        :param id:int 否 告警事件ID
        :param alarm_type:string 否	监控类型，多字段使用半角逗号分隔 详情见alarm_type
        :param level:int 否	监控类型，告警级别，1为致命，2为预警，3为提醒
        :param alarm_content__contains:string	否 从alarm_content字段中匹配
        :param user_status:	string	否	通知状态 "notified,unnotified"
        :param status:string	否	告警状态，可选（待定）
        :param extend_fields:string	否	用户自定义显示的额外字段，多字段使用半角逗号分隔"
        :param ordering:string	否	排序方式，默认为id(升序)，可选source_time,begin_time,end_time，加上"-"前缀为降序
        :param page:int	否	当前页码数，默认为1
        :param page_size:int	否	每页最大显示数，默认为5
        :return:result
        """
        kwargs = {
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "source_time__gte": start_time,
            "source_time__lte": end_time,
            "id": id,
            "alarm_type__in": alarm_type,
            "level": level,
            "alarm_content__contains": alarm_content__contains,
            "user_status__in": user_status,
            "status": status,
            "extend_fields": extend_fields,
            "ordering": ordering,
        }
        if page:
            kwargs["page"]: page
            kwargs["page_size"]: page_size

        data = self.client.monitor.get_alarms(kwargs)
        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result['result'] = data['result']
            for alarm in data['data']['result']:
                alarm['source_time'] = make_time(alarm['source_time'])
                result['data'].append(alarm)
        else:
            logger.warning(
                f"{get_now_time()} 获取指定告警事件失败：{data['message']} 接口名称(get_alarms) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    def get_alarm_strategy(self, bk_biz_id: int, alarm_strategy_id: int):
        """
        查询监控策略详情
        :param bk_biz_id:int 是	业务ID
        :param alarm_strategy_id:int 是	策略ID
        :return:result
        """
        kwargs = {
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "alarm_strategy_id": alarm_strategy_id,
        }

        data = self.client.monitor.get_alarm_strategy(kwargs)
        result = {"result": False, "message": "nothing"}
        if data.get("result", False):
            result['result'] = data['result']
            result.update(data)
        else:
            logger.warning(
                f"{get_now_time()} 查询监控策略详情失败：{data['message']} 接口名称(get_alarm_strategy) 请求参数({kwargs}) 返回参数({data})")
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
        result = {"result": False, "message": "nothing"}
        if data.get("result", False):
            result['result'] = data['result']
            result['device'] = data['data']['device']
            result['list'] = data['data']['list']
            result['timetaken'] = data['data']['timetaken']
        else:
            logger.warning(
                f"{get_now_time()} 图表数据查询失败：{data['message']} 接口名称(get_ts_data) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    def import_alarm_strategy(self, bk_biz_id, conf_list=[]):
        """
        导入监控策略
        :param bk_biz_id:int	是	通用业务ID
        :param conf_list:list	是	导入配置
        :return:result
        """
        kwargs = {
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "conf_list": conf_list
        }

        data = self.client.monitor.import_alarm_strategy(kwargs)
        result = {"result": False, "message": "nothing","fail":[],"success":[]}
        if data.get("result", False):
            result['result'] = data['result']
            result['fail'] = data['data']['fail']
            result['success'] = data['data']['success']
        else:
            logger.warning(
                f"{get_now_time()} 导入监控策略失败：{data['message']} 接口名称(import_alarm_strategy) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    def import_log_collector(self, bk_biz_id, conf_list=[]):
        """
        导入日志采集器配置
        :param bk_biz_id:int	是	通用业务ID
        :param conf_list:list	是	导入配置
        :return:result
        """
        kwargs = {
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "conf_list": conf_list
        }

        data = self.client.monitor.import_log_collector(kwargs)
        result = {"result": False, "message": "nothing","failed":{},"successed":{}}
        if data.get("result", False):
            result['result'] = data['result']
            result['failed'] = data['data']['failed']
            result['successed'] = data['data']['successed']
        else:
            logger.warning(
                f"{get_now_time()} 导入日志采集器配置失败：{data['message']} 接口名称(import_log_collector) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    def import_script_collector(self, collector_conf_list=[]):
        """
        导入脚本采集器配置
        :param collector_conf_list:	list	是	脚本采集任务配置
        :return:result
        """
        kwargs = {
            "bk_token": self.bk_token,
            "collector_conf_list": collector_conf_list
        }

        data = self.client.monitor.import_script_collector(kwargs)
        result = {"result": False, "message": "nothing","failed":{},"success":{}}
        if data.get("result", False):
            result['result'] = data['result']
            result['failed'] = data['data']['failed']
            result['success'] = data['data']['success']
        else:
            logger.warning(
                f"{get_now_time()} 导入脚本采集器配置失败：{data['message']} 接口名称(import_script_collector) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    def import_uptime_check_node(self, conf_list=[]):
        """
        导入拨测节点配置
        :param conf_list:list	是	节点列表
        :return:result
        """
        kwargs = {
            "bk_token": self.bk_token,
            "conf_list": conf_list
        }

        data = self.client.monitor.import_uptime_check_node(kwargs)
        result = {"result": False, "message": "nothing","failed":{},"success":{}}
        if data.get("result", False):
            result['result'] = data['result']
            result['failed'] = data['data']['failed']
            result['success'] = data['data']['success']
        else:
            logger.warning(
                f"{get_now_time()} 导入拨测节点配置失败：{data['message']} 接口名称(import_uptime_check_node) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    def import_uptime_check_task(self, bk_biz_id:int,conf_list=[]):
        """
        导入拨测任务配置
        :param bk_biz_id:int 是	业务ID
        :param conf_list:list 是 节点列表
        :return:result
        """
        kwargs = {
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "conf_list": conf_list
        }

        data = self.client.monitor.import_uptime_check_task(kwargs)
        result = {"result": False, "message": "nothing","failed":{},"success":{}}
        if data.get("result", False):
            result['result'] = data['result']
            result['failed'] = data['data']['failed']
            result['success'] = data['data']['success']
        else:
            logger.warning(
                f"{get_now_time()} 导入拨测任务配置失败：{data['message']} 接口名称(import_uptime_check_task) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    def list_alarm_instance(self, bk_biz_id: int, bk_cloud_id="", id="", bk_supplier_id="0", source_time="", status="",
                            user_status="", event_id=""):
        """
        批量筛选告警
        :param bk_biz_id:int 是	业务ID
        :param bk_cloud_id:int	否	云区域ID
        :param id:int 否 告警ID
        :param bk_supplier_id:int 否	开发商ID
        :param source_time:time 否	告警发生时间
        :param status:string 否	状态
        :param user_status:string 否	告警外部状态
        :param event_id:string 否	关联事件ID
        :return:result
        """
        kwargs = {
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_cloud_id": bk_cloud_id,
            "bk_supplier_id": bk_supplier_id,
            "source_time": source_time,
            "status": status,
            "id": id,
            "user_status": user_status,
            "event_id": event_id,
        }
        data = self.client.monitor.list_alarm_instance(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            for alarm in data['data']:
                result['data'].append({
                    "bk_biz_id": alarm['bk_biz_id'],  # 业务ID
                    "bk_cloud_id": alarm['bk_cloud_id'],  # 云区域ID
                    "bk_supplier_id": alarm['bk_supplier_id'],  # 开发商ID
                    "alarm_attr_id": alarm['alarm_attr_id'],  # 监控ID
                    "alarm_source_id": alarm['alarm_source_id'],  # 告警源ID
                    "id": alarm['id'],  # 告警ID
                    "ip": alarm['ip'],  # 主机IP
                    "raw": alarm['raw'],  # 告警内容
                    "level": alarm['level'],  # 告警等级
                    "status": alarm['status'],  # 状态
                    "comment": alarm['comment'],  # 备注
                    "alarm_type": alarm['alarm_type'],  # 告警类型
                    "source_type": alarm['source_type'],  # 告警源类型
                    "origin_alarm": alarm['origin_alarm'],  # 告警源数据
                    "alarm_content": alarm['alarm_content'],  # 告警内容
                    "snap_alarm_source": alarm['snap_alarm_source'],  # 告警源配置快照

                    "begin_time": make_time(alarm['begin_time']),  # 处理开始时间
                    "end_time": make_time(alarm['end_time']),  # 处理结束时间
                    "source_time": make_time(alarm['source_time']),  # 告警发生时间

                    "source_id": alarm['source_id'],  # 告警特征ID
                    "event_id": alarm['event_id'],  # 关联事件ID
                    "priority": alarm['priority'],  # 告警优先级
                    "user_status": alarm['user_status'],  # 告警外部状态
                })
        else:
            logger.warning(
                f"{get_now_time()} 批量筛选告警失败：{data['message']} 接口名称(alarm_instance) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']
        return result

    def list_component_instance(self, bk_biz_id: int, ip="", id="", bk_cloud_id=0, component=""):
        """
        批量筛选组件
        :param bk_biz_id:int 是	业务ID
        :param ip:string 否	实例IP
        :param id:int 否 组件ID
        :param bk_cloud_id:int	否	云区域ID
        :param component:string	否	组件名称
        :return:result
        """
        kwargs = {
            "bk_token": self.bk_token,
            "id": id,
            "ip	": ip,
            "component": component,
            "bk_biz_id": bk_biz_id,
            "bk_cloud_id": bk_cloud_id,
        }
        data = self.client.monitor.list_component_instance(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']

        else:
            logger.warning(
                f"{get_now_time()} 批量筛选组件失败：{data['message']} 接口名称(list_component_instance) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def metadata_create_data_id(self, data_name, etl_config, operator="admin", mq_cluster=0, data_description="",
                                is_custom_source=True):
        """
        创建监控数据源
        :param data_name:int 	string	是	数据源名称
        :param etl_config:string	是	清洗模板配置，prometheus exportor对应"prometheus"
        :param operator:string	是	操作者
        :param mq_cluster:int	否	数据源使用的消息集群
        :param data_description:string	否	数据源的具体描述
        :param is_custom_source:bool 否	是否用户自定义数据源，默认为是
        :return:result
        """
        kwargs = {
            "bk_token": self.bk_token,
            "data_name": data_name,
            "etl_config": etl_config,
            "operator": operator,
            "data_description": data_description,
            "is_custom_source": is_custom_source
        }
        if mq_cluster:
            kwargs['mq_cluster'] = mq_cluster

        data = self.client.monitor.metadata_create_data_id(kwargs)
        result = {"result": False, "message": "nothing", "bk_data_id": 0}

        if data.get("result", False):
            result['result'] = data['result']
            result['bk_data_id'] = data['data']['bk_data_id']

        else:
            logger.warning(
                f"{get_now_time()} 创建监控数据源失败：{data['message']} 接口名称(metadata_create_data_id) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

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

    def metadata_get_data_id(self, bk_data_id: int, data_name=""):
        """
        获取监控数据源具体信息
        :param bk_data_id:int	否	数据源ID
        :param data_name:string	否	数据源名称
        :return:result
        """
        kwargs = {
            "bk_token": self.bk_token,
            "bk_data_id": bk_data_id,
            "data_name": data_name,
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

    def metadata_get_result_table(self, table_id: str):
        """
        获取监控结果表具体信息
        :param table_id:string	是	结果表ID
        :return:result
        """
        kwargs = {
            "bk_token": self.bk_token,
            "table_id": table_id,
        }

        data = self.client.monitor.metadata_get_result_table(kwargs)
        result = {"result": False, "message": "nothing", "data": {}}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(
                f"{get_now_time()} 获取监控结果表具体信息失败：{data['message']} 接口名称(metadata_get_result_table) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def metadata_list_result_table(self, bk_biz_id: int, is_public_include=0, datasource_type=""):
        """
        查询监控结果表
        :param bk_biz_id:int false	获取指定业务下的结果表信息
        :param is_public_include:int false	是否包含全业务结果表, 0为不包含, 非0为包含全业务结果表
        :param datasource_type:string false	需要过滤的结果表类型, 如system
        :return:result
        """
        kwargs = {
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "is_public_include": is_public_include,
            "datasource_type": datasource_type
        }

        data = self.client.monitor.metadata_list_result_table(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(
                f"{get_now_time()} 查询监控结果表失败：{data['message']} 接口名称(metadata_list_result_table) 请求参数({kwargs}) 返回参数({data})")

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
            logger.warning(
                f"{get_now_time()} 修改监控结果表失败：{data['message']} 接口名称(metadata_modify_result_table) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def save_alarm_strategy(self, bk_biz_id: str, alarm_strategy_id: int, hostindex_id: str, solution_task_id="",
                            ip=[],
                            prform_cate="", cc_set=[], cc_module=[], topo=[], unit=None,
                            rules={}, scenario="performance", is_enabled=None, nodata_alarm=0, is_classify_notice=False,
                            alarm_level_config=dict, solution_is_enable=False, solution_type="job",
                            solution_params_replace="", monitor_id=None,
                            display_name=None, condition=[]):
        """
        创建/更新监控策略
        :param solution_task_id:string	自动处理绑定的作业id
        :param ip:list	监控的ip范围
        :param prform_cate:string	ip/set/topo，监控范围的类型
        :param cc_set:list	监控的集群范围
        :param cc_module:list	监控的模块范围
        :param topo:list	监控的业务拓扑范围
        :param unit:string	监控项的单位
        :param hostindex_id:string	主机指标ID(主机监控策略专用)
        :param alarm_strategy_id:int	监控策略id，如果为0是创建，否则为更新
        :param rules:dict	触发及收敛规则
        :param scenario:string	监控场景(performance/log/custom/uptimecheck/dashboard-custom)
        :param is_enabled:boolean	是否启用
        :param bk_biz_id:int	业务ID
        :param nodata_alarm:int	无数据告警配置，0为不开启
        :param is_classify_notice:boolean	是否分级告警
        :param alarm_level_config:dict	告警配置
        :param solution_is_enable:boolean	是否开启接近自动处理
        :param solution_type:string	自动处理类型，目前只有job
        :param solution_params_replace:string	解决方案参数
        :param monitor_id:int	监控项ID
        :param display_name:string	策略名称
        :param condition:list	匹配条件
        :return:result
        """
        # kwargs = {
        #     "bk_token": self.bk_token,
        #     "bk_biz_id": bk_biz_id,
        #     "alarm_strategy_id": alarm_strategy_id,
        #     "hostindex_id": hostindex_id,
        #     "scenario": scenario,
        #     "prform_cate": prform_cate,
        #     "is_classify_notice": is_classify_notice,
        #     "ip": ip,
        #     "cc_set": cc_set,
        #     "cc_module": cc_module,
        #     "topo": topo,
        #     "condition": condition,
        #     "solution_is_enable": solution_is_enable,
        #     "rules": rules,
        #     "nodata_alarm": nodata_alarm,
        #     "solution_type": solution_type,
        #     "solution_task_id": solution_task_id,
        #     "solution_params_replace": solution_params_replace,
        #     "alarm_level_config": alarm_level_config,
        # }
        kwargs={
            # "alarm_strategy_id": 8,
            "hostindex_id": "7",
            "scenario": "performance",
            "prform_cate": "topo",
            # "is_classify_notice": False,
            "ip": ["172.27.16.120"],
            "cc_set": [23],
            "cc_module": [124],
            "topo": [
                {
                    "host_count": 0,
                    "default": 0,
                    "bk_obj_name": "业务",
                    "bk_obj_id": "biz",
                    "service_instance_count": 0,
                    "child": [
                        {
                            "host_count": 0,
                            "default": 0,
                            "bk_obj_name": "集群",
                            "bk_obj_id": "set",
                            "service_instance_count": 0,
                            "child": [
                                {
                                    "host_count": 0,
                                    "default": 0,
                                    "bk_obj_name": "模块",
                                    "bk_obj_id": "module",
                                    "service_instance_count": 0,
                                    "child": [],
                                    "service_template_id": 0,
                                    "bk_inst_id": 124,
                                    "bk_inst_name": "考试主机"
                                }
                            ],
                            "service_template_id": 0,
                            "bk_inst_id": 23,
                            "bk_inst_name": "考试集群"
                        }
                    ],
                    "service_template_id": 0,
                    "bk_inst_id": 4,
                    "bk_inst_name": "考试"
                }
            ],
            # "condition": [
            #     []
            # ],
            # "solution_is_enable": False,
            # "rules": {
            #     "check_window": 5,
            #     "count": 3,
            #     "alarm_window": 1440
            # },
            # "nodata_alarm": 0,
            # "solution_type": "job",
            # "solution_task_id": "",
            # "solution_params_replace": "",
            # "solution_notice": [],
            "alarm_level_config": {
                "1":{
                    # "detect_algorithm": [
                    #     {
                    #         "algorithm_id": 1000,
                    #         "config": {
                    #             "threshold": 95,
                    #             "message": "当前指标值(${metric|value}${metric|unit}) ${method} (${threshold}${metric|unit})",
                    #             "method": "gte"
                    #         }
                    #     }
                    # ],
                    # "notify_way": [
                    #     "mail"
                    # ],
                    # "role_list": [
                    #     "Operator",
                    #     "BakOperator"
                    # ],
                    # "monitor_level": 2,
                    # "alarm_start_time": "00:00",
                    # "alarm_end_time": "23:59",
                    # "responsible": [],
                    # "phone_receiver": [],
                    # "is_recovery": False
                }
            },
            "bk_biz_id": 4
        }
        # save_json("kwargs",kwargs)
        data = self.client.monitor.save_alarm_strategy(kwargs)
        result = {"result": False, "message": "nothing", "data": {}}
        save_json("save_alarm_strategy", data)
        if data.get("result", False):
            result['result'] = data['result']
        else:
            logger.warning(
                f"{get_now_time()} 创建/更新监控策略失败：{data['message']} 接口名称(save_alarm_strategy) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

monitor_api = MONITOR_API("liujiqing")


def save_json(filename, data):
    with open(f"{filename}.json", "w", encoding="utf-8")as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))


def make_time(time_str):
    return time_str[:time_str.rfind("+")]


def get_now_time():
    return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
