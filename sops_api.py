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

    # todo error: interface response is not the JSON format, please try again later or contact component developer to handle this
    def claim_functionalization_task(self, bk_biz_id, task_id,constants: {}, name=""):
        """
        职能化任务认领
        :param bk_biz_id: 业务id
        :param task_id: 任务ID，需要任务状态是未开始的
        :param constants: 任务全局参数 变量 KEY，${key} 格式
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "task_id": task_id,
            "name": name,
            "constants": constants
        }
        data = self.client.sops.claim_functionalization_task(kwargs)
        result = {"result": False, 'message': 'Nothing', 'data': ""}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 职能化任务认领失败：{data['message']} 接口名称(claim_functionalization_task) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def create_periodic_task(self, bk_biz_id, template_id, name, cron: {}, constants={}, exclude_task_nodes_ids=[]):
        """
        创建周期任务
        :param bk_biz_id: 业务id
        :param template_id: 任务ID，需要任务状态是未开始的
        :param name: 要创建的周期任务名称
        :param cron: 要创建的周期任务调度策略
        :param constants: 任务全局参数 变量 KEY，${key} 格式
        :param exclude_task_nodes_ids: 跳过执行的节点ID列表
        :return:
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
            result['activities'] = [{"id": item['id'], "name": item['name'], "stage_name": item['stage_name']} for item in data['data']['pipeline_tree']['activities'].values()]
        else:
            logger.warning(f"{get_now_time()} 创建周期任务失败：{data['message']} 接口名称(create_periodic_task) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result

    def create_task(self, bk_biz_id, template_id, name, constants, template_source="business",flow_type="common",exclude_task_nodes_id=[]):
        """
        通过流程模板创建任务
        :param bk_biz_id: 模板所属业务ID
        :param template_id: 模板ID
        :param template_source: 流程模板来源，business:默认值，业务流程，common：公共流程
        :param name: 任务名称
        :param constants: 任务全局参数 变量 KEY，${key} 格式
        :param flow_type: 任务流程类型，common: 常规流程，common_func：职能化流程
        :param exclude_task_nodes_id: 跳过执行的节点ID列表
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "template_id": template_id,
            "template_source": template_source,
            "name": name,
            "flow_type": flow_type,
            "constants": constants,
            "exclude_task_nodes_id": exclude_task_nodes_id
        }
        data = self.client.sops.create_task(kwargs)
        result = {"result": False, "message": "nothing", "task_id": 0}
        if data.get("result", False):
            result['result'] = data['result']
            result['task_id'] = data['data']['task_id']
        else:
            logger.warning(f"{get_now_time()} 创建任务失败：{data['message']} 接口名称(create_task) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    # todo project_id 可有可无
    def fast_create_task(self, bk_biz_id, project_id, name, pipeline_tree, flow_type="common", description="", category=""):
        """
        快速创建一次性任务
        :param bk_biz_id: 业务ID
        :param project_id: 项目ID
        :param name: 任务名称
        :param pipeline_tree: 任务实例树
        :param flow_type: 任务流程类型，common: 常规流程，common_func：职能化流程
        :param description: 任务描述
        :param category: 任务分类 详细信息请见API文档描述
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "project_id": project_id,
            "name": name,
            "pipeline_tree": pipeline_tree,
            "flow_type": flow_type,
            "description": description,
            "category": category
        }
        data = self.client.sops.fast_create_task(kwargs)
        result = {"result": False, "message": "nothing", "task_id": 0, "task_url": None, "pipeline_tree": {}}

        if data.get("result", False):
            result['result'] = data['result']
            result['task_url'] = data['data']['task_url']
            result['pipeline_tree'] = data['data']['pipeline_tree']
            result['task_id'] = data['data']['task_id']
        else:
            logger.warning(f"{get_now_time()} 创建一次性任务失败：{data['message']} 接口名称(fast_create_task) 请求参数({kwargs}) 返回参数({data})")
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
        save_json("1",data)
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
            logger.warning(f"{get_now_time()} 查询公共流程模板详情失败：{data['message']} 接口名称(get_common_template_info) 请求参数({kwargs}) 返回参数({data})")
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
            logger.warning(
                f"{get_now_time()} 查询公共模板列表失败：{data['message']} 接口名称(get_common_template_list) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    def get_periodic_task_info(self, bk_biz_id, task_id):
        """
        查询某个周期任务的详情
        :param task_id: 周期任务ID
        :param bk_biz_id: 模板所属业务ID
        :return:
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
            logger.warning(
                f"{get_now_time()} 查询周期任务的详情失败：{data['message']} 接口名称(get_periodic_task_info) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def get_periodic_task_list(self, bk_biz_id):
        """
        查询某个业务下所有的周期任务
        :param bk_biz_id: 业务ID
        :return:
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
            logger.warning(
                f"{get_now_time()} 查询业务下所有的周期任务失败：{data['message']} 接口名称(get_periodic_task_list) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    # todo Error Message: Third-party system internal error, please try again later or contact component developer to handle this
    def get_plugin_list(self, bk_biz_id, scope="cmdb_biz"):
        """
        获取某个业务下所有的可用插件
        :param bk_biz_id: 业务ID
        :param scope: 唯一 ID 的范围，取值为 cmdb_biz 或 project，为 cmdb_biz 时 bk_biz_id 代表业务 ID，反之代表项目 ID，默认为 cmdb_biz
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "scope": scope,
        }
        data = self.client.sops.get_plugin_list(kwargs)
        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 查询业务下所有的周期任务失败：{data['message']} 接口名称(get_plugin_list) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    def get_tasks_status(self, bk_biz_id, task_id_list:[], scope="cmdb_biz",include_children_status=True):
        """
        批量查询任务执行状态
        :param bk_biz_id: 业务ID
        :param task_id_list: 任务ID列表
        :param scope: cmdb_biz 时 bk_biz_id 代表业务 ID，project 代表项目 ID，默认为 cmdb_biz
        :param include_children_status:返回的结果中是否需要包含任务中节点的状态
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "task_id_list": task_id_list,
            "scope": scope,
            "include_children_status": include_children_status,
        }
        data = self.client.sops.get_tasks_status(kwargs)

        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result['result'] = data['result']
            for task in data['data']:
                result['data'].append({
                    "name": task['name'],
                    "finish_time": make_time(task['finish_time']),
                    "start_time": make_time(task['start_time']),
                    "state": task['status']['state'],
                    "children": task['status']['children'],
                    "create_time": make_time(task['create_time']),
                    "url": task['url'],
                    "id": task['id']
                })
        else:
            logger.warning(f"{get_now_time()} 批量查询任务执行状态失败：{data['message']} 接口名称(get_tasks_status) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    def get_task_detail(self, bk_biz_id, task_id):
        """
        查询任务执行详情
        :param bk_biz_id: 业务ID
        :param task_id: 任务ID
        :return:
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
            result['template_id'] = data['data']['template_id']
            result['project_id'] = data['data']['project_id']
            result['constants'] = {constant_name: {'name': constant['name'], 'value': constant['value']} for
                                    constant_name, constant in data['data']['constants'].items()}
        else:
            logger.warning(f"{get_now_time()} 查询任务执行详情失败：{data['message']} 接口名称(get_task_detail) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']
        return result

    # todo error: interface response is not the JSON format, please try again later or contact component developer to handle this
    def get_task_list(self, bk_biz_id, scope="cmdb_biz", keyword="", is_started=False, is_finished=False, limit=15, offset=0):
        """
        获取某个业务下的任务列表
        :param bk_biz_id: 业务ID
        :param scope: cmdb_biz 时 bk_biz_id 代表业务 ID，project代表项目 ID  默认为 cmdb_biz
        :param keyword: 根据任务名关键词过滤任务列表，
        :param is_started: 根据任务是否已开始过滤任务列表
        :param is_finished: 根据任务是否已结束过滤任务列表
        :param limit: 分页，返回任务列表任务数，默认为15
        :param offset: 分页，返回任务列表起始任务下标，默认为0
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "scope": scope,
            "keyword": keyword,
            "is_started": is_started,
            "is_finished": is_finished,
            "limit": limit,
            "offset": offset,
        }
        data = self.client.sops.get_task_list(kwargs)
        result = {"result": False, "message": "nothing","data":[]}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 查询任务执行详情失败：{data['message']} 接口名称(get_task_list) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']
        return result

    def get_task_node_data(self, bk_biz_id, task_id, node_id, scope="cmdb_biz", subprocess_stack="[]", component_code=""):
        """
        获取任务节点的数据
        :param bk_biz_id: 业务 ID
        :param task_id:任务 ID
        :param scope: cmdb_biz 时 bk_biz_id 代表业务 ID，project代表项目 ID  默认为 cmdb_biz
        :param node_id:节点 ID
        :param subprocess_stack: 原子编码
        :param component_code: 子流程堆栈，json 格式的列表
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "task_id": task_id,
            "scope": scope,
            "node_id": node_id,
            "subprocess_stack": subprocess_stack,
            "component_code": component_code,
        }
        data = self.client.sops.get_task_node_data(kwargs)
        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 获取任务节点的数据失败：{data['message']} 接口名称(get_task_node_data) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    def get_task_node_detail(self, bk_biz_id, task_id, node_id, scope="cmdb_biz", subprocess_stack="[]", component_code=""):
        """
        查询任务节点执行详情
        :param bk_biz_id: 业务 ID
        :param task_id:任务 ID
        :param scope: cmdb_biz 时 bk_biz_id 代表业务 ID，project代表项目 ID  默认为 cmdb_biz
        :param node_id:节点 ID
        :param subprocess_stack: 原子编码
        :param component_code: 子流程堆栈，json 格式的列表
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "task_id": task_id,
            "scope": scope,
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
            logger.warning(f"{get_now_time()} 查询任务节点执行详情失败：{data['message']} 接口名称(get_task_node_detail) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    def get_task_status(self, bk_biz_id, task_id):
        """
        查询任务或任务节点执行状态
        :param bk_biz_id: 业务 ID
        :param task_id:任务 ID
        :return:
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
            logger.warning(f"{get_now_time()} 获取任务状态失败：{data['message']} 接口名称(get_task_status) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    def get_template_info(self, bk_biz_id, template_id, template_source="business"):
        """
        查询业务下的单个模板详情
        :param bk_biz_id: 业务ID
        :param template_id: 模板ID
        :param template_source: 流程模板来源，business:默认值，业务流程，common：公共流程
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
        save_json("1",data)
        result = {"result": False, "message": "nothing"}
        if data.get("result", False):
            result['result'] = data['result']
            result['name'] = data['data']['name']
            result['project_id'] = data['data']['project_id']
            result['bk_biz_name'] = data['data']['bk_biz_name']
            result['creator'] = data['data']['creator']
            result['activities'] = [{"id": item['id'], "name": item['name'], "stage_name": item['stage_name'], "job_content": item['component']['data']['job_content']['value']}
                                    for item in data['data']['pipeline_tree']['activities'].values()]
            result['constants'] = [{"name": v['name'], "value": k} for k, v in
                                   data['data']['pipeline_tree']['constants'].items()]
            result['create_time'] = make_time(data['data']['create_time'])
            result['id'] = data['data']['id']
        else:
            logger.warning(f"{get_now_time()} 查询业务下的单个模板详情失败：{data['message']} 接口名称(get_template_info) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def get_template_list(self, bk_biz_id, template_source="business"):
        """
        查询业务下的模板列表
        :param bk_biz_id: 业务ID
        :param template_source: 流程模板来源，business:默认值，业务流程，common：公共流程
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "template_source": template_source,
        }
        data = self.client.sops.get_template_list(kwargs)

        result = {"result": False, "message": "nothing","data":[]}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 查询业务下的模板列表失败：{data['message']} 接口名称(get_template_list) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def get_template_schemes(self, bk_biz_id, template_id, scope="cmdb_biz"):
        """
        获取模板的执行方案列表
        :param bk_biz_id: 业务ID
        :param template_id: 模板ID
        :param scope: cmdb_biz 时 bk_biz_id 代表业务 ID，project代表项目 ID  默认为 cmdb_biz
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "template_id": template_id,
            "scope": scope
        }
        data = self.client.sops.get_template_schemes(kwargs)

        result = {"result": False, "message": "nothing","data":[]}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 获取模板的执行方案列表失败：{data['message']} 接口名称(get_template_schemes) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def get_user_project_detail(self, bk_biz_id, scope="cmdb_biz"):
        """
        获取项目的详情
        :param bk_biz_id: 业务ID
        :param scope: cmdb_biz 时 bk_biz_id 代表业务 ID，project代表项目 ID  默认为 cmdb_biz
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "scope": scope
        }
        data = self.client.sops.get_user_project_detail(kwargs)
        result = {"result": False, "message": "nothing", "data": {}}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 获取项目的详情失败：{data['message']} 接口名称(get_user_project_detail) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def get_user_project_list(self, bk_biz_id, scope="cmdb_biz"):
        """
        查询用户有权限的项目列表
        :param bk_biz_id: 业务ID
        :param scope: cmdb_biz 时 bk_biz_id 代表业务 ID，project代表项目 ID  默认为 cmdb_biz
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "scope": scope
        }
        data = self.client.sops.get_user_project_list(kwargs)
        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 查询用户有权限的项目列表失败：{data['message']} 接口名称(get_user_project_list) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo you have no permission to call this api.
    def import_common_template(self, template_data, override=True):
        """
        导入公共流程
        :param template_data: 公共流程数据
        :param override: 是否覆盖 ID 相同的流程
        :return:
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
            logger.warning(f"{get_now_time()} 导入公共流程失败：{data['message']} 接口名称(import_common_template) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    # todo you have no permission to call this api.
    def import_project_template(self, template_data, project_id):
        """
        导入项目流程
        :param template_data: 公共流程数据
        :param project_id: 项目 ID
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "template_data": template_data,
            "project_id": project_id,
        }
        data = self.client.sops.import_project_template(kwargs)

        result = {"result": False, "message": "nothing", "count": 0}
        if data.get("result", False):
            result['result'] = data['result']
            result['count'] = data['data']['count']
        else:
            logger.warning(f"{get_now_time()} 导入项目流程失败：{data['message']} 接口名称(import_project_template) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def modify_constants_for_periodic_task(self, bk_biz_id, task_id, constants={}):
        """
        修改周期任务的全局参数
        :param bk_biz_id: 业务ID
        :param task_id: 任务ID
        :param constants: 任务全局参数

        """
        # "constants": {"${bk_timing}": "100"}
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
            logger.warning(f"{get_now_time()} 修改周期任务的全局参数失败：{data['message']} 接口名称(modify_constants_for_periodic_task) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    # todo error: interface response is not the JSON format, please try again later or contact component developer to handle this
    def modify_constants_for_task(self, task_id, bk_biz_id, constants={}, name="", scope="cmdb_biz"):
        """
        修改周期任务的全局参数
        :param task_id: 任务ID
        :param bk_biz_id: 业务ID
        :param constants: 任务全局参数
        :param name: 任务新名称
        :param scope:  cmdb_biz 时 bk_biz_id 代表业务 ID，project代表项目 ID  默认为 cmdb_biz
        :return:
        """
        # "constants": {"${bk_timing}": "100"}
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "task_id": task_id,
            "bk_biz_id": bk_biz_id,
            "constants": constants,
            "name": name,
            "scope": scope,
        }
        data = self.client.sops.modify_constants_for_task(kwargs)
        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result['result'] = data['result']
        else:
            logger.warning(f"{get_now_time()} 修改周期任务的全局参数失败：{data['message']} 接口名称(modify_constants_for_task) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    def modify_cron_for_periodic_task(self, bk_biz_id, task_id, cron={}):
        """
        修改周期任务的调度策略
        :param bk_biz_id: 业务ID
        :param task_id: 任务ID
        :param cron: 调度策略对象
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
            logger.warning(
                f"{get_now_time()} 修改周期任务的调度策略失败：{data['message']} 接口名称(modify_cron_for_periodic_task) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def node_callback(self, bk_biz_id, task_id, node_id, callback_data={}):
        """
        回调指定的节点
        :param bk_biz_id: 业务ID
        :param task_id: 任务ID
        :param node_id: 节点 ID
        :param callback_data: 回调数据
        :return:
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
            logger.warning(f"{get_now_time()} 回调指定的节点失败：{data['message']} 接口名称(node_callback) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def operate_node(self, bk_biz_id, task_id, node_id,action, scope="cmdb_biz", data=None, inputs=None, flow_id=None):
        """
        操作节点
        :param bk_biz_id: 业务ID
        :param task_id: 任务ID
        :param scope:  cmdb_biz 时 bk_biz_id 代表业务 ID，project代表项目 ID  默认为 cmdb_biz
        :param node_id: 节点 ID
        :param action: 操作类型，可选值有：callback（节点回调）, skip_exg（跳过执行失败的分支网关）, retry（重试失败节点）, skip（跳过失败的节点）, pause_subproc（暂停正在执行的子流程）, resume_subproc（继续暂停的子流程）
        :param data: action 为 callback 时传入的数据
        :param inputs: action 为 retry 时重试节点时节点的输入数据
        :param flow_id: action 为 skip_exg 时选择执行的分支 id
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "task_id": task_id,
            "scope": scope,
            "node_id": node_id,
            "action": action,
            "data": data,
            "inputs": inputs,
            "flow_id": flow_id
        }
        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key]:
                kwargs.pop(param_key)

        data = self.client.sops.operate_node(kwargs)
        result = {"result": False, "message": "nothing"}
        if data.get("result", False):
            result['result'] = data['result']
        else:
            logger.warning(f"{get_now_time()} 操作节点失败：{data['message']} 接口名称(operate_node) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def operate_task(self, bk_biz_id, task_id, action):
        """
        操作任务
        :param bk_biz_id: 业务ID
        :param task_id: 任务ID
        :param action: 操作类型
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
            logger.warning(f"{get_now_time()} 操作任务失败：{data['message']} 接口名称(operate_task) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def preview_task_tree(self, bk_biz_id, template_id, scope="cmdb_biz",version=None,exclude_task_nodes_id=[]):
        """
        获取节点选择后新的任务树
        :param bk_biz_id: 业务ID
        :param template_id: 模板ID
        :param scope:  cmdb_biz 时 bk_biz_id 代表业务 ID，project代表项目 ID  默认为 cmdb_biz
        :param version: 模板的版本，不填时默认为最新版本
        :param exclude_task_nodes_id: 需要移除的可选节点 ID 列表，不填时默认为 []
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "template_id": template_id,
            "scope": scope,
            "version": version,
            "exclude_task_nodes_id": exclude_task_nodes_id,
        }
        data = self.client.sops.preview_task_tree(kwargs)
        result = {"result": False, "message": "nothing"}
        if data.get("result", False):
            result['result'] = data['result']
        else:
            logger.warning(f"{get_now_time()} 获取节点选择后新的任务树失败：{data['message']} 接口名称(preview_task_tree) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def query_task_count(self, bk_biz_id, conditions={}, group_by="status"):
        """
        查询任务实例分类统计总数
        :param bk_biz_id: 业务ID
        :param conditions:任务过滤条件
        :param group_by: 分类统计维度，status：按任务状态（未执行、执行中、已完成）统计，category：按照任务类型统计，flow_type：按照流程类型统计，create_method：按照创建方式
        :return:
        """
        # group_by: status：按任务状态（未执行、执行中、已完成）统计，category：按照任务类型统计，flow_type：按照流程类型统计，create_method：按照创建方式
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
            logger.warning(
                f"{get_now_time()} 查询任务实例分类统计总数失败：{data['message']} 接口名称(query_task_count) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    def set_periodic_task_enabled(self, bk_biz_id, task_id, enabled=False):
        """
        设置周期任务是否激活
        :param bk_biz_id: 业务ID
        :param task_id: 周期任务ID
        :param enabled: 该周期任务是否激活，不传则为 false
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
            logger.warning(
                f"{get_now_time()} 设置周期任务激活失败：{data['message']} 接口名称(set_periodic_task_enabled) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

    def start_task(self, bk_biz_id, task_id):
        """
        启动任务
        :param bk_biz_id: 业务ID
        :param task_id: 任务ID
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
            logger.warning(f"{get_now_time()} 执行任务失败：{data['message']} 接口名称(start_task) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result


def make_time(time_str):
    return time_str[:time_str.rfind("+") - 1]


def save_json(filename, data):
    with open(f"{filename}.json", "w", encoding="utf-8")as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))

def get_now_time():
    return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")