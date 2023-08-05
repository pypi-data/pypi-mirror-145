# coding:utf-8
'''
@File    : tools.py
@Author  : chendb
@Desc    : 工具类
'''



from .util import send_mail_util, json_util, send_robot_msg_util, http_client_util, time_stamp_util, get_now_time_util, \
    random_string_util, random_string_util, Faker, trans_data_to_url_util, xml_to_dict_util, dict_to_xml_util


class Tool(object):

    def __init__(self, faker_lang='zh_CN'):
        self.faker_data = Faker(faker_lang)     # 随机数据
        self.mail_from_user = ''                # 邮件发送者账号
        self.mail_from_user_pwd = ''            # 邮件发送者密码
        self.mail_from_user_host = ''           # 邮件发送者host
        self.qy_wechat_token = ''               # 企业微信机器人token


    def send_mail_msg(self, to_user, subject, content):
        # 发送邮件
        send_mail_util(self.mail_from_user, self.mail_from_user_pwd, self.mail_from_user_host, to_user, subject, content)

    @staticmethod
    def json_loads(json_str):
        # dict -> str
        return json_util(json_str, 'json_load', indent=None)

    @staticmethod
    def json_dumps(dict_str, **kwargs):
        # str -> dict
        return json_util(dict_str, 'json_dump', **kwargs)
    
    @staticmethod
    def xml_to_dict(p_xml):
        # xml -> dict
        return xml_to_dict_util(p_xml)
    
    @staticmethod
    def dict_to_xml(data, cdata=False):
        # dict -> xml
        return dict_to_xml_util(data, cdata)
    
    @staticmethod
    def trans_data_to_url(url, data):
        # 参数转成url链接，get请求
        return trans_data_to_url_util(url, data)

    def send_qy_wechat_msg(self, msg, at_all=None):
        # 发送企微机器人webhook
        if at_all is None:
            at_all = []
        send_robot_msg_util(msg, 'qyWechat', qy_wechat_token=self.qy_wechat_token, at_all=at_all)
    
    @staticmethod
    def http_client(url, method='GET', data=None, **kwargs):
        return http_client_util(url, method, data, **kwargs)
    
    @staticmethod
    def time_stamp(time_stamp='s'):
        # 当前时间戳
        return time_stamp_util(time_stamp)
    
    @staticmethod
    def get_now_time(date_type='-'):
        return get_now_time_util(date_type, 'now')
    
    @staticmethod
    def time_stamp_to_date(time_stamp, date_type='-'):
        # 时间戳转日期
        return get_now_time_util(date_type, time_stamp)
    
    @staticmethod
    def date_to_time_stamp(time_stamp, date_type='-'):
        # 日期转时间戳
        return get_now_time_util(date_type, time_stamp, True)
    
    def random_phone(self):
        # 随机手机号
        return str(self.faker_data.phone_number())

    def random_ssn(self):
        # 随机身份证号
        return str(self.faker_data.ssn())
    
    def random_name(self):
        # 随机中文姓名
        return self.faker_data.name()
    
    def random_number(self, n):
        # 随机位数数字
        return str(self.faker_data.random_number(n)).zfill(n)
    
    @staticmethod
    def random_string(n):
        # 随机位数字符串
        return random_string_util(n)