# coding:utf-8
'''
@File    : util.py
@Author  : chendb
@Desc    : 工具
'''



import yagmail
import json
import requests
import time
import random
from faker import Faker
import string
from bs4 import BeautifulSoup


def send_mail_util(from_user, pwd, host, to_user, subject, content):
    # 发送邮件
    with yagmail.SMTP(user=from_user, password=pwd, host=host) as yag:
        yag,send(to_user, subject, content)

def json_util(pre_json, to_json_type, **kwargs):
    # json解析
    try:
        return json.loads(pre_json) if to_json_type == 'json_load' else json.dumps(
            pre_json, ensure_ascii=False, **kwargs
        )
    except:
        return pre_json
    
def xml_to_dict_util(p_xml):
    # xml转dict
    soup = BeautifulSoup(p_xml, features='xml')
    xml = soup.find('xml')
    if not xml:
        return {'error': 'FAIL', 'error_msg': p_xml}
    return dict([(item.name, item.text) for item in xml.find_all()])

def dict_to_xml_util(data, cdata):
    # dict转xml
    xml = [f'<{k}>{f"<![CDATA[{v}]]>" if isinstance(v, str) else v}</{k}>' for k, v in data.items()] \
        if cdata else [f"<{k}>{v}</{k}>" for k, v in data.items()]
    return f"<xml>{''.join(xml)}</xml>".encode('utf-8').decode()

def trans_data_to_url_util(url, data):
    # 参数拼接转成url形式
    if data:
        url = f'{url}?{"&".join([f"{k}={v}" for k, v in data.items()])}'
    return url

def http_client_util(url, method, data, **kwargs):
    # http请求
    up_method = method.upper()
    if up_method == 'POST':
        res = requests.post(url, data=data, **kwargs)
    elif up_method == 'PUT':
        res = requests.put(url, data=data)
    elif up_method == 'DELETE':
        res = requests.delete(url, data=data, **kwargs)
    elif up_method == 'OPTIONS':
        res = requests.options(url, **kwargs)
    elif up_method == 'HEAD':
        res = requests.head(url, **kwargs)
    elif up_method == 'PATCH':
        res = requests.patch(url, data=data, **kwargs)
    else:
        res = requests.get(url, params=data, **kwargs)
    res.encoding = 'utf-8'
    return res

def send_robot_msg_util(msg, send_type, at_all, qy_wechat_token=''):
    # 机器人webhoook
    payloads = {"msgtype": "text", "text": {"content": msg}}
    if send_type == 'qyWechat':
        payloads['text']['mentioned_mobile_list'] = ['@all'] if at_all is True else at_all
        url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send'
        pre_data = {'key': qy_wechat_token}
        url = trans_data_to_url_util(url, pre_data)
        data = json_util(payloads, 'json_dump').encode('utf-8')
        http_client_util(url, 'POST', data=data, headers={'Content-Type': 'application/json'})

def time_stamp_util(time_type):
    # 时间戳
    t = time.time()
    stamp = int(t * 1000) if time_type == 'ms' else int(t)
    return stamp

def get_now_time_util(format_type, time_stamp, d2s=False):
    # 获取当前时间
    f = '%Y-%m-%d %H:%M:%S' if format_type == '-' else '%Y%m%d%H%M%S'
    if time_stamp == 'now':
        return time.strftime(f, time.localtime())
    elif d2s:
        return int(time.mktime(time.strptime(time_stamp, f)))
    else:
        return time.strftime(f, time.localtime(int(time_stamp)))

def random_string_util(n):
    # 随机字符串
    return ''.join(random.sample(string.ascii_letters + string.digits, n))

def format_quot_str_util(pre_str, double_quot=False):
    # 格式化字符串
    if isinstance(pre_str, str):
        return f'"{pre_str}"' if double_quot else f"'{pre_str}'"
    if pre_str is None:
        return 'null'
    if pre_str is True:
        return 'true'
    if pre_str is False:
        return 'false'
    return str(pre_str)

def make_and_sql(sql_list):
    # 拼接sql
    return " and " + " and ".join(sql_list)

def make_sql_str_util(sql_type, table, select_target=None, where=None, update_target=None, insert_target=None,
                      order_by=None, limit=None, select_in=None, between=None, like=None, compare=None,
                      is_not_null=None):
    # 生成sql语句
    where_info = ' where 1=1'
    # where条件 = 语句
    where_info += make_and_sql([f'{k}={format_quot_str_util(v)}' for k, v in where.items()]) if where else ''
    # 判断null 和 not null
    where_info += make_and_sql(
        [f"{k} is {'not null' if v else 'null'}" for k, v in is_not_null.items()]) if is_not_null else ''
    # between条件语句
    where_info += make_and_sql(
        [f'{k} between {format_quot_str_util(v[0])} and {format_quot_str_util(v[1])}' for k, v in
         between.items()]) if between else ''
    # in条件语句
    where_info += make_and_sql(
        [f'{k} in ({", ".join([format_quot_str_util(i) for i in v])})' for k, v in
         select_in.items()]) if select_in else ''
    # like条件语句
    where_info += make_and_sql([f'{k} like {format_quot_str_util(v)}' for k, v in like.items()]) if like else ''
    # 大于 小于 语句
    where_info += make_and_sql(
        [' and '.join([f'{k} {i} {format_quot_str_util(j)}' for i, j in v.items()]) for k, v in
         compare.items()]) if compare else ''
    # insert语句
    if sql_type == 'insert':
        target_info, values_info = [], []
        for k, v in insert_target.items():
            target_info.append(k)
            values_info.append(format_quot_str_util(v))
    # update语句
    elif sql_type == 'update':
        target_str = ", ".join(f"{k}={format_quot_str_util(v)}" for k, v in update_target.items())
        return f'update {table} set {target_str}{where_info};'
    # delete语句
    elif sql_type == 'delete':
        return f'delete from {table}{where_info};'
    else:
        target_str = ", ".join(select_target) if select_target else "*"
        order_str = ' order by ' + ', '.join(
            [f'{k} {v}' for k, v in order_by.items()]) if order_by else ''
        limit_str = f' limit {limit}' if limit else ''
        return f'select {target_str} from {table}{where_info}{order_str}{limit_str};'