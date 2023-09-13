# -*- coding: utf-8 -*-
#
# TencentBlueKing is pleased to support the open source community by making
# 蓝鲸智云 - API 网关(BlueKing - APIGateway) available.
# Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
# Licensed under the MIT License (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
#     http://opensource.org/licenses/MIT
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions and
# limitations under the License.
#
# We undertake not to change the open source license (MIT license) applicable
# to the current version of the project delivered to anyone in the future.
#
from typing import Any, Dict, cast

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status

from apigateway.apis.web.support import serializers
from apigateway.apps.support.api_sdk import exceptions
from apigateway.apps.support.api_sdk.helper import SDKHelper
from apigateway.apps.support.api_sdk.models import SDKFactory
from apigateway.apps.support.models import APISDK
from apigateway.common.error_codes import error_codes
from apigateway.core.models import ResourceVersion
from apigateway.utils.responses import OKJsonResponse
from apigateway.utils.swagger import PaginatedResponseSwaggerAutoSchema


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        auto_schema=PaginatedResponseSwaggerAutoSchema,
        query_serializer=serializers.APISDKQueryInputSLZ(),
        responses={status.HTTP_200_OK: serializers.SDKListOutputSLZ(many=True)},
        tags=["WebAPI.Support"],
    ),
)
@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        responses={status.HTTP_200_OK: ""}, request_body=serializers.APISDKGenerateInputSLZ, tags=["WebAPI.Support"]
    ),
)
class APISDKListCreateApi(generics.ListCreateAPIView):
    serializer_class = serializers.SDKListOutputSLZ
    lookup_field = "id"

    def list(self, request, *args, **kwargs):
        slz = serializers.APISDKQueryInputSLZ(data=request.query_params, context={"request": request})
        slz.is_valid(raise_exception=True)

        queryset = APISDK.objects.filter_sdk(
            gateway=self.request.gateway,
            language=slz.validated_data.get("language"),
            version_number=slz.validated_data.get("version_number"),
            resource_version_id=slz.validated_data.get("resource_version_id"),
            order_by="-id",
            fuzzy=True,
        )

        page = self.paginate_queryset(queryset)

        sdks = [SDKFactory.create(model=i) for i in page]
        slz = self.get_serializer(sdks, many=True)
        return OKJsonResponse(data=self.paginator.get_paginated_data(slz.data))

    @transaction.atomic
    def create(self, request, gateway_id):
        """
        生成 SDK
        """
        slz = serializers.APISDKGenerateInputSLZ(
            data=request.data,
            context={
                "request": request,
            },
        )
        slz.is_valid(raise_exception=True)

        data = cast(Dict[str, Any], slz.validated_data)
        resource_version = get_object_or_404(ResourceVersion, gateway=request.gateway, id=data["resource_version_id"])

        with SDKHelper(resource_version=resource_version) as helper:
            try:
                info = helper.create(
                    data["language"],
                    version=data["version"],
                    operator=self.request.user.username,
                )
            except exceptions.ResourcesIsEmpty:
                raise error_codes.INTERNAL.format(_("网关下无资源（公开，且请求方法非 ANY），无法生成 SDK。"), replace=True)
            except exceptions.GenerateError:
                raise error_codes.INTERNAL.format(_("网关 SDK 生成失败。"), replace=True)
            except exceptions.PackError:
                raise error_codes.INTERNAL.format(_("网关 SDK 打包失败。"), replace=True)
            except exceptions.DistributeError:
                raise error_codes.INTERNAL.format(_("网关 SDK 发布失败。"), replace=True)
            except exceptions.TooManySDKVersion as err:
                raise error_codes.INTERNAL.format(
                    _("同一资源版本，最多只能生成 {count} 个 SDK。").format(count=err.max_count),
                    replace=True,
                )

            # 非公开 SDK，直接进行下载
            # if not info.context.is_public:
            #     packaged_files = info.get_packaged_files()
            #     file_name, file_path = next(iter(packaged_files.items()))
            #     return DownloadableResponse(open(file_path, "rb"), filename=file_name)

        slz = self.get_serializer(SDKFactory.create(info.sdk))
        return OKJsonResponse(data=slz.data)