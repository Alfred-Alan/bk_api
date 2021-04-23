import logging
from datetime import datetime

from config import APP_CODE as app_code, SECRET_KEY as app_secret
from blueking.component.shortcuts import get_client_by_request

logger = logging.getLogger(__name__)


class LogSearch_API:
    def __init__(self, bk_token, client):
        self.bk_token = bk_token
        self.client = client

    def reload(self, bk_token, request):
        self.bk_token = bk_token
        self.client = get_client_by_request(request)

    # todo
    def esquery_search(self, indices, scenario_id="log", storage_cluster_id=0, time_field="", start_time="",
                       end_time="", time_range="15m", query_string="*", filter=[], start=0, size=500, aggs={}, highlight={}):
        """
        日志查询接口
        :param indices: 索引列表
        :param scenario_id: ES接入场景(非必填） 默认为log，蓝鲸数据平台：bkdata 原生ES：es 日志采集：log
        :param storage_cluster_id: 当scenario_id为es或log时候需要传入
        :param time_field: 时间字段（非必填，bkdata内部为dtEventTimeStamp，外部如果传入时间范围需要指定时间字段）
        :param start_time: 开始时间
        :param end_time: 结束时间
        :param time_range: 时间标识符符["15m", "30m", "1h", "4h", "12h", "1d", "customized"]（非必填，默认15m）
        :param query_string: 搜索语句query_string(非必填，默认为*)
        :param filter: 搜索过滤条件（非必填，默认为没有过滤，默认的操作符是is） 操作符支持 is、is one of、is not、is not one of
        :param start: 起始位置（非必填，类似数组切片，默认为0）
        :param size: 条数（非必填，控制返回条目，默认为500）
        :param aggs: ES的聚合参数
        :param highlight: 高亮参数
        :return:
        """
        kwargs = {
            "bk_app_code": app_code,
            "bk_app_secret": app_secret,
            "bk_token": self.bk_token,
            "indices": indices,
            "scenario_id": scenario_id,
            "time_field": time_field,
            "start_time": start_time,
            "end_time": end_time,
            "time_range": time_range,
            "query_string": query_string,
            "filter": filter,
            "start": start,
            "size": size,
            "aggs": aggs,
            "highlight": highlight
        }
        if scenario_id == "es" or scenario_id == "log":
            kwargs['storage_cluster_id'] = storage_cluster_id

        # 删除参数空值项
        for param_key in list(kwargs.keys()):
            if not kwargs[param_key]:
                kwargs.pop(param_key)

        data = self.client.log_search.esquery_search(kwargs)
        result = {"result": False, 'message': 'Nothing', 'data': {}}

        if data.get('result', False):
            result['result'] = data['result']
            result['data'] = data['data']
        else:
            logger.warning(f"{get_now_time()} 日志查询接口失败：{data['message']} 接口名称(esquery_search) 请求参数({kwargs}) 返回参数({data})")

        result['message'] = data["message"]

        return result


def get_now_time():
    return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
