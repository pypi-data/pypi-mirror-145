# -*- coding: utf-8 -*-
# @Time    : 2020/8/20 4:58 下午
# @Author  : jeffery
# @FileName: logger.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description:
import logging


def init_logger(log_level, log_file, log_file_level):
    log_format = logging.Formatter("[%(asctime)s %(levelname)s] %(message)s")
    logger = logging.getLogger()
    logger.setLevel(log_level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.handlers = [console_handler]

    if log_file is not None and len(log_file) > 0:
        file_handler = logging.FileHandler(log_file, encoding="UTF-8")
        file_handler.setLevel(log_file_level)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

    return logger
