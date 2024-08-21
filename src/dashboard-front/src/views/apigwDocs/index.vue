<template>
  <div class="docs-main">
    <header class="page-tabs">
      <div class="tabs-group">
        <nav
          class="page-tab"
          :class="{ 'active': curTab === 'apigw' }"
          @click="curTab = 'apigw'"
        >{{ t('网关 API 文档') }}</nav>
        <nav
          class="page-tab"
          :class="{ 'active': curTab === 'component' }"
          @click="curTab = 'component'"
        >{{ t('组件 API 文档') }}</nav>
      </div>
    </header>
    <main class="docs-main-content">
      <div class="top-bar">
        <bk-input
          type="search"
          :placeholder="t('请输入网关名称或描述')"
          v-model="filterData.keyword"
          clearable
          style="width: 400px"
        />
        <bk-link theme="primary" class="f12 ml24" @click.prevent="isSdkInstructionSliderShow = true">
          <i class="apigateway-icon icon-ag-document f14"></i>
          {{ t('SDK 使用说明')}}
        </bk-link>
        <!-- <bk-button
          theme="primary"
          @click="handleGoApigw"
        >
          {{ t('网关管理') }}
        </bk-button> -->
      </div>
      <div class="docs-list">
        <bk-loading :loading="isLoading">
          <bk-table
            :data="tableData"
            remote-pagination
            :pagination="pagination"
            show-overflow-tooltip
            @page-limit-change="handlePageSizeChange"
            @page-value-change="handlePageChange"
            :border="['outer']"
          >
            <bk-table-column
              :label="t('网关名称')"
              field="name"
            >
              <template #default="{ data }">
                <span class="link-name" @click="gotoDetails(data)">{{data?.name || '--'}}</span>
                <bk-tag theme="success" v-if="data?.is_official">
                  {{ t('官方') }}
                </bk-tag>
              </template>
            </bk-table-column>
            <bk-table-column
              :label="t('网关描述')"
              field="description"
            >
              <template #default="{ data }">
                {{ data?.description || '--' }}
              </template>
            </bk-table-column>
            <bk-table-column
              :label="t('网关负责人')"
              field="maintainers"
            >
              <template #default="{ data }">
                {{ data?.maintainers?.join(', ') || '--' }}
              </template>
            </bk-table-column>
            <bk-table-column
              :label="t('SDK 包名称')"
              field="maintainers"
            >
              <template #default="{ data }">
                --
              </template>
            </bk-table-column>
            <bk-table-column
              :label="t('SDK 最新版本')"
              field="maintainers"
            >
              <template #default="{ data }">
                --
              </template>
            </bk-table-column>
            <bk-table-column
              :label="t('操作')"
              width="180"
              fixed="right"
            >
              <template #default="{ row }">
                <bk-button
                  text
                  theme="primary"
                  @click="isSdkDetailDialogShow = true"
                >
                  {{ t('查看 SDK') }}
                </bk-button>
                <bk-button
                  text
                  theme="primary"
                  class="pl10 pr10"
                >
                  {{ t('下载 SDK') }}
                </bk-button>
              </template>
            </bk-table-column>
            <template #empty>
              <TableEmpty
                :keyword="tableEmptyConf.keyword"
                :abnormal="tableEmptyConf.isAbnormal"
                @reacquire="getList"
                @clear-filter="handleClearFilterKey"
              />
            </template>
          </bk-table>
        </bk-loading>
      </div>
    </main>
    <!--  SDK使用说明 Slider  -->
    <SdkInstructionSlider v-model="isSdkInstructionSliderShow"></SdkInstructionSlider>
    <SdkDetailDialog v-model="isSdkDetailDialogShow"></SdkDetailDialog>
  </div>
</template>

<script lang="ts" setup>
import {
  provide,
  ref,
  watch,
} from 'vue';
import { useQueryList } from '@/hooks';
import { useI18n } from 'vue-i18n';
import { getGatewaysDocs } from '@/http';
import { useRouter } from 'vue-router';
import TableEmpty from '@/components/table-empty.vue';
import SdkInstructionSlider from '@/views/apigwDocs/components/sdk-instruction-slider.vue';
import useMaxTableLimit from '@/hooks/use-max-table-limit';
import SdkDetailDialog from '@/views/apigwDocs/components/sdk-detail-dialog.vue';
import { TabType } from '@/views/apigwDocs/types';

const { t } = useI18n();
const router = useRouter();

const filterData = ref({ keyword: '' });

const {
  tableData,
  pagination,
  isLoading,
  handlePageChange,
  handlePageSizeChange,
  getList,
} = useQueryList(getGatewaysDocs, filterData);


// 当前视口高度能展示最多多少条表格数据
const maxTableLimit = ref(10);
maxTableLimit.value = useMaxTableLimit(271);

// 注意，pagination 的 limit 必须在 limitList 里才能生效
// 所以要先放进 limitList 里
pagination.value.limitList.unshift(maxTableLimit.value);
pagination.value.limit = maxTableLimit.value;


// const handleGoApigw = () => {
//   window.open(window.BK_DASHBOARD_URL);
// };
const tableEmptyConf = ref<{keyword: string, isAbnormal: boolean}>({
  keyword: '',
  isAbnormal: false,
});

// 当前展示的是 网关 | 组件 相关内容
const curTab = ref<TabType>('apigw');

// 提供当前 tab 的值
// 注入时请使用：const curTab = inject<Ref<TabType>>('curTab');
provide('curTab', curTab);

const isSdkInstructionSliderShow = ref(false);
const isSdkDetailDialogShow = ref(false);

const gotoDetails = (data: any) => {
  router.push({
    name: 'apigwAPIDetailIntro',
    params: {
      apigwId: data?.name,
    },
  });
};

const handleClearFilterKey = () => {
  filterData.value = { keyword: '' };
  getList();
  updateTableEmptyConfig();
};

const updateTableEmptyConfig = () => {
  const searchParams = {
    ...filterData.value,
  };
  const list = Object.values(searchParams).filter(item => item !== '');
  tableEmptyConf.value.isAbnormal = pagination.value.abnormal;
  if (list.length && !tableData.value.length) {
    tableEmptyConf.value.keyword = 'placeholder';
    return;
  }
  if (list.length) {
    tableEmptyConf.value.keyword = '$CONSTANT';
    return;
  }
  tableEmptyConf.value.keyword = '';
};

watch(
  () => tableData.value, () => {
    updateTableEmptyConfig();
  },
  {
    deep: true,
  },
);

</script>

<style lang="scss" scoped>
.docs-main {

  .page-tabs {
    height: 52px;
    margin-bottom: 24px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #FFFFFF;
    box-shadow: 0 3px 4px 0 #0000000a;

    .tabs-group {
      display: flex;
      justify-content: center;

      .page-tab {
        width: 135px;
        height: 52px;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;

        &:hover {
          color: #3A84FF;
        }

        &.active {
          background-color: #F0F5FF;
          border-top: 3px solid #3A84FF;
          color: #3A84FF;
        }
      }
    }
  }

  .docs-main-content {
    width: 1280px;
    margin: auto;

    .top-bar {
      margin-bottom: 16px;
      display: flex;
      justify-content: flex-end;
      align-items: center;
    }

    .link-name {
      color: #3A84FF;
      cursor: pointer;
    }
  }
}
</style>
