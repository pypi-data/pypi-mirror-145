# -*- coding: utf-8 -*-
"""
@Time : 2022/2/10 16:28 
@Author : YarnBlue 
@description : 
@File : log.py 
"""
import logging
import os.path

import colorlog


class levelFilter(logging.Filter):
    """
    不输出错误级别日志
    """
    def filter(self, record):
        if record.levelno > logging.WARNING:
            return False
        return True


class log:
    def __init__(self, filename='log.log', error_filename='error.log'):
        self.log_colors_config = {

            'DEBUG': 'white',  # cyan white
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
        self.logger = logging.getLogger(__name__)

        # 输出到控制台
        self.console_handler = logging.StreamHandler()
        # 输出到文件
        filePath = os.path.dirname(os.path.dirname(__file__))
        self.file_handler = logging.FileHandler(filename=os.path.join(filePath, f'MyLog/{filename}'), mode='a',
                                                encoding='utf8')
        # 输出错误日记到文件
        self.erro_file_handler = logging.FileHandler(filename=os.path.join(filePath, f'MyLog/{error_filename}'),
                                                     mode='a', encoding='utf8')

        # 日志级别，logger 和 handler以最高级别为准，不同handler之间可以不一样，不相互影响
        self.logger.setLevel(logging.DEBUG)
        self.console_handler.setLevel(logging.DEBUG)
        self.file_handler.setLevel(logging.INFO)
        self.erro_file_handler.setLevel(logging.ERROR)

        # 日志增加过滤条件
        self.file_handler.addFilter(levelFilter())

        # 日志输出格式
        self.file_formatter = logging.Formatter(
            fmt='[%(asctime)s.%(msecs)03d] "%(pathname)s:%(lineno)d" [%(levelname)s] : %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S'
        )
        self.console_formatter = colorlog.ColoredFormatter(
            fmt='%(log_color)s[%(asctime)s.%(msecs)03d] "%(pathname)s:%(lineno)d" [%(levelname)s] : %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S',
            log_colors=self.log_colors_config
        )
        self.console_handler.setFormatter(self.console_formatter)
        self.file_handler.setFormatter(self.file_formatter)
        self.erro_file_handler.setFormatter(self.file_formatter)
        if not self.logger.handlers:
            self.logger.addHandler(self.console_handler)
            self.logger.addHandler(self.file_handler)
            self.logger.addHandler(self.erro_file_handler)

    def __del__(self):
        self.console_handler.close()
        self.file_handler.close()
        self.erro_file_handler.close()

    def log(self):
        return self.logger
