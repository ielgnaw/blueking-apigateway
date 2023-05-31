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
# Generated by Django 2.2.11 on 2020-04-11 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("support", "0003_apisdk_resource_version"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="resourcedoc",
            name="resource",
        ),
        migrations.AddField(
            model_name="resourcedoc",
            name="resource_id",
            field=models.IntegerField(db_index=True, default=0),
            preserve_default=False,
        ),
    ]
