import base64
import json
import logging
import time
from datetime import datetime

from config import APP_CODE as app_code, SECRET_KEY as app_secret
from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from blueapps.utils.logger import logger



class JOB_API:
    def __init__(self,username):
        self.bk_token = ''
        self.client = get_client_by_user(username)

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
            logger.warning(f"{get_now_time()} 执行作业失败：{data['message']} 接口名称(execute_job) 请求参数({kwargs}) 返回参数({data})")

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
            logger.warning(f"{get_now_time()} 快速执行脚本失败：{data['message']} 接口名称(fast_execute_script) 请求参数({kwargs}) 返回参数({data})")

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
            logger.warning(f"{get_now_time()} 快速执行sql脚本失败：{data['message']} 接口名称(fast_execute_sql) 请求参数({kwargs}) 返回参数({data})")

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
            logger.warning(f"{get_now_time()} 快速分发文件失败：{data['message']} 接口名称(fast_push_file) 请求参数({kwargs}) 返回参数({data})")
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
            logger.warning(f"{get_now_time()} 获取业务下定时作业信息失败：{data['message']} 接口名称(get_cron_list) 请求参数({kwargs}) 返回参数({data})")

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
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "bk_job_id": job_id,
        }
        data = self.client.job.get_job_detail(kwargs)
        result = {'result': False, 'message': 'Nothing', "steps": []}
        if data.get('result', False):
            result['result'] = data['result']
            result['name'] = data['data']['name']
            result['creator'] = data['data']['creator']
            result['bk_job_id'] = data['data']['bk_job_id']
            result['create_time'] = make_time(data['data']['create_time'])
            result['step_num'] = data['data']['step_num']
            result['global_vars']=[{'name':vars['name'],'id':vars['id'],'type':vars['type']} for vars in data['data']['global_vars']]
            for step in data['data']['steps']:
                result['steps'].append({
                    'account': step['account'],
                    'creator': step['creator'],
                    'script_timeout': step['script_timeout'],
                    'name': step['name'],
                    'script_content': step['script_content'],
                    'step_id': step['step_id'],
                    'script_id': step['script_id'],
                    'script_param': step['script_param'],
                    'type': step['type'],
                    'script_type': step['script_type'],
                })
        else:
            logger.warning(f"{get_now_time()} 查询作业模板详情失败：{data['message']} 接口名称(get_job_detail) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def get_job_instance_log(self, bk_biz_id: int, job_instance_id: int):
        """
        查询作业执行日志
        :param bk_biz_id:
        :param job_instance_id:
        :return:
        """
        kwargs = {
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
            logger.warning(f"{get_now_time()} 获取作业执行日志失败：{data['message']} 接口名称(get_job_instance_log) 请求参数({kwargs}) 返回参数({data})")

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
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "job_instance_id": job_instance_id,
        }
        is_finished = False
        count = 0
        while True:
            data = self.client.job.get_job_instance_status(kwargs)
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
            logger.warning(f"{get_now_time()} 获取脚本执行详情失败：{data['message']} 接口名称(get_job_instance_status) 请求参数({kwargs}) 返回参数({data})")

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
            logger.warning(f"{get_now_time()} 查询作业模板失败：{data['message']} 接口名称(get_job_list) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def get_os_account(self, bk_biz_id: int):
        """
        查询业务下的执行账号
        :param bk_biz_id:
        :return:
        """
        kwargs = {
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
            logger.warning(f"{get_now_time()} 查询业务下的执行账号失败：{data['message']} 接口名称(get_os_account) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data['message']

        return result

    def get_own_db_account_list(self, bk_biz_id: int):
        """
        查询用户有权限的DB帐号列表
        :param bk_biz_id:
        :return:
        """
        kwargs = {
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id
        }
        data = self.client.job.get_own_db_account_list(kwargs)
        result = {'result': False, 'message': 'Nothing', "data": []}
        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 查询用户有权限的DB帐号列表失败：{data['message']} 接口名称(get_own_db_account_list) 请求参数({kwargs}) 返回参数({data})")

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
            logger.warning(f"{get_now_time()} 查询脚本详情失败：{data['message']} 接口名称(get_script_detail) 请求参数({kwargs}) 返回参数({data})")

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
            logger.warning(f"{get_now_time()} 获取脚本列表失败：{data['message']} 接口名称(get_script_list) 请求参数({kwargs}) 返回参数({data})")
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
            logger.warning(f"{get_now_time()} 查询作业步骤的执行状态失败：{data['message']} 接口名称(get_step_instance_status) 请求参数({kwargs}) 返回参数({data})")
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
            logger.warning(f"{get_now_time()} 新建或保存定时作业失败：{data['message']} 接口名称(save_cron) 请求参数({kwargs}) 返回参数({data})")
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
            logger.warning(f"{get_now_time()} 更新定时作业状态失败：{data['message']} 接口名称(update_cron_status) 请求参数({kwargs}) 返回参数({data})")
        result['message'] = data['message']

        return result

job_api = JOB_API("liujiqing")

def save_json(filename, data):
    with open(f"{filename}.json", "w", encoding="utf-8")as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))

def make_time(time_str):
    return time_str[:time_str.rfind("+") - 1]

def get_now_time():
    return datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")