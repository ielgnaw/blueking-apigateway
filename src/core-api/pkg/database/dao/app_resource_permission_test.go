/*
 * TencentBlueKing is pleased to support the open source community by making
 * 蓝鲸智云 - API 网关(BlueKing - APIGateway) available.
 * Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
 * Licensed under the MIT License (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 *     http://opensource.org/licenses/MIT
 *
 * Unless required by applicable law or agreed to in writing, software distributed under
 * the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
 * either express or implied. See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * We undertake not to change the open source license (MIT license) applicable
 * to the current version of the project delivered to anyone in the future.
 */

package dao

import (
	"testing"
	"time"

	"core/pkg/database"

	sqlmock "github.com/DATA-DOG/go-sqlmock"
	"github.com/jmoiron/sqlx"
	"github.com/stretchr/testify/assert"
)

func Test_appResourcePermissionManager_Get(t *testing.T) {
	database.RunWithMock(t, func(db *sqlx.DB, mock sqlmock.Sqlmock, t *testing.T) {
		mockQuery := `^SELECT id, bk_app_code, api_id, resource_id, expires FROM permission_app_resource`

		bkAppCode := "bk_app_code"
		gatewayID := int64(1)
		resourceID := int64(2)

		permission := AppResourcePermission{
			ID:         1,
			BkAppCode:  bkAppCode,
			GatewayID:  gatewayID,
			ResourceID: resourceID,
			Expires:    time.Now(),
		}

		mockData := []interface{}{
			permission,
		}
		mockRows := database.NewMockRows(mock, mockData...)

		mock.ExpectQuery(mockQuery).WithArgs(bkAppCode, gatewayID, resourceID).WillReturnRows(mockRows)

		manager := &appResourcePermissionManager{DB: db}
		p, err := manager.Get(bkAppCode, gatewayID, resourceID)

		assert.NoError(t, err, "query from db fail.")
		assert.Equal(t, permission, p)
	})
}
