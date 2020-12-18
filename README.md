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

