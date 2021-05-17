import base64
import json
import logging
import time
from datetime import datetime

from config import APP_CODE as app_code, SECRET_KEY as app_secret
from blueking.component.shortcuts import get_client_by_request, get_client_by_user

logger = logging.getLogger(__name__)


class SOPS_API:
    def __init__(self, bk_token, client):
        self.bk_token = bk_token
        self.client = client

    def reload(self, bk_token, request):
        self.bk_token = bk_token
        self.client = get_client_by_request(request)

    def create_periodic_task(self, bk_biz_id, template_id, name, cron: {}, constants={}, exclude_task_nodes_ids=[]):
        """
        创建周期任务
        """
        # cron:{"minute": "*/1", "hour": "15", "day_of_week":"*", "day_of_month":"*", "month_of_year":"*"}
        # "constants": {"${bk_timing}": "100"}
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "template_id": template_id,
            "name": name,
            "cron": cron,
            "constants": constants,
            "exclude_task_nodes_id": exclude_task_nodes_ids
        }
        data = self.client.sops.create_periodic_task(kwargs)
        result = {"result": False, 'message': 'Nothing', 'job_instance_id': 0}

        if data.get('result', False):
            result['result'] = data['result']
            result['name'] = data['data']['name']
            result['kwargs'] = [{"name": v['name'], "value": k} for k, v in data['data']['form'].items()]
            result['cron'] = data['data']['cron']
            result['activities'] = [{"id": item['id'], "name": item['name'], "stage_name": item['stage_name']} for item
                                    in data['data']['pipeline_tree']['activities'].values()]
        else:
            logger.error(u'创建周期任务失败：%s' % data['message'])

        result['message'] = data["message"]

        return result

    def create_task(self, bk_biz_id, template_id, name, constants, flow_type="common"):
        """
        通过流程模板创建任务
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "name": name,
            "template_id": template_id,
            "flow_type": flow_type,
            "constants": constants,
        }
        data = self.client.sops.create_task(kwargs)
        result = {"result": False, "message": "nothing", "task_id": 0}
        if data.get("result", False):
            result['result'] = data['result']
            result['task_id'] = data['data']['task_id']
        else:
            logger.error("创建任务失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def get_common_template_info(self, template_id):
        """
        查询公共流程模板详情
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "template_id": template_id,
        }
        data = self.client.sops.get_common_template_info(kwargs)
        result = {"result": False, "message": "nothing"}
        if data.get("result", False):
            result['result'] = data['result']
            result['name'] = data['data']['name']
            result['creator'] = data['data']['creator']
            result['activities'] = [{"id": item['id'], "name": item['name'], "stage_name": item['stage_name']} for item
                                    in data['data']['pipeline_tree']['activities'].values()]
            result['constants'] = [{"name": v['name'], "value": k} for k, v in
                                   data['data']['pipeline_tree']['constants'].items()]
            result['create_time'] = make_time(data['data']['create_time'])
            result['id'] = data['data']['id']
        else:
            logger.error("查询公共流程模板详情失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def get_common_template_list(self):
        """
        查询公共模板列表
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
        }
        data = self.client.sops.get_common_template_list(kwargs)
        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("查询公共模板列表失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def get_periodic_task_info(self, bk_biz_id, task_id):
        """
        查询周期任务的详情
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "task_id": task_id
        }
        data = self.client.sops.get_periodic_task_info(kwargs)

        result = {"result": False, "message": "nothing"}
        if data.get("result", False):
            result['result'] = data['result']
            result['name'] = data['data']['name']
            result['creator'] = data['data']['creator']
            result['constants'] = [{"name": v['name'], "value": k} for k, v in data['data']['form'].items()]
            result['cron'] = data['data']['cron']
            result['activities'] = [{"id": item['id'], "name": item['name'], "stage_name": item['stage_name']} for item
                                    in data['data']['pipeline_tree']['activities'].values()]
        else:
            logger.error("查询周期任务的详情失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def get_periodic_task_list(self, bk_biz_id):
        """
        查询某个业务下所有的周期任务
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
        }
        data = self.client.sops.get_periodic_task_list(kwargs)
        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("查询业务下所有的周期任务失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def get_task_detail(self, bk_biz_id, task_id):
        """
        查询任务执行详情
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "task_id": task_id
        }
        data = self.client.sops.get_task_detail(kwargs)
        result = {"result": False, "message": "nothing"}
        if data.get("result", False):
            result['result'] = data['result']
            result['id'] = data['data']['id']
            result['name'] = data['data']['name']
            result['outputs'] = data['data']['outputs']
            result['create_time'] = make_time(data['data']['create_time'])
            result['finish_time'] = make_time(data['data']['finish_time'])
            result['executor'] = data['data']['executor']
            result['task_url'] = data['data']['task_url']
        else:
            logger.error("查询任务执行详情失败：%s" % data['message'])
        result['message'] = data['message']
        return result

    def get_task_node_detail(self, bk_biz_id, task_id, node_id, subprocess_stack="[]", component_code=""):
        """
        查询任务节点执行详情
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "task_id": task_id,
            "node_id": node_id,
            "subprocess_stack": subprocess_stack,
            "component_code": component_code,
        }
        data = self.client.sops.get_task_node_detail(kwargs)
        result = {"result": False, "message": "nothing"}
        if data.get("result", False):
            result['result'] = data['result']
            result['id'] = data['data']['id']
            result['name'] = data['data']['name']
            result['inputs'] = data['data']['inputs']
            result['state'] = data['data']['state']
            result['start_time'] = make_time(data['data']['start_time'])
            result['finish_time'] = make_time(data['data']['finish_time'])
            result['job_inst_url'] = data['data']['outputs'][3]['value']
        else:
            logger.error("查询任务节点执行详情失败：%s" % data['message'])
        result['message'] = data['message']

        return result

    def get_task_status(self, bk_biz_id, task_id):
        """
        查询任务或任务节点执行状态
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "task_id": task_id
        }
        is_finished = False
        count = 0
        while True:
            data = self.client.sops.get_task_status(kwargs)
            if data.get("result", False):
                state = data['data']['state']
                if state == "RUNNING":
                    time.sleep(1)
                else:
                    is_finished = True
                    break
            else:
                logger.error("request error %s" % data['message'])
                count += 1
                if count >= 5:
                    break
                time.sleep(1)

        data = self.client.sops.get_task_status(kwargs)
        result = {"result": False, "message": "nothing", "task_id": 0, "data": []}

        if is_finished:
            result['result'] = data['result']
            result['task_id'] = task_id
            result['state'] = data['data']['state']
            result['finish_time'] = make_time(data['data']['finish_time'])
            result['start_time'] = make_time(data['data']['start_time'])
            for child in data['data']['children'].values():
                result['data'].append({
                    "name": child['name'],
                    "state": child['state'],
                    "skip": child['skip'],
                    "retry": child['retry'],
                    "finish_time": make_time(child['finish_time']),
                    "start_time": make_time(child['start_time']),
                })
        else:
            logger.error("获取任务状态失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def get_template_info(self, bk_biz_id, template_id, template_source="business"):
        """
        查询业务下的单个模板详情
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "template_id": template_id,
            "template_source": template_source,
        }
        data = self.client.sops.get_template_info(kwargs)
        result = {"result": False, "message": "nothing"}
        if data.get("result", False):
            result['result'] = data['result']
            result['name'] = data['data']['name']
            result['creator'] = data['data']['creator']
            result['activities'] = [{"id": item['id'], "name": item['name'], "stage_name": item['stage_name']} for item
                                    in data['data']['pipeline_tree']['activities'].values()]
            result['constants'] = [{"name": v['name'], "value": k} for k, v in
                                   data['data']['pipeline_tree']['constants'].items()]
            result['create_time'] = make_time(data['data']['create_time'])
            result['id'] = data['data']['id']
        else:
            logger.error("查询业务下的单个模板详情失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def import_common_template(self, template_data, override=True):
        """
        导入公共流程
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "template_data": template_data,
            "override": override,
        }
        data = self.client.sops.import_common_template(kwargs)

        result = {"result": False, "message": "nothing", "count": 0}
        if data.get("result", False):
            result['result'] = data['result']
            result['count'] = data['data']['count']
        else:
            logger.error("导入公共流程失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def modify_constants_for_periodic_task(self, bk_biz_id, task_id, constants={}):
        """
        修改周期任务的全局参数
        # "constants": {"${bk_timing}": "100"}
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "task_id": task_id,
            "constants": constants,
        }
        data = self.client.sops.modify_constants_for_periodic_task(kwargs)
        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result['result'] = data['result']
            for item in data['data'].values():
                result['data'].append({
                    "key": item['key'],
                    "value": item['value'],
                })
        else:
            logger.error("修改周期任务的全局参数失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def modify_cron_for_periodic_task(self, bk_biz_id, task_id, cron={}):
        """
        修改周期任务的调度策略
        # cron:{"minute": "*/1", "hour": "15", "day_of_week":"*", "day_of_month":"*", "month_of_year":"*"}
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "task_id": task_id,
            "cron": cron,
        }
        data = self.client.sops.modify_cron_for_periodic_task(kwargs)
        result = {"result": False, "message": "nothing", "cron": {}}
        if data.get("result", False):
            result['result'] = data['result']
            result['cron'] = data['data']['cron']

        else:
            logger.error("修改周期任务的调度策略失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def node_callback(self, bk_biz_id, task_id, node_id, callback_data={}):
        """
        回调指定的节点
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "task_id": task_id,
            "node_id": node_id,
            "callback_data": callback_data
        }
        data = self.client.sops.node_callback(kwargs)
        result = {"result": False, "message": "nothing"}
        if data.get("result", False):
            result['result'] = data['result']

        else:
            logger.error("回调指定的节点失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def operate_task(self, bk_biz_id, task_id, action):
        """
        操作任务
        start	开始任务，等效于调用 start_task 接口
        pause	暂停任务，任务处于执行状态时调用
        resume	继续任务，任务处于暂停状态时调用
        revoke	终止任务
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "task_id": task_id,
            "action": action,
        }
        data = self.client.sops.operate_task(kwargs)
        result = {"result": False, "message": "nothing"}
        if data.get("result", False):
            result['result'] = data['result']
        else:
            logger.error("操作任务失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def query_task_count(self, bk_biz_id, conditions={}, group_by="status"):
        """
        查询任务实例分类统计总数
        group_by: status：按任务状态（未执行、执行中、已完成）统计，category：按照任务类型统计，flow_type：按照流程类型统计，create_method：按照创建方式
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "conditions": conditions,
            "group_by": group_by
        }
        data = self.client.sops.query_task_count(kwargs)
        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result['result'] = data['result']
            result['total'] = data['data']['total']
            result['data'] = data['data']['groups']
        else:
            logger.error("查询任务实例分类统计总数失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def set_periodic_task_enabled(self, bk_biz_id, task_id, enabled=False):
        """
        设置周期任务是否激活
        enabled	该周期任务是否激活，不传则为 false
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "task_id": task_id,
            "enabled": enabled
        }
        data = self.client.sops.set_periodic_task_enabled(kwargs)
        result = {"result": False, "message": "nothing"}
        if data.get("result", False):
            result['result'] = data['result']
            result['enabled'] = data['data']['enabled']
        else:
            logger.error("设置周期任务激活失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def start_task(self, bk_biz_id, task_id):
        """
        启动任务
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "task_id": task_id
        }
        data = self.client.sops.start_task(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("执行任务失败：%s" % data['message'])

        result['message'] = data['message']

        return result



def make_time(time_str):
    return time_str[:time_str.rfind("+") - 1]


def save_json(filename, data):
    with open(f"{filename}.json", "w", encoding="utf-8")as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))

def get_now_time():
    return datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")