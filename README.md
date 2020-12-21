使用方式 

只需要将logic文件放在项目中

```python
from ...logic import bk_client

# 例：
result = bk_client.cc.search_business()
result = bk_client.job.get_script_list()
result = bk_client.sops.get_template_list()
```

如果需要刷新链接 

```python
bk_token = request.COOKIES.get("bk_token")

bk_client.reload(bk_token, request)
result = bk_client.cc.search_business()
print(result)
```
新增monitor_api 蓝鲸监控API (60%)</br> 
需配合ESB组件使用</br> 
目前最新ESB不支持蓝鲸监控API</br>
自行添加蓝鲸监控方法支持使用：https://github.com/Alfred-Alan/blueking

准守返回方式
```python
from datetime import datetime

def get_now_time():
    return datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")

logger.warning(f"{get_now_time()} xxx失败：{data['message']} 接口名称(xxx) 请求参数({kwargs}) 返回参数({data})")
```
