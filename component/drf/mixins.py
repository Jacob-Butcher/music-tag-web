# -*- coding: utf-8 -*-
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response


class ApiGenericMixin(object):
    """API视图类通用函数"""

    # TODO 权限部分加载基类中
    if settings.SITE_LOGIN == "false":
        permission_classes = ()

    def finalize_response(self, request, response, *args, **kwargs):
        """统一返回数据格式"""

        if response.data is None:
            response.data = {
                'result': True,
                'message': 'success',
                'data': None
            }
        elif isinstance(response.data, (list, tuple)):
            response.data = {
                'result': True,
                'message': 'success',
                'data': response.data
            }
        elif isinstance(response.data, dict) and ('code' not in response.data and 'result' not in response.data):
            response.data = {
                'result': True,
                'message': 'success',
                'data': response.data
            }
        if response.status_code == status.HTTP_204_NO_CONTENT and request.method == 'DELETE':
            response.status_code = status.HTTP_200_OK

        return super(ApiGenericMixin, self).finalize_response(
            request, response, *args, **kwargs
        )
