#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging,traceback


printlog=logging.getLogger('err')			# 通过getLogger()传入要使用的logger


def global_exception_handler(exc, context):
	# 记录日志
	printlog.error(traceback.format_exc())
	#调用REST framework自己的异常处理
	response = exception_handler(exc, context)

	if not response:
		#DRF未处理的异常
		msg = str(exc)
		return Response({'msg': msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	else:
		#DRF已处理的异常
		if isinstance(response.data, list):
			msg = '; '.join(response.data)
		elif isinstance(response.data, str):
			msg = response.data
		else:
			msg = str(response.data)
		return Response({'msg': msg},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


