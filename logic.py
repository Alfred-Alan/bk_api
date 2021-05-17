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
from cc_api import CC_API
from job_api import JOB_API
from monitor_api import MONITOR_API
from sops_api import SOPS_API
from usermanage_api import UserManage_API

logger = logging.getLogger(__name__)








# 模拟工厂类
class BK_Client:
    def __init__(self,username):
        self.bk_token = ''
        self.client = get_client_by_user(username)
        self.AVAILABLE_COLLECTIONS = {
            'cc': CC_API,
            'job': JOB_API,
            'sops': SOPS_API,
            'monitor': MONITOR_API,
            'usermanage': UserManage_API
        }

    def reload(self, bk_token, request):
        self.bk_token = bk_token
        self.client = get_client_by_request(request)

    def __getattr__(self, item):
        return self.AVAILABLE_COLLECTIONS[item](self.bk_token, self.client)


bk_client = BK_Client("liujiqing")


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


def get_now_time():
    return datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")