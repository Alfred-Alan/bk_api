import base64
import json
import logging
import time

from config import APP_CODE as app_code, SECRET_KEY as app_secret
from blueking.component.shortcuts import get_client_by_request, get_client_by_user

# celery 使用 ：https://www.cnblogs.com/wang-kai-xuan/p/11978849.html

# axios <script src="https://unpkg.com/axios/dist/axios.min.js"></script>

logger = logging.getLogger(__name__)


class JOB_API:
    def __init__(self, bk_token, client):
        self.bk_token = bk_token
        self.client = client

    def reload(self, bk_token, request):
        self.bk_token = bk_token
        self.client = get_client_by_request(request)

    def execute_job(self, bk_biz_id, bk_job_id, values=[], steps=[]):
        '''
        :param bk_biz_id: int
        :param bk_job_id: int
        :param values: []
        :param steps: []
        :return: result
        '''
        # global_vars = [
        #     {
        #         'type': '参数类型',
        #         'id': '参数ID',
        #         "ip_list": [{"bk_cloud_id": 0,"ip": "10.0.0.1"},]
        #     }
        # ]
        # steps = [{"name": "脚本名称", "step_id": 脚本ID, "script_timeout": 1000,"script_param":"脚本参数"}]
        # {
        #     "name": "分发文件",
        #     "step_id": 3,
        #     "file_source": [
        #         {"files": ["abc.txt"],
        #             "account": "root",
        #             "ip_list": [{"ip": ip, "bk_cloud_id": 0} for ip in send_ip]
        #         }
        #     ],
        #     "account": "root",
        #     "file_target_path": file_path,
        #     "ip_list": [{"ip": ip, "bk_cloud_id": 0} for ip in recve_ip],
        # }
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_job_id": bk_job_id,
            "global_vars": values,
            "steps": steps
        }
        data = self.client.job.execute_job(kwargs)
        result = {'message': 'Nothing', 'job_instance_id': 0}
        if data.get('data', False):
            result['job_instance_id'] = data['data']['job_instance_id']
        else:
            logger.error(u'执行作业失败：%s' % data['message'])

        result['message'] = data["message"]

        return result

    def fast_execute_script(self, bk_biz_id: int, script_id: int, script_type: int, ips: [], script_content="",
                            script_param=""):
        """
        快速执行脚本
        :param bk_biz_id:
        :param script_id:
        :param script_content:
        :param script_param:
        :param script_type:
        :param ips:
        :return:
        """
        ip_list = [{"bk_cloud_id": 0, "ip": ip} for ip in ips]
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": int(bk_biz_id),
            "script_id": script_id,
            "script_content": str(base64.b64encode(script_content.encode('utf-8')), 'utf-8'),
            "script_param": str(base64.b64encode(script_param.encode('utf-8')), "utf-8"),
            "script_timeout": 1000,
            "account": "root",
            "script_type": int(script_type),
            "ip_list": ip_list
        }
        data = self.client.job.fast_execute_script(kwargs)
        result = {"result": False, "message": "nothing", "job_instance_id": 0}

        if data.get("result", False):
            result['result'] = data['result']
            result['job_instance_id'] = data['data']['job_instance_id']
        else:
            logger.error("快速执行脚本失败：%s" % data['message'])

        result['message'] = data['message']
        return result

    def fast_execute_sql(self, bk_biz_id, script_id, db_account_id, ips):
        """
        快速执行sql
        :param bk_biz_id:
        :param script_id:
        :param db_account_id:
        :param ips:
        :return:
        """
        ip_list = [{"bk_cloud_id": 0, "ip": ip} for ip in ips]
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "db_account_id": db_account_id,
            "script_id": script_id,
            "script_timeout": 1000,
            "ip_list": ip_list
        }
        data = self.client.job.fast_execute_sql(kwargs)
        result = {"result": False, "message": "nothing", "job_instance_id": 0}
        if data.get("result", False):
            result["result"] = data['result']
            result["job_instance_id"] = data['data']['job_instance_id']
        else:
            logger.error("快速执行sql脚本失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def fast_push_file(self, bk_biz_id: int, source_ip, file_target_path, file_array: [], accept_ips: []):
        """
        快速分发文件
        :param bk_biz_id:
        :param file_target_path:
        :param source_ip:
        :param file_array:
        :param accept_ips:
        :return:
        """
        file_dict = {
            "files": [file for file in file_array],
            "account": "root",
            "ip_list": [{"bk_cloud_id": 0, "ip": ip} for ip in source_ip],
        }

        accept_ips = [{'bk_cloud_id': 0, 'ip': ip} for ip in accept_ips]
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "account": "root",
            "file_target_path": file_target_path,
            "file_source": [file_dict],
            "ip_list": accept_ips
        }
        data = self.client.job.fast_push_file(kwargs)
        result = {"result": False, "message": "nothing", "job_instance_id": 0}

        if data.get("result", False):
            result['result'] = data['result']
            result['job_instance_id'] = data['data']['job_instance_id']
        else:
            logger.error("快速分发文件失败：%s" % data['message'])
        result['message'] = data['message']

        return result

    def get_cron_list(self, bk_biz_id: int, cron_id=0, cron_name="", cron_status=1, creator="admin",
                      create_time_start="", create_time_end=""):
        """
        获取业务下定时作业信息
        :param bk_biz_id:
        :param cron_id:
        :param cron_name:
        :param cron_status:
        :param creator:
        :param create_time_start:
        :param create_time_end:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
        }
        # 如果存在 cron_id
        if cron_id:
            kwargs['cron_id'] = cron_id
        else:
            kwargs.update({"cron_id": cron_id,
                           "cron_name": cron_name,
                           "cron_status": cron_status,  # 1：已启动 2:已暂停
                           "creator": creator,
                           "create_time_start": create_time_start,
                           "create_time_end": create_time_end,
                           "start": 0,
                           "length": 100
                           })
        data = self.client.job.get_cron_list(kwargs)
        result = {"result": False, "message": "nothing", data: []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("获取业务下定时作业信息失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def get_job_detail(self, bk_biz_id: int, job_id: int):
        """
        获取作业模板详情
        :param bk_biz_id:
        :param job_id:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_job_id": job_id,
        }
        data = self.client.job.get_job_detail(kwargs)
        save_json("get_job_detail", data)

        return data

    def get_job_instance_log(self, bk_biz_id: int, job_instance_id: int):
        """
        查询作业执行日志
        :param bk_biz_id:
        :param job_instance_id:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "job_instance_id": job_instance_id,
        }
        data = self.client.job.get_job_instance_log(kwargs)

        result = {'result': False, 'message': 'Nothing', 'job_instance_id': 0, "logs": []}
        if data.get('result', False):
            result['result'] = data['result']
            log_dict = {}
            for scrtip in data['data']:
                for step in scrtip['step_results']:
                    for ip_log in step["ip_logs"]:
                        if ip_log['ip'] in log_dict:
                            log_dict[ip_log['ip']].append({
                                "start_time": ip_log['start_time'],
                                "log_content": ip_log['log_content'],
                                "end_time": ip_log['end_time'],
                            })
                        else:
                            log_dict[ip_log['ip']] = [{
                                "start_time": make_time(ip_log['start_time']),
                                "log_content": ip_log['log_content'],
                                "end_time": make_time(ip_log['end_time']),
                            }]
            for key, value in log_dict.items():
                result['logs'].append({
                    "ip": key,
                    "log_content": value,
                })
        else:
            logger.error(u'获取作业执行日志失败：%s' % result.get('message'))

        result['message'] = data['message']
        return result

    def get_job_instance_status(self, bk_biz_id: int, job_instance_id: int):
        """
        获取脚本执行详情
        :param bk_biz_id:
        :param job_instance_id:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "job_instance_id": job_instance_id,
        }
        is_finished = False
        count = 0
        while True:
            data = self.client.job.get_job_instance_status(kwargs)
            save_json("get_job_instance_status", data)
            if data.get("result", False):
                status = data['data']['job_instance']['status']
                if int(status) == 2:
                    time.sleep(1)
                else:
                    is_finished = True
                    break
            else:
                logger.error("request error：%s" % data['message'])
                count += 1
                if count >= 5:
                    break
                time.sleep(1)

        now_time = time.strftime("%Y-%M-%D %H:%m:%S", time.localtime())
        result = {"result": False, "message": "nothing", "job_instance_id": 0, "create_time": now_time, "step": []}

        if is_finished:
            result['result'] = data['result']
            result['job_instance_id'] = data['data']['job_instance']['job_instance_id']
            result['total_time'] = data['data']['job_instance']['total_time']
            result['create_time'] = make_time(data['data']['job_instance']['create_time'])
            result['status'] = data['data']['job_instance']['status']
            result['operator'] = data['data']['job_instance']['operator']
            result['is_finished'] = data['data']['is_finished']
            for step in data['data']['blocks']:
                result['step'].append({
                    "name": step['step_instances'][0]['name'],
                    "step_instance_id": step['step_instances'][0]['step_instance_id']
                })
        else:
            logger.error("获取脚本执行详情失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def get_job_list(self, bk_biz_id: int, creator="admin", name="", create_time_start="", create_time_end="",
                     tag_id="1"):
        """
        查询作业模板
        :param bk_biz_id:
        :param creator:
        :param name:
        :param create_time_start:
        :param create_time_end:
        :param tag_id:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "creator": creator,
            "name": name,
            "create_time_start": create_time_start,
            "create_time_end": create_time_end,
            "tag_id": tag_id,  # 1.未分类、2.运营发布、3.故障处理、4.常用工具、5.产品自助、6.测试专用、7.持续集成
            "start": 0,
            "length": 100
        }
        data = self.client.job.get_job_list(kwargs)
        result = {'result': False, 'message': 'Nothing', "data": []}
        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error(u'查询作业模板失败：%s' % result.get('message'))

        result['message'] = data['message']

        return result

    def get_os_account(self, bk_biz_id: int):
        """
        查询业务下的执行账号
        :param bk_biz_id:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id
        }
        data = self.client.job.get_os_account(kwargs)
        save_json("get_os_account", data)
        result = {'result': False, 'message': 'Nothing', "data": []}
        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error(u'查询业务下的执行账号失败：%s' % result.get('message'))

        result['message'] = data['message']

        return result

    def get_own_db_account_list(self, bk_biz_id: int):
        """
        查询用户有权限的DB帐号列表
        :param bk_biz_id:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id
        }
        data = self.client.job.get_own_db_account_list(kwargs)
        result = {'result': False, 'message': 'Nothing', "data": []}
        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error(u'查询用户有权限的DB帐号列表失败：%s' % result.get('message'))

        result['message'] = data['message']

        return result

    def get_script_detail(self, bk_biz_id: int, id: int):
        """
        查询脚本详情
        :param bk_biz_id:
        :param id:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "id": id
        }
        data = self.client.job.get_script_detail(kwargs)
        save_json("get_script_detail", data)
        result = {'result': False, 'message': 'Nothing', "detail": {}}
        if data.get('result', False):
            result['result'] = data['result']
            result['detail'] = data['data']
        else:
            logger.error(u'查询脚本详情失败：%s' % result.get('message'))

        result['message'] = data['message']

        return result

    def get_script_list(self, bk_biz_id: int, script_type: int, is_public=False):
        """
        获取脚本列表
        :param bk_biz_id:
        :param script_type:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "script_type": script_type,
            "is_public": is_public,
            "return_script_content": True,
        }
        data = self.client.job.get_script_list(kwargs)
        result = {"result": False, "message": "nothing", "data": []}
        if data.get("result", False):
            result["result"] = data['result']
            for script in data['data']['data']:
                result['data'].append({
                    "bk_biz_id": script['bk_biz_id'],
                    "name": script['name'],
                    "creator": script['creator'],
                    "public": script['public'],
                    "type": script['type'],
                    "id": script['id'],
                    "create_time": script['create_time']
                })
        else:
            logger.error("获取脚本列表失败：%s" % data['message'])
        result['message'] = data['message']
        return result

    def get_step_instance_status(self, bk_biz_id: int, job_instance_id=0, step_instance_id=0):
        """
        查询作业步骤的执行状态
        :param bk_biz_id:
        :param job_instance_id:
        :param step_instance_id:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "params": {
                "job_instance_id": job_instance_id,
                "step_instance_id": step_instance_id
            }
        }
        data = self.client.job.get_step_instance_status(kwargs)
        result = {"result": False, "message": "nothing", "status": {}}
        if data.get("result", False):
            result["result"] = data['result']
            result["status"] = data['data']
        else:
            logger.error("查询作业步骤的执行状态失败：%s" % data['message'])
        result['message'] = data['message']

        return result

    def save_cron(self, bk_biz_id: int, bk_job_id: int, cron_name, cron_expression, ):
        """
        新建或保存定时作业
        :param bk_biz_id:
        :param cron_name:
        :param cron_expression:
        :param bk_job_id:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_job_id": bk_job_id,
            "cron_name": cron_name,
            "cron_expression": cron_expression
        }
        data = self.client.job.save_cron(kwargs)
        save_json("save_cron", data)
        result = {"result": False, "message": "nothing", "cron_id": 0}
        if data.get("result", False):
            result["result"] = data['result']
            result["cron_id"] = data['data']['cron_id']
        else:
            logger.error("新建或保存定时作业失败：%s" % data['message'])
        result['message'] = data['message']

        return result

    def update_cron_status(self, bk_biz_id: int, cron_status: int, cron_id: int):
        """
        更新定时作业状态，如启动或暂停
        :param bk_biz_id:
        :param cron_status:
        :param cron_id:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "cron_status": cron_status,  # 定时状态，1.启动、2.暂停
            "cron_id": cron_id
        }
        data = self.client.job.update_cron_status(kwargs)
        save_json("update_cron_status", data)
        result = {"result": False, "message": "nothing", "cron_id": 0}
        if data.get("result", False):
            result["result"] = data['result']
            result["cron_id"] = data['data']['cron_id']
        else:
            logger.error("更新定时作业状态失败：%s" % data['message'])
        result['message'] = data['message']

        return result


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

    def query_task_count(self, bk_biz_id,conditions={},group_by="status"):
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
        result = {"result": False, "message": "nothing","data":[]}
        if data.get("result", False):
            result['result'] = data['result']
            result['total'] = data['data']['total']
            result['data'] = data['data']['groups']
        else:
            logger.error("查询任务实例分类统计总数失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def set_periodic_task_enabled(self, bk_biz_id,task_id,enabled=False):
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


class CC_API:
    def __init__(self, bk_token, client):
        self.bk_token = bk_token
        self.client = client

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

    def list_biz_hosts(self, bk_biz_id: int, bk_obj_id, bk_inst_ids=[]):
        """
        查询业务下主机
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

    def search_biz_inst_topo(self, bk_biz_id: int):
        """
        查询业务下拓扑
        :param bk_biz_id:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id
        }
        data = self.client.cc.search_biz_inst_topo(kwargs)
        result = {"result": False, "message": "nothing", "data": []}
        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = [make_topo(data['data'])]
        else:
            logger.error("获取业务实例拓扑失败:%s", data['message'])

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

    def search_module(self, bk_biz_id: int, bk_set_id, condition={}):
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


