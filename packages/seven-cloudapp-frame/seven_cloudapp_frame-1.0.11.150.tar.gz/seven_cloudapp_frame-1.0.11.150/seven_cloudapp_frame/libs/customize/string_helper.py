# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-10-22 13:32:07
@LastEditTime: 2022-02-21 11:16:39
@LastEditors: HuangJianYi
@Description: 
"""
import re
import datetime

class StringHelper:
    """
    :description: 字符串帮助类
    """

    #sql关键字
    _sql_pattern_key = r"\b(and|like|exec|execute|insert|create|select|drop|grant|alter|delete|update|asc|count|chr|mid|limit|union|substring|declare|master|truncate|char|delclare|or)\b|(\*|;)"
    #Url攻击正则
    _url_attack_key = r"\b(alert|xp_cmdshell|xp_|sp_|restore|backup|administrators|localgroup)\b"

    @classmethod
    def is_contain_sql(self, str):
        """
        :description: 是否包含sql关键字
        :param str:参数值
        :return:
        :last_editors: HuangJianYi
        """
        result = re.search(self._sql_pattern_key, str.lower())
        if result:
            return True
        else:
            return False

    @classmethod
    def filter_routine_key(self, key):
        """
        :description: 过滤常规字符
        :param key:参数值
        :return:
        :last_editors: HuangJianYi
        """
        routine_key_list = ["\u200b"]
        if not isinstance(key, str):
            return key
        for item in routine_key_list:
            key = key.replace(item, "")
        return key

    @classmethod
    def filter_sql(self, key):
        """
        :description: 过滤sql关键字
        :param key:参数值
        :return:
        :last_editors: HuangJianYi
        """
        if not isinstance(key, str):
            return key
        result = re.findall(self._sql_pattern_key, key.lower())
        for item in result:
            key = key.replace(item[0], "")
            key = key.replace(item[0].upper(), "")
        return key

    @classmethod
    def filter_special_key(self, key):
        """
        :description: 过滤sql特殊字符
        :param key:参数值
        :return:
        :last_editors: HuangJianYi
        """
        if not isinstance(key, str):
            return key
        special_key_list = ["\"", "\\", "/", "*", "'", "=", "-", "#", ";", "<", ">", "+", "%", "$", "(", ")", "%", "@","!"]
        for item in special_key_list:
            key = key.replace(item, "")
        return key

    @classmethod
    def is_attack(self, str):
        """
        :description: 处理攻击请求
        :param str:当前请求地址
        :return:
        :last_editors: HuangJianYi
        """
        if ":" in str:
            return True
        result = re.search(self._url_attack_key, str.lower())
        if result:
            return True
        else:
            return False
    
    @classmethod
    def check_under_age(self, card_id):
        """
        :description: 根据身份证号校验是否未成年
        :param card_id:身份证号
        :return:True已成年False未成年
        :last_editors: HuangJianYi
        """
        result = True
        if len(card_id) == 18:
            birthday_dict = self.get_birthday(card_id)
            birthday_year = birthday_dict["year"]
            birthday_month = birthday_dict["month"]
            birthday_day = birthday_dict["day"]
            now_time = datetime.datetime.today()
            #获取今日日期
            today = int(str(now_time.month) + str(now_time.day))
            if now_time.day < 10:
                today = int(str(now_time.month) + '0' + str(now_time.day))
            #如果今日日期超过生日 则年龄为年份相减，否则年份相减再减1
            age = 0
            if today - int(birthday_month + birthday_day) > 0:
                age = now_time.year - int(birthday_year)
            else:
                age = now_time.year - int(birthday_year) - 1
            if age < 18:
                result = False
        return result

    @classmethod
    def get_birthday(self, card_id):
        """
        :description: 根据身份证号获取生日
        :param card_id:身份证号
        :return:字典
        :last_editors: HuangJianYi
        """
        birthday_dict = {"year":0,"month":0,"day":0}
        if len(card_id) == 18:
            birthday_dict["year"] = card_id[6:10]
            birthday_dict["month"] = card_id[10:12]
            birthday_dict["day"] = card_id[12:14]
        return birthday_dict
