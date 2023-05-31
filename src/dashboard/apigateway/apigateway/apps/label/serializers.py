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
from django.utils.translation import gettext_lazy
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from apigateway.apps.label.models import APILabel
from apigateway.common.fields import CurrentGatewayDefault
from apigateway.core.validators import MaxCountPerGatewayValidator


class APILabelSLZ(serializers.ModelSerializer):
    api = serializers.HiddenField(default=CurrentGatewayDefault())

    class Meta:
        model = APILabel
        fields = [
            "api",
            "id",
            "name",
            "updated_time",
        ]
        read_only_fields = ["id", "updated_time"]
        lookup_field = "id"

        validators = [
            UniqueTogetherValidator(
                queryset=APILabel.objects.all(),
                fields=("api", "name"),
                message=gettext_lazy("网关下标签名称已存在。"),
            ),
            MaxCountPerGatewayValidator(
                APILabel,
                max_count_callback=lambda gateway: gateway.max_api_label_count,
                message=gettext_lazy("每个网关最多创建 {max_count} 个标签。"),
            ),
        ]


class APILabelQuerySLZ(serializers.Serializer):
    name = serializers.CharField(allow_blank=True, required=False)
    order_by = serializers.ChoiceField(
        choices=["name", "-name", "updated_time", "-updated_time"],
        allow_blank=True,
        required=False,
    )
