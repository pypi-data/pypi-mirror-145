# -*- coding: utf-8 -*-
# Author: LinShu
# Email: 1419282435@qq.com


import configparser
import os
from munch import DefaultMunch


def dict_to_object(res, default=''):
    """
    字典转为对象
    :param res:
    :return:
    """
    if isinstance(res, str):
        return DefaultMunch.fromJSON(res, default)
    if isinstance(res, dict):
        return DefaultMunch.fromDict(res, default)
    if isinstance(res, bytes):
        res = res.decode("utf-8")
        return DefaultMunch.fromDict(res, default)


def judge_conf(path):
    if 'conf' in os.listdir(os.path.abspath(path)):
        return os.path.abspath(path)
    else:
        return judge_conf(path + '../')


def get_config():
    try:
        path = '../../'
        current_path = judge_conf(path)
    except:
        current_path = os.path.abspath('..')
    config_file_path = os.path.join(os.path.abspath(current_path + os.path.sep), 'conf', 'config.ini')
    conf = configparser.ConfigParser()
    conf.read(config_file_path, encoding='utf-8')
    items = list()
    for section in conf.sections():
        items += conf.items(section)
    return dict_to_object(dict(items))


conf = get_config()
