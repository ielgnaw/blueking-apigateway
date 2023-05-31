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
# Generated by Django 2.0.13 on 2020-07-07 02:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_auto_20200618_1801"),
        ("monitor", "0006_auto_20200623_1523"),
    ]

    operations = [
        migrations.AddField(
            model_name="alarmrecord",
            name="api",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="core.API"),
        ),
        migrations.AlterField(
            model_name="alarmstrategy",
            name="alarm_subtype",
            field=models.CharField(
                choices=[
                    ("status_code_5xx", "后端响应状态码5xx"),
                    ("gateway_timeout", "请求后端响应超时"),
                    ("bad_gateway", "请求后端错误"),
                ],
                db_index=True,
                max_length=64,
            ),
        ),
    ]
