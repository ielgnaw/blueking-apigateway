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

import os

from common.constants import API_TYPE_Q
from components.component import Component

from .toolkit import configs


class Sleep(Component):
    """"""

    sys_name = configs.SYSTEM_NAME
    api_type = API_TYPE_Q

    def handle(self):
        path_vars = self.request.path_vars and self.request.path_vars.val_dict or self.request.kwargs

        result = self.outgoing.http_client.request(
            self.request.wsgi_request.method,
            host=os.environ.get("ESB_ECHO_HOST"),
            path="/sleep/{sleep}/".format(**path_vars),
            response_type="text",
        )
        self.response.payload = {
            "result": True,
            "data": {},
            "message": result,
        }
