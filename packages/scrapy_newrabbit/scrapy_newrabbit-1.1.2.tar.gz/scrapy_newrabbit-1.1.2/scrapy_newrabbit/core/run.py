# -*- coding: utf-8 -*-
# Author: LinShu
# Email: 1419282435@qq.com

from importlib import import_module
import datetime
import logging
import os
import sys
from scrapy_newrabbit.utils import SpiderLoader
from scrapy_newrabbit.utils import get_project_settings
from scrapy_newrabbit.settings import overridden_settings

settings_base = get_project_settings()
settings_copy = settings_base.copy()
settings = dict(overridden_settings(settings_copy))


root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

logging.basicConfig(level=getattr(logging, getattr(settings, 'LOG_LEVEL', 'INFO')),
                    format='pid:%(process)d %(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    )


def run(cmd) -> None:
    """手动启动方法"""
    if isinstance(cmd, str):
        cmd = cmd.split(' ')
    while '' in cmd:
        cmd.remove('')
    base_path = 'spiders.'
    if len(cmd) != 4:
        logging.error("命令行格式错误")
        raise
    try:
        path = base_path + cmd[0]
        root_path = cmd[0]
        spider_name = cmd[1]
        way = cmd[2]
        async_num = int(cmd[3])
        queue_name = cmd[0] + '/' + spider_name
    except Exception:
        logging.error("命令行格式错误")
        raise

    start_time = datetime.datetime.now()
    logging.info(f"爬虫启动时间：{start_time}")

    sl = SpiderLoader(type("settings", (object,), dict(getlist=lambda x: [path], getbool=lambda x: False)))
    spider_module = sl.load(spider_name)
    sp = spider_module(path=path, queue_name=queue_name, way=way, async_num=async_num)

    get_settings = getattr(spider_module, 'custom_settings', None)

    if get_settings:
        try:
            item_pipelines = list(get_settings['ITEM_PIPELINES'].keys())
            if '.' in item_pipelines[0]:
                pipline_name = item_pipelines[0].split('.')[-1]
            else:
                pipline_name = item_pipelines[0]
        except KeyError:
            pipline_name = "%sPipeline" % root_path
    else:
        pipline_name = "%sPipeline" % root_path.replace('.','_')

    pipeline = import_module("pipelines")
    pipelineObj = getattr(pipeline, pipline_name, getattr(pipeline, 'Pipeline'))()

    pipelineObj.open_spider(sp)
    setattr(sp, "pipelineObj", pipelineObj)
    sp.main()
    pipelineObj.close_spider(sp)
    end_time = datetime.datetime.now()

    logging.info(f"爬虫启动时间：{start_time}")
    logging.info(f"爬虫结束时间：{end_time}")
    logging.info(f"爬虫运行时长：{end_time - start_time}")
    logging.info(f"Item数量：{pipelineObj.count}")
