#!/usr/bin/env python
# -*- coding: utf-8 -*-


# !/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import time

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('request')
logger.setLevel('INFO')

"""日志中间件"""


class RequestLogs(MiddlewareMixin):

	__exclude_urls = ['index/']  # 定义不需要记录日志的url名单

	def __init__(self, *args):
		super().__init__(*args)
		self.start_time = None  # 开始时间
		self.end_time = None  # 响应时间
		self.data = {}  # dict数据

	# def process_request(self, request):
	# 	"""
	# 	绑定request
	# 	"""
	#
	# 	self.start_time = time.time()  # 开始时间
	#
	# 	# 请求IP
	# 	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	# 	if x_forwarded_for:
	# 		# 如果有代理，获取真实IP
	# 		re_ip = x_forwarded_for.split(",")[0]
	# 	else:
	# 		re_ip = request.META.get('REMOTE_ADDR')
	#
	# 	# 请求方法
	# 	re_method = request.method
	#
	# 	path = request.path
	#
	#
	# 	self.data.update(
	# 		{'method': re_method,  # 请求方法
	# 		 'path': path,  # 请求url
	# 		 'ip': re_ip,  # 请求IP
	# 		 }
	# 	)
	# 	logger.info(self.data)

	def process_response(self, request, response):
		"""
		绑定response
		"""
		# 请求url在 exclude_urls中，直接return，不打印日志
		self.data['path'] = request.path

		for url in self.__exclude_urls:
			if url in self.data.get('path'):
				return response

		# 获取响应数据字符串(多用于API, 返回JSON字符串)
		# rp_content = response.content.decode()
		# self.data['rp_content'] = rp_content

		self.data['status_code'] = response.status_code  # 响应码

		try:
			if request.user.email != '':
				name = request.user.email
			else:
				name = request.user.username
		except AttributeError:
			name = None
		self.data['user'] = name

		# # 耗时
		# self.end_time = time.time()  # 响应时间
		# access_time = self.end_time - self.start_time
		# self.data['access_time'] = round(access_time * 1000)  # 耗时毫秒/ms

		self.data['datetime'] = time.strftime('%y-%m-%d:%H-%M-%S')
		logger.info(str(self.data) + "]\n")
		return response