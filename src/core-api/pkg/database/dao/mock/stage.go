// Code generated by MockGen. DO NOT EDIT.
// Source: stage.go

// Package mock is a generated GoMock package.
package mock

import (
	dao "core/pkg/database/dao"
	reflect "reflect"

	gomock "github.com/golang/mock/gomock"
)

// MockStageManager is a mock of StageManager interface.
type MockStageManager struct {
	ctrl     *gomock.Controller
	recorder *MockStageManagerMockRecorder
}

// MockStageManagerMockRecorder is the mock recorder for MockStageManager.
type MockStageManagerMockRecorder struct {
	mock *MockStageManager
}

// NewMockStageManager creates a new mock instance.
func NewMockStageManager(ctrl *gomock.Controller) *MockStageManager {
	mock := &MockStageManager{ctrl: ctrl}
	mock.recorder = &MockStageManagerMockRecorder{mock}
	return mock
}

// EXPECT returns an object that allows the caller to indicate expected use.
func (m *MockStageManager) EXPECT() *MockStageManagerMockRecorder {
	return m.recorder
}

// GetByName mocks base method.
func (m *MockStageManager) GetByName(gatewayID int64, stageName string) (dao.Stage, error) {
	m.ctrl.T.Helper()
	ret := m.ctrl.Call(m, "GetByName", gatewayID, stageName)
	ret0, _ := ret[0].(dao.Stage)
	ret1, _ := ret[1].(error)
	return ret0, ret1
}

// GetByName indicates an expected call of GetByName.
func (mr *MockStageManagerMockRecorder) GetByName(gatewayID, stageName interface{}) *gomock.Call {
	mr.mock.ctrl.T.Helper()
	return mr.mock.ctrl.RecordCallWithMethodType(mr.mock, "GetByName", reflect.TypeOf((*MockStageManager)(nil).GetByName), gatewayID, stageName)
}
