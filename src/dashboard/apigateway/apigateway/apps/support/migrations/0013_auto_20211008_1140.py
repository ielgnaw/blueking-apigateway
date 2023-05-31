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
# Generated by Django 2.0.13 on 2021-10-08 03:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0018_stage_is_public"),
        ("support", "0012_auto_20210907_1205"),
    ]

    operations = [
        migrations.CreateModel(
            name="ResourceDocSwagger",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_time", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_time", models.DateTimeField(auto_now=True, null=True)),
                ("swagger", models.TextField(blank=True, default="")),
                ("api", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.API")),
            ],
            options={
                "verbose_name": "资源文档 Swagger 扩展",
                "verbose_name_plural": "资源文档 Swagger 扩展",
                "db_table": "support_resource_doc_swagger",
            },
        ),
        migrations.RemoveField(
            model_name="resourcedocextend",
            name="resource_doc",
        ),
        migrations.AlterField(
            model_name="resourcedoc",
            name="source",
            field=models.CharField(
                choices=[("import", "导入"), ("custom", "自定义")], db_index=True, default="custom", max_length=32
            ),
        ),
        migrations.DeleteModel(
            name="ResourceDocExtend",
        ),
        migrations.AddField(
            model_name="resourcedocswagger",
            name="resource_doc",
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="support.ResourceDoc"),
        ),
    ]
