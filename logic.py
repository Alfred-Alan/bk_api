import json
from datetime import datetime

from bk_api.cc_api import CC_API
from bk_api.iam_api import IAM_API
from bk_api.job_api import JOB_API
from bk_api.sops_api import SOPS_API
from bk_api.monitor_api import MONITOR_API
from bk_api.log_search_api import LogSearch_API
from bk_api.usermanage_api import UserManage_API
from blueking.component.shortcuts import get_client_by_request, get_client_by_user

# celery 使用 ：https://www.cnblogs.com/wang-kai-xuan/p/11978849.html
# typing-extensions==3.7.4.3
# axios <script src="https://unpkg.com/axios/dist/axios.min.js"></script>

# 账号
# 密码
# Saas部署测试环境数据库IP信息：
# 数据库名：
# 数据库密码：

# 模拟工厂类
class BK_Client:
    def __init__(self,username):
        self.bk_token = ''
        self.client = get_client_by_user(username)
        self.cc = CC_API(self.bk_token, self.client)
        self.job = JOB_API(self.bk_token, self.client)
        self.sops = SOPS_API(self.bk_token, self.client)
        self.monitor = MONITOR_API(self.bk_token, self.client)
        self.log_search = LogSearch_API(self.bk_token, self.client)
        self.usermanage = UserManage_API(self.bk_token, self.client)
        self.iam = IAM_API(self.bk_token, self.client)

    def reload(self, request):
        self.bk_token = request.COOKIES.get("bk_token")
        self.client = get_client_by_request(request)
        self.cc = CC_API(self.bk_token, self.client)
        self.job = JOB_API(self.bk_token, self.client)
        self.sops = SOPS_API(self.bk_token, self.client)
        self.monitor = MONITOR_API(self.bk_token, self.client)
        self.log_search = LogSearch_API(self.bk_token, self.client)
        self.usermanage = UserManage_API(self.bk_token, self.client)
        self.iam = IAM_API(self.bk_token, self.client)


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