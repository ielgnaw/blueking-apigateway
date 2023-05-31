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
# Generated by Django 2.0.13 on 2022-04-01 02:51

import django.db.models.deletion
import jsonfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0019_auto_20220307_1601"),
    ]

    operations = [
        migrations.CreateModel(
            name="SslCertificate",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_time", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_time", models.DateTimeField(auto_now=True, null=True)),
                ("created_by", models.CharField(blank=True, max_length=32, null=True)),
                ("updated_by", models.CharField(blank=True, max_length=32, null=True)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("client", "客户端证书"),
                            ("server", "服务端证书"),
                            ("client_ref", "客户端引用证书"),
                            ("server_ref", "服务端引用证书"),
                        ],
                        db_index=True,
                        max_length=32,
                    ),
                ),
                ("name", models.CharField(db_index=True, help_text="引用类证书，名称表示引用名称", max_length=128)),
                ("snis", jsonfield.fields.JSONField(blank=True, default=list)),
                ("cert", models.TextField(blank=True, default="")),
                ("key", models.TextField(blank=True, default="")),
                ("ca_cert", models.TextField(blank=True, default="")),
                ("expires", models.DateTimeField(verbose_name="过期时间")),
                ("api", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.API")),
            ],
            options={
                "db_table": "core_ssl_certificate",
            },
        ),
    ]
