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


monitor_api = MONITOR_API("liujiqing")


def save_json(filename, data):
    with open(f"{filename}.json", "w", encoding="utf-8")as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))


def make_time(time_str):
    return time_str[:time_str.rfind("+")]


def get_now_time():
    return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
