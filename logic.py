import base64
import json
import logging
import time
from datetime import datetime

from config import APP_CODE as app_code, SECRET_KEY as app_secret
from blueking.component.shortcuts import get_client_by_request, get_client_by_user

# celery 使用 ：https://www.cnblogs.com/wang-kai-xuan/p/11978849.html

# axios <script src="https://unpkg.com/axios/dist/axios.min.js"></script>

# 账号 bkds30003_test
# 密码 test23@BK
# Saas部署测试环境数据库IP信息：10.0.0.15#3306
# 数据库名：bkds30003_test
# 数据库密码：test23@BK

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


class MONITOR_API:
    def __init__(self, bk_token, client):
        self.bk_token = bk_token
        self.client = client

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

            result['data']["begin_time"] = make_monitor_time(data['data']['begin_time'])  # 处理开始时间
            result['data']["end_time"] = make_monitor_time(data['data']['end_time'])  # 处理结束时间
            result['data']["source_time"] = make_monitor_time(data['data']['source_time'])  # 告警发生时间

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
        save_json("export_alarm_strategy",data)
        result = {"result": False, "message": "nothing"}
        if data.get("result", False):
            result['result'] = data['result']
            result['fail'] = data['data']['fail']
            result['success'] = data['data']['success']
            result['data'] = data['data']['data']
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
                alarm['source_time'] = make_monitor_time(alarm['source_time'])
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
        result = {"result": False, "message": "nothing", "fail": [], "success": []}
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
        result = {"result": False, "message": "nothing", "failed": {}, "successed": {}}
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
        result = {"result": False, "message": "nothing", "failed": {}, "success": {}}
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
        result = {"result": False, "message": "nothing", "failed": {}, "success": {}}
        if data.get("result", False):
            result['result'] = data['result']
            result['failed'] = data['data']['failed']
            result['success'] = data['data']['success']
        else:
            logger.warning(
                f"{get_now_time()} 导入拨测节点配置失败：{data['message']} 接口名称(import_uptime_check_node) 请求参数({kwargs}) 返回参数({data})")
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
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "conf_list": conf_list
        }

        data = self.client.monitor.import_uptime_check_task(kwargs)
        result = {"result": False, "message": "nothing", "failed": {}, "success": {}}
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

                    "begin_time": make_monitor_time(alarm['begin_time']),  # 处理开始时间
                    "end_time": make_monitor_time(alarm['end_time']),  # 处理结束时间
                    "source_time": make_monitor_time(alarm['source_time']),  # 告警发生时间

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
                    2: {
                        "monitor_level": 2,
                        "responsible": [],
                        "notice_start_time": "00:00",
                        "detect_algorithm": [
                            {
                                "config": {
                                    "threshold": 95,
                                    "message": "当前指标值(${metric|value}${metric|unit}) ${method} (${threshold}${metric|unit})",
                                    "method": "gte"
                                },
                                "display": "当前值≥阈值:95%",
                                "name": "静态阈值",
                                "algorithm_id": 1000
                            }
                        ],
                        "notice_end_time": "23:59",
                        "phone_receiver": [],
                        "notify_way": [
                            "mail"
                        ],
                        "is_recovery": False,
                        "role_list": [
                            "Operator",
                            "BakOperator"
                        ]
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

# 模拟工厂类
class BK_Client:
    def __init__(self,username):
        self.bk_token = ''
        self.client = get_client_by_user(username)
        self.AVAILABLE_COLLECTIONS = {
            'cc': CC_API,
            'job': JOB_API,
            'sops': SOPS_API,
            'monitor': MONITOR_API
        }

    def reload(self, bk_token, request):
        self.bk_token = bk_token
        self.client = get_client_by_request(request)

    def __getattr__(self, item):
        return self.AVAILABLE_COLLECTIONS[item](self.bk_token, self.client)


bk_client = BK_Client("liujiqing")


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

def make_monitor_time(time_str):
    return time_str[:time_str.rfind("+")]

def get_now_time():
    return datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")