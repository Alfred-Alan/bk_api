import base64
import json
import time
from datetime import datetime
from config import APP_CODE as app_code, SECRET_KEY as app_secret
from blueking.component.shortcuts import get_client_by_request
from blueapps.utils.logger import logger


class JOB_API:
    def __init__(self, bk_token, client):
        self.bk_token = bk_token
        self.client = client

    def reload(self, bk_token, request):
        self.bk_token = bk_token
        self.client = get_client_by_request(request)

    def execute_job_plan(self, bk_biz_id, job_plan_id, global_var_list=[]):
        """
        :param bk_biz_id: int 业务id
        :param job_plan_id: int 作业方案id
        :param global_var_list: [] 全局参数
        :return: result
        """
        # global_var_list = [
        #     {
        #         'type': '参数类型',
        #         'id': '参数ID',
        #         'server': {
        #             'ip_list': [{'ip': '10.0.6.35', 'bk_cloud_id': 0}]
        #         },
        #     }
        # ]
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "job_plan_id": job_plan_id,
            "global_var_list": global_var_list,
        }
        data = self.client.job.execute_job_plan(kwargs)

        result = {'result': data['result'], 'message': 'Nothing', 'job_instance_id': 0}

        if data.get('data', False):
            result['job_instance_id'] = data['data']['job_instance_id']
        else:
            logger.error(u'执行作业失败：%s' % data['message'])

        result['message'] = data["message"]

        return result

    def fast_execute_script(self, bk_biz_id: int, script_language: int, target_server: {}, account_alias="root",
                            script_version_id=None, script_id=None, script_content=None, task_name="", script_param=""):
        """
        快速执行脚本
        :param bk_biz_id: 业务id
        :param script_version_id: 脚本版本id
        :param script_id: 脚本id 优先级：script_version_id>script_id>script_content
        :param script_content: 脚本内容
        :param task_name: 脚本名称
        :param script_param: 脚本参数
        :param script_language: 脚本语言1 - shell, 2 - bat, 3 - perl, 4 - python, 5 - powershell
        :param account_alias: 执行账户名称
        :param target_server: 目标机器
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": int(bk_biz_id),
            "script_version_id": script_version_id,
            "script_id": script_id,
            "script_content": str(base64.b64encode(script_content.encode('utf-8')), 'utf-8'),
            "task_name": task_name,
            "script_param": str(base64.b64encode(script_param.encode('utf-8')), "utf-8"),
            "timeout": 7200,
            "account_alias": account_alias,
            "script_language": int(script_language),
            "target_server": target_server
        }
        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key]:
                kwargs.pop(param_key)
        data = self.client.job.fast_execute_script(kwargs)
        result = {"result": False, "message": "nothing", "job_instance_id": 0}

        if data.get("result", False):
            result['result'] = data['result']
            result['job_instance_id'] = data['data']['job_instance_id']
        else:
            logger.error("快速执行脚本失败：%s" % data['message'])

        result['message'] = data['message']
        return result

    def fast_execute_sql(self, bk_biz_id: int, db_account_id, target_server: {}, script_id=None, script_version_id=None,
                         script_content=''):
        """
        快速执行sql
        :param bk_biz_id:
        :param script_version_id: 脚本版本id
        :param script_id: 脚本id script_version_id>script_id>script_content
        :param script_content: 脚本内容
        :param db_account_id: SQL执行的db帐号ID
        :param target_server: 目标服务器
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "script_version_id": script_version_id,
            "script_id": script_id,
            "script_content": script_content,
            "timeout": 1000,
            "db_account_id": db_account_id,
            "target_server": target_server
        }
        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key]:
                kwargs.pop(param_key)

        data = self.client.job.fast_execute_sql(kwargs)
        result = {"result": False, "message": "nothing", "job_instance_id": 0}
        if data.get("result", False):
            result["result"] = data['result']
            result["job_instance_id"] = data['data']['job_instance_id']
        else:
            logger.error("快速执行sql脚本失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def fast_transfer_file(self, bk_biz_id: int, account_id, file_target_path, source_ip, file_array: [],
                           target_server: {}, transfer_mode=2, download_speed_limit=None, upload_speed_limit=None):
        """
        快速分发文件
        :param bk_biz_id: 业务id
        :param account_id: 执行账户id
        :param file_target_path:	文件传输目标路径
        :param source_ip:  数据源ip
        :param file_array: 文件名数组
        :param download_speed_limit: 下载限速，单位MB
        :param upload_speed_limit:上传限速，单位MB
        :param transfer_mode: 传输模式。1-严谨模式，2-强制模式，3-保险模式。默认使用强制模式
        :param target_server:目标服务器
        :return:
        """
        file_dict = {
            "file_list": [file for file in file_array],
            "account": {
                "id": account_id
            },
            "server": {
                "ip_list": [{"bk_cloud_id": 0, "ip": ip} for ip in source_ip]
            }
        }
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "account_id": account_id,
            "file_target_path": file_target_path,
            "file_source_list": [file_dict],
            "timeout": 7200,
            "download_speed_limit": download_speed_limit,
            "upload_speed_limit": upload_speed_limit,
            "transfer_mode": transfer_mode,
            "target_server": target_server
        }
        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key]:
                kwargs.pop(param_key)

        print(kwargs)
        data = self.client.job.fast_transfer_file(kwargs)
        result = {"result": False, "message": "nothing", "job_instance_id": 0}

        if data.get("result", False):
            result['result'] = data['result']
            result['job_instance_id'] = data['data']['job_instance_id']
        else:
            logger.error("快速分发文件失败：%s" % data['message'])
        result['message'] = data['message']

        return result

    def get_account_list(self, bk_biz_id: int, category, start=None, length=None):
        """
        查询业务下的执行账号
        :param bk_biz_id:
        :param category: 账号用途（1：系统账号，2：DB账号），不传则不区分
        :param start: 分页记录起始位置，默认为0
        :param length: 单次返回最大记录数，最大1000，默认为20
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "category": category,
            "start": start,
            "length": length
        }
        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key]:
                kwargs.pop(param_key)

        data = self.client.job.get_account_list(kwargs)
        result = {'result': False, 'message': 'Nothing', "data": []}
        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error(u'查询业务下用户有权限的执行账号失败：%s' % result.get('message'))

        result['message'] = data['message']

        return result

    def get_cron_detail(self, bk_biz_id: int, id, ):

        """
        查询定时作业详情
        :param bk_biz_id:
        :param id:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "id": id,
        }

        data = self.client.job.get_cron_detail(kwargs)
        result = {"result": False, "message": "nothing", "data": {}}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("查询定时作业详情：%s" % data['message'])

        result['message'] = data['message']

        return result

    def get_cron_list(self, bk_biz_id: int, id=None, name="", status=None, creator="",
                      create_time_start="", create_time_end=""):

        """
        获取业务下定时作业信息
        :param bk_biz_id:
        :param name:
        :param id:
        :param status:
        :param creator:
        :param create_time_start:
        :param create_time_end:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id
        }
        # 如果存在 cron_id
        if id:
            kwargs['id'] = id
        else:
            kwargs.update({
                "name": name,
                "status": status,
                "creator": creator,
                "create_time_start": create_time_start,
                "create_time_end": create_time_end,
                "start": 0,
                "length": 100
            })

        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key] and kwargs[param_key] != 0:
                kwargs.pop(param_key)
        data = self.client.job.get_cron_list(kwargs)
        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error("获取业务下定时作业信息失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def get_job_instance_global_var_value(self, bk_biz_id: int, job_instance_id: int):
        """
        获取作业实例全局变量的值
        :param bk_biz_id:	业务ID
        :param job_instance_id:	作业实例ID
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "job_instance_id": job_instance_id
        }
        data = self.client.job.get_job_instance_global_var_value(kwargs)
        result = {"result": False, "message": 'nothing', "data": {}}
        if data.get("result"):
            result['data'] = data['data']
            result['result'] = data['result']
            result['message'] = data['message']
        else:
            result['message'] = data['message']
            logger.error("获取业务下定时作业信息失败：%s" % data['message'])
        return result

    def get_job_instance_ip_log(self, bk_biz_id: int, job_instance_id, step_instance_id, ip):
        """
        根据ip查询作业执行日志
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
            "step_instance_id": step_instance_id,
            "bk_cloud_id": 0,
            "ip": ip
        }
        data = self.client.job.get_job_instance_ip_log(kwargs)

        result = {'result': False, 'message': 'Nothing', 'data': []}
        if data.get("result"):
            result['data'] = data['data']
            result['result'] = data['result']
            result['message'] = data['message']
        else:
            result['message'] = data['message']
            logger.error(u'根据ip查询作业执行日志：%s' % result.get('message'))

        result['message'] = data['message']
        return result

    def get_job_instance_list(self, bk_biz_id: int, create_time_start, create_time_end, job_instance_id=None, ip="",
                              job_cron_id="", operator="", name=None, launch_mode=None, type=None, status=None,
                              start=0, length=100):
        """
        根据ip查询作业执行日志
        :param bk_biz_id:	业务 ID
        :param create_time_start:创建起始时间，Unix 时间戳，单位毫秒
        :param create_time_end:创建结束时间，Unix 时间戳，单位毫秒
        :param job_cron_id:任务实例ID。 如果出入job_instance_id，将忽略其他查询条件
        :param operator:执行人，精准匹配
        :param name:任务名称，模糊匹配
        :param launch_mode:执行方式。1 - 页面执行，2 - API调用，3 - 定时执行
        :param type:任务类型。0 - 作业执行，1 - 脚本执行，2 - 文件分发
        :param status:任务状态。1 - 等待执行，2 - 正在执行，3 - 执行成功，4 - 执行失败，7 - 等待确认，10 - 强制终止中，11 - 强制终止成功，13 - 确认终止
        :param ip:执行目标服务器IP, 精准匹配
        :param start:默认0表示从第1条记录开始返回
        :param length:返回记录数量，不传此参数默认返回 20 条
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "create_time_start": create_time_start,
            "create_time_end": create_time_end,
            "start": start,
            "length": length
        }
        # 如果存在 job_instance_id
        if job_instance_id:
            kwargs['job_instance_id'] = job_instance_id
        else:
            kwargs.update({
                "job_cron_id": job_cron_id,
                "operator": operator,
                "name": name,
                "launch_mode": launch_mode,
                "type": type,
                "status": status,
                "ip": ip,
            })

        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key] and kwargs[param_key] != 0:
                kwargs.pop(param_key)
        print(kwargs)
        data = self.client.job.get_job_instance_list(kwargs)

        result = {'result': False, 'message': 'Nothing', 'data': []}
        if data.get("result"):
            result['data'] = data['data']
            result['result'] = data['result']
            result['message'] = data['message']
        else:
            result['message'] = data['message']
            logger.error(u'查询作业实例列表（执行历史)：%s' % result.get('message'))

        result['message'] = data['message']
        return result

    def get_job_instance_status(self, bk_biz_id: int, job_instance_id: int, return_ip_result=False):
        """
        获取脚本执行详情
        :param bk_biz_id:
        :param job_instance_id:
        :param return_ip_result:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "job_instance_id": job_instance_id,
            "return_ip_result": return_ip_result
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
            result['create_time'] = make_stamp_time(data['data']['job_instance']['create_time'])
            result['end_time'] = make_stamp_time(data['data']['job_instance']['end_time'])
            result['status'] = data['data']['job_instance']['status']
            result['finished'] = data['data']['finished']
            for step in data['data']['step_instance_list']:
                result['step'].append({
                    "name": step['name'],
                    "step_instance_id": step['step_instance_id']
                })
        else:
            logger.error("获取脚本执行详情失败：%s" % data['message'])

        result['message'] = data['message']

        return result

    def get_job_plan_detail(self, bk_biz_id, job_plan_id):
        """
        查询作业执行方案详情
        :param bk_biz_id:业务 ID
        :param job_instance_id:	作业执行方案 ID
        :return:
        """
        kwargs = {
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "job_plan_id": job_plan_id
        }
        data = self.client.job.get_job_plan_detail(kwargs)
        result = {"result": False, "message": 'nothing', "data": {}}
        if data.get("result"):
            result['data'] = data['data']
            result['result'] = data['result']
            result['message'] = data['message']
        else:
            result['message'] = data['message']

            logger.error("查询作业执行方案详情：%s" % data['message'])
        return result

    def get_job_plan_list(self, bk_biz_id: int, job_template_id="", creator="", name="", create_time_start="",
                          create_time_end=""):
        """
        查询执行方案列表
        :param bk_biz_id:
        :param job_template_id:
        :param creator:
        :param name:
        :param create_time_start:
        :param create_time_end:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "job_template_id": job_template_id,
            "creator": creator,
            "name": name,
            "create_time_start": create_time_start,
            "create_time_end": create_time_end,
            "start": 0,
            "length": 100
        }
        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key] and kwargs[param_key] != 0:
                kwargs.pop(param_key)

        data = self.client.job.get_job_plan_list(kwargs)
        result = {'result': False, 'message': 'Nothing', "data": []}
        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error(u'查询执行方案列表：%s' % result.get('message'))

        result['message'] = data['message']

        return result

    def get_job_template_list(self, bk_biz_id: int, creator="", name="", create_time_start="", create_time_end=""):
        """
        查询作业模版列表
        :param bk_biz_id:
        :param creator:
        :param name:
        :param create_time_start:
        :param create_time_end:
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
            "start": 0,
            "length": 100
        }

        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key] and kwargs[param_key] != 0:
                kwargs.pop(param_key)

        data = self.client.job.get_job_template_list(kwargs)
        result = {'result': False, 'message': 'Nothing', "data": []}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error(u'查询作业模版列表：%s' % result.get('message'))

        result['message'] = data['message']

        return result

    def get_public_script_list(self, name="", script_language=""):
        """
        查询公共脚本列表
        :param name:脚本名称，支持模糊查询
        :param script_language: 脚本语言。1：shell，2：bat，3：perl，4：python，5：powershell，6：sql。如果不传，默认返回所有
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "name": name,
            "script_language": script_language,
            "start": 0,
            "length": 100
        }

        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key] and kwargs[param_key] != 0:
                kwargs.pop(param_key)

        data = self.client.job.get_public_script_list(kwargs)
        result = {'result': False, 'message': 'Nothing', "data": []}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error(u'查询公共脚本列表：%s' % result.get('message'))

        result['message'] = data['message']

        return result

    def get_public_script_version_detail(self, id="", script_id=None, version=None):
        """
        查询公共脚本版本详情
        :param id:脚本版本ID
        :param script_id:脚本ID
        :param version: 脚本版本（可与script_id一起传入定位某个脚本版本）
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
        }
        if id:
            kwargs['id'] = id
        else:
            kwargs.update({
                "script_id": script_id,
                "version": version
            })

        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key] and kwargs[param_key] != 0:
                kwargs.pop(param_key)

        data = self.client.job.get_public_script_version_detail(kwargs)
        result = {'result': False, 'message': 'Nothing', "data": {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error(u'查询公共脚本版本详情：%s' % result.get('message'))

        result['message'] = data['message']

        return result

    def get_public_script_version_list(self, script_id):
        """
        查询公共脚本版本详情
        :param script_id:脚本ID
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "script_id": script_id,
            "return_script_content": True,
            "start": 0,
            "length": 100
        }

        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key] and kwargs[param_key] != 0:
                kwargs.pop(param_key)

        data = self.client.job.get_public_script_version_list(kwargs)
        result = {'result': False, 'message': 'Nothing', "data": {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error(u'查询公共脚本版本详情：%s' % result.get('message'))

        result['message'] = data['message']

        return result

    def get_script_list(self, bk_biz_id: int, name=None, script_language=None):
        """
        获取脚本列表
        :param bk_biz_id:
        :param name:脚本名称，支持模糊查询
        :param script_language:脚本语言。0：所有脚本类型，1：shell，2：bat，3：perl，4：python，5：powershell，6：sql。默认值为0
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "name": name,
            "script_language": script_language,
            "start": 0,
            "length": 100
        }
        data = self.client.job.get_script_list(kwargs)

        result = {"result": False, "message": "nothing", "data": []}

        if data.get("result", False):
            result["result"] = data['result']
            result['data'] = data['data']['data']
        else:
            logger.error("获取脚本列表失败：%s" % data['message'])

        result['message'] = data['message']
        return result

    def get_script_version_detail(self, bk_biz_id: int, id: int, script_id=None, version=None):
        """
        查询脚本详情
        :param bk_biz_id:
        :param id:
        :param script_id:
        :param version:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
        }

        if id:
            kwargs['id'] = id
        else:
            kwargs.update({
                "script_id": script_id,
                "version": version
            })

        data = self.client.job.get_script_version_detail(kwargs)
        result = {'result': False, 'message': 'Nothing', "detail": {}}
        if data.get('result', False):
            result['result'] = data['result']
            result['detail'] = data['data']
        else:
            logger.error(u'查询脚本详情失败：%s' % result.get('message'))

        result['message'] = data['message']

        return result

    def get_script_version_list(self, bk_biz_id: int, script_id):
        """
        查询业务脚本版本列表
        :param bk_biz_id:
        :param id:
        :param script_id:
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "script_id": script_id,
            "return_script_content": True,
            "start": 0,
            "length": 100
        }

        data = self.client.job.get_script_version_list(kwargs)
        result = {'result': False, 'message': 'Nothing', "data": {}}
        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.error(u'查询业务脚本版本列表：%s' % result.get('message'))

        result['message'] = data['message']

        return result

    def operate_job_instance(self, bk_biz_id: int, job_instance_id, operation_code):
        """
        用于对执行的作业实例进行操作
        :param bk_biz_id:	业务ID
        :param job_instance_id:	作业实例ID
        :param operation_code:	操作类型：2、失败IP重做，3、忽略错误，4、执行，5、跳过，6、确认继续 8、全部重试，9、终止确认流程，10-重新发起确认
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "job_instance_id": job_instance_id,
            "operation_code": operation_code
        }
        print(kwargs)
        data = self.client.job.operate_job_instance(kwargs)

        result = {"result": False, "message": "nothing", "job_instance_id": 0}
        if data.get("result", False):
            result["result"] = data['result']
            result["job_instance_id"] = data['data']['job_instance_id']
        else:
            logger.error("对执行的作业实例进行操作失败：%s" % data['message'])
        result['message'] = data['message']

        return result

    def operate_step_instance(self, bk_biz_id: int, job_instance_id, step_instance_id, operation_code):
        """
        用于对执行的实例的步骤进行操作
        :param bk_biz_id:	业务ID
        :param job_instance_id:	作业实例ID
        :param step_instance_id:	步骤实例ID
        :param operation_code:	操作类型：2、失败IP重做，3、忽略错误，4、执行，5、跳过，6、确认继续 8、全部重试，9、终止确认流程，10-重新发起确认
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "job_instance_id": job_instance_id,
            "step_instance_id": step_instance_id,
            "operation_code": operation_code
        }

        data = self.client.job.operate_step_instance(kwargs)

        result = {"result": False, "message": "nothing", "job_instance_id": 0, "step_instance_id": 0}
        if data.get("result", False):
            result["result"] = data['result']
            result["job_instance_id"] = data['data']['job_instance_id']
            result["step_instance_id"] = data['data']['step_instance_id']
        else:
            logger.error("对执行的实例的步骤进行操作失败：%s" % data['message'])
        result['message'] = data['message']

        return result

    def save_cron(self, bk_biz_id: int, job_plan_id: int, name, expression, global_var_list: [], id=None):
        """
        新建或保存定时作业
        :param bk_biz_id:
        :param id:定时任务 ID，更新定时任务时，必须传这个值
        :param job_plan_id:
        :param name:定时作业名称，
        :param expression:各字段含义为：分 时 日 月 周，如: 0/5 * * * ?
        :param global_var_list:全局变量信息
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "id": id,
            "job_plan_id": job_plan_id,
            "name": name,
            "expression": expression,
            "global_var_list": global_var_list,

        }

        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key] and kwargs[param_key] != 0:
                kwargs.pop(param_key)
        data = self.client.job.save_cron(kwargs)
        result = {"result": False, "message": "nothing", "id": 0}
        if data.get("result", False):
            result["result"] = data['result']
            result["id"] = data['data']['id']
        else:
            logger.error("新建或保存定时作业失败：%s" % data['message'])
        result['message'] = data['message']

        return result

    def update_cron_status(self, bk_biz_id: int, status: int, id: int):
        """
        更新定时作业状态，如启动或暂停
        :param bk_biz_id:
        :param id:
        :param status:定时状态，1.启动、2.暂停
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "bk_biz_id": bk_biz_id,
            "id": id,
            "status": status  # 定时状态，1.启动、2.暂停
        }
        data = self.client.job.update_cron_status(kwargs)
        result = {"result": False, "message": "nothing", "id": 0}
        if data.get("result", False):
            result["result"] = data['result']
            result["id"] = data['data']['id']
        else:
            logger.error("更新定时作业状态失败：%s" % data['message'])
        result['message'] = data['message']

        return result


def save_json(filename, data):
    with open(f"{filename}.json", "w", encoding="utf-8")as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))


def make_time(time_str):
    return time_str[:time_str.rfind("+") - 1]


def make_stamp_time(timestamp):
    timestamp = float(timestamp / 1000)
    timearray = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", timearray)


def get_now_time():
    return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
