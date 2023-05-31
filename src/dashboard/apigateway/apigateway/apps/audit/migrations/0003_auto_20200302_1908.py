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
# Generated by Django 2.0.13 on 2020-03-02 11:08

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("audit", "0002_auto_20200302_1545"),
    ]

    operations = [
        migrations.AddField(
            model_name="auditeventlog",
            name="op_object_group",
            field=models.CharField(db_index=True, default="", max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="auditeventlog",
            name="event_id",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
