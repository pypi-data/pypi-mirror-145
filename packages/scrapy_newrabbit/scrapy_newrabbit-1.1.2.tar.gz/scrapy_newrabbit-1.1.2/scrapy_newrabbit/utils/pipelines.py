# -*- coding: utf-8 -*-
# Author: LinShu
# Email: 1419282435@qq.com

class Pipeline:
    def __init__(self):
        self.count = 0

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.count += 1

    def close_spider(self, spider):
        pass
