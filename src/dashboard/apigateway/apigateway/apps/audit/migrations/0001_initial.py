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
# Generated by Django 2.0.13 on 2019-11-27 02:24

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("event_id", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("system", models.CharField(max_length=64)),
                ("username", models.CharField(max_length=64)),
                ("op_time", models.DateTimeField(auto_now_add=True)),
                (
                    "op_type",
                    models.CharField(
                        choices=[("query", "查询"), ("create", "创建"), ("delete", "删除"), ("modify", "修改")], max_length=32
                    ),
                ),
                (
                    "op_status",
                    models.CharField(choices=[("success", "成功"), ("fail", "失败"), ("unknown", "未知")], max_length=32),
                ),
                ("op_object_type", models.CharField(max_length=32)),
                ("op_object_id", models.CharField(blank=True, max_length=64, null=True)),
                ("op_object_name", models.CharField(blank=True, max_length=64, null=True)),
                ("data_before", models.TextField(blank=True, null=True)),
                ("data_after", models.TextField(blank=True, null=True)),
                ("comment", models.TextField(blank=True, null=True)),
            ],
        ),
    ]
