# -*- encoding: utf-8 -*-

import os
import logging
import logging.handlers

#公共日志模块

def get_logger(module_name, file_name=None):
	#输出格式
	formatter = logging.Formatter(fmt='%(levelname)s %(asctime)s  %(message)s  [%(module)s.%(funcName)s() L%(lineno)d]\n', datefmt='%y-%m-%d %H:%M:%S')

	#处理器1，所有级别的信息都将输出到控制台
	handler1 = logging.StreamHandler()
	handler1.setFormatter(formatter)
	handler1.setLevel(logging.DEBUG)

	#处理器2，除了DEGUB级别，其余级别的信息都将输出到文件
	handler2 = None
	if file_name:
		#创建log目录
		try:
			dir = os.path.dirname(file_name)
			if dir and not os.path.exists(dir):
				os.makedirs(dir)
		except Exception as e:
			print('Create dir error: ' + str(e))

		try:
			handler2 = logging.handlers.RotatingFileHandler(filename=file_name, maxBytes=10 * 1024 * 1024, backupCount=10)
			handler2.setFormatter(formatter)
			handler2.setLevel(logging.INFO)
		except Exception as e:
			print('Create RotatingFileHandler error: ' + str(e))

	logger = logging.getLogger(module_name)
	logger.setLevel(logging.DEBUG)
	if handler1: logger.addHandler(handler1)
	if handler2: logger.addHandler(handler2)

	return logger

if __name__ == '__main__':
	import time
	logger = get_logger(__name__)

	while True:
		logger.debug('Debug')
		logger.info('Info')
		logger.warning('Warning')
		logger.error('Error')
		logger.critical('Critical')
		logger.info(u'开始读取任务...')
		time.sleep(10)