# -*- coding: utf-8 -*-
"""
views相关模块代码
"""
import math
from collections import OrderedDict

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView as _APIView

from component.drf.mixins import ApiGenericMixin


class APIView(ApiGenericMixin, _APIView):
    """APIView"""

    pass


class ModelViewSet(ApiGenericMixin, viewsets.ModelViewSet):
    """按需改造DRF默认的ModelViewSet类"""

    def perform_create(self, serializer):
        """创建时补充基础Model中的字段"""
        user = serializer.context.get("request").user
        username = getattr(user, "username", "guest")
        serializer.save(creator=username, updated_by=username)

    def perform_update(self, serializer):
        """更新时补充基础Model中的字段"""
        user = serializer.context.get("request").user
        username = getattr(user, "username", "guest")
        serializer.save(updated_by=username)


class ReadOnlyModelViewSet(ApiGenericMixin, viewsets.ReadOnlyModelViewSet):
    """按需改造DRF默认的ModelViewSet类"""

    pass


class ViewSet(ApiGenericMixin, viewsets.ViewSet):
    """按需改造DRF默认的ViewSet类"""

    pass


class GenericViewSet(ApiGenericMixin, viewsets.GenericViewSet):
    """按需改造DRF默认的GenericViewSet类"""

    def is_validated_data(self, data):
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def get_page_info(self, validated_data):
        page = validated_data.get("page", 1)
        page_size = validated_data.get("page_size", 5)
        start = (int(page) - 1) * int(page_size)
        end = start + int(page_size)
        return start, end

    def my_paginated_response(self, validated_data, total_count, return_data):
        page = int(validated_data.get("page", 1))
        page_size = int(validated_data.get("page_size", 5))
        total_page = math.ceil(total_count / page_size)
        return Response(
            OrderedDict(
                [
                    ("page", page),
                    ("total_page", total_page),
                    ("count", total_count),
                    ("items", return_data),
                ]
            )
        )

    def convert_post_to_get(self, request):
        data = request.query_params
        _mutable = data._mutable
        data._mutable = True
        data.update(request.data)
        data._mutable = _mutable

    def failure_response(self, msg="failed"):
        return Response({"result": False, "code": "400", "data": [], "message": msg})

    def success_response(self, msg="success", data=None):
        if data is None:
            data = []
        return Response({"result": True, "code": "200", "data": data, "message": msg})