# 模拟工厂类
class BK_Client:
    def __init__(self):
        self.bk_token = ''
        self.client = get_client_by_user("liujiqing")
        self.AVAILABLE_COLLECTIONS = {
            'cc': CC_API,
            'job': JOB_API,
            'sops': SOPS_API,
        }

    def reload(self, bk_token, request):
        self.bk_token = bk_token
        self.client = get_client_by_request(request)

    def __getattr__(self, item):
        return self.AVAILABLE_COLLECTIONS[item](self.bk_token, self.client)


bk_client = BK_Client()


# class BK_API:
#     def __init__(self):
#         self.bk_token = ''
#         self.client = get_client_by_user("admin")
#
#     def reload(self, bk_token, request):
#         self.bk_token = bk_token
#         self.client = get_client_by_request(request)
#
#     def list_users(self):
#         kwargs = {
#             "bk_app_code": app_code,
#             "bk_app_secret": app_secret,
#             "bk_token": self.bk_token,
#             "fields": "username,id",
#         }
#         data = self.client.usermanage.list_users(kwargs)
#
#         result = {"result": False, "message": "nothing", "users": []}
#
#         if data.get("result", False):
#             result["result"] = data['result']
#             result["users"] = data['data']['results']
#         else:
#             logger.error("获取用户失败 %s" % data['message'])
#
#         result['message'] = data['message']
#         return result
#
# bk_api = BK_API()


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


def make_data(data):
    chiled = []
    # 如果存在child
    if data['child']:
        for i in data['child']:
            chiled.append(make_data(i))
        data = {"id": data['bk_inst_id'], "name": data['bk_inst_name'], "bk_inst_id": data['bk_inst_id'],
                'bk_obj_id': data['bk_obj_id'], 'children': chiled, 'expanded': True}
        return data
    else:
        data = {"id": data['bk_inst_id'], "name": data['bk_inst_name'], "bk_inst_id": data['bk_inst_id'],
                'bk_obj_id': data['bk_obj_id'], }
        return data
