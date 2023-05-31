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

import json

from django import forms

from common.constants import API_TYPE_OP, HTTP_METHOD
from common.forms import BaseComponentForm, TypeCheckField
from components.component import Component

from .toolkit import configs, tools


class UpdateObjectTopoGraphics(Component):
    suggest_method = HTTP_METHOD.POST
    label = u"更新拓扑图"
    label_en = "update a topo graphics"

    sys_name = configs.SYSTEM_NAME
    api_type = API_TYPE_OP

    host = configs.host

    class Form(BaseComponentForm):
        scope_type = forms.CharField(label="scope type", required=True)
        scope_id = forms.CharField(label="scope id", required=True)
        action = forms.CharField(label="action", required=True)
        data = TypeCheckField(label="data", promise_type=list, required=True)

    def handle(self):
        client = tools.CCClient(self)
        self.response.payload = client.post(
            host=self.host,
            path="/api/v3/objects/topographics/scope_type/{scope_type}/scope_id/{scope_id}/action/{action}".format(
                **self.form_data
            ),  # noqa
            data=json.dumps(self.form_data["data"]),
        )
