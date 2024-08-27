<template>
  <div class="page-wrap">
    <header class="page-header">
      <!-- 默认头部 -->
      <main class="flex-row align-items-center header-main">
        <i
          class="icon apigateway-icon icon-ag-return-small"
          @click="router.back()"
        ></i>
        {{ curApigw.name }}
        <!--        <div class="title-name">-->
        <!--          <span></span>-->
        <!--          <div class="name"></div>-->
        <!--        </div>-->
      </main>
      <aside
        class="detail-toggle"
        :class="{ 'active': isAsideVisible }"
        @click="toggleAsideVisible()"
      ><i class="apigateway-icon icon-ag-document f14"></i>
      </aside>
    </header>
    <main class="page-content">
      <bk-resize-layout
        placement="right"
        :border="false"
        collapsible
        style="height: 800px; flex-grow: 1;"
      >
        <template #main>
          <bk-resize-layout
            placement="left"
            style="height: 800px;margin-left: 40px;"
            initial-divide="288px"
            :border="false"
          >
            <template #aside>
              <div class="left pr8">
                <div class="simple-side-nav">
                  <header class="side-nav-header">
                    <header class="title">
                      {{ t('资源列表') }}
                      <aside v-if="resourceList.length" class="sub-title">{{ resourceList.length }}</aside>
                    </header>
                    <main class="nav-filters">
                      <article>
                        <bk-select
                          v-model="curStageId"
                          style=""
                          :clearable="false"
                          filterable
                          :input-search="false"
                          :prefix="t('环境')"
                          @change="handleStageChange"
                        >
                          <bk-option
                            v-for="option in stageList"
                            :key="option.id"
                            :value="option.name"
                            :label="option.name"
                          >
                          </bk-option>
                        </bk-select>
                      </article>
                      <article>
                        <!-- 环境切换时添加 query参数 ， 根据query参数切换对应的环境 -->
                        <bk-input
                          :placeholder="searchPlaceholder"
                          type="search"
                          clearable
                          v-model="keyword"
                        >
                        </bk-input>
                      </article>
                    </main>
                  </header>
                  <main class="resource-list">
                    <template v-if="Object.keys(resourceGroup).length">
                      <article class="resource-item" v-for="resource in resourceList" :key="resource.id">
                        <header class="res-item-name">{{ t(resource.name) }}</header>
                        <main class="res-item-desc">{{ t(resource.description) }}</main>
                      </article>
                    </template>
                    <template v-else-if="keyword">
                      <TableEmpty
                        :keyword="keyword"
                        @clear-filter="keyword = ''"
                      />
                    </template>
                  </main>
                </div>
              </div>
            </template>
            <template #main>
              <div class="right">
                <bk-loading
                  :loading="mainContentLoading"
                >
                  <router-view></router-view>
                </bk-loading>
              </div>
            </template>
          </bk-resize-layout>
        </template>
        <template #aside>右侧slider</template>
      </bk-resize-layout>
    </main>
  </div>
</template>

<script lang="ts" setup>
import {
  ref,
  computed,
  watch,
} from 'vue';
import { useI18n } from 'vue-i18n';
import {
  useRoute,
  useRouter,
} from 'vue-router';
import {
  getGatewaysDetailsDocs,
  getApigwStagesDocs,
  getGatewaysDocs,
  getApigwResourcesDocs,
} from '@/http';
import { useToggle } from '@vueuse/core';
import TableEmpty from '@/components/table-empty.vue';

const { t } = useI18n();
const route = useRoute();
const router = useRouter();

const [isAsideVisible, toggleAsideVisible] = useToggle(false);

const curApigwId = ref<any>(0);
const curApigw = ref<any>({});
const resourceList = ref<any>([]);
const stageList = ref<any>([]);
const curStageId = ref<any>('');
const originResourceGroup = ref<any>({});
const curComponentName = ref<any>('');
const activeName = ref<any>([]);
const apigwList = ref<any>([]);
const keyword = ref<string>('');
const curResource = ref<any>({});
const mainContentLoading = ref<boolean>(false);

const searchPlaceholder = computed(() => {
  return t('在{resourceLength}个资源中搜索...', { resourceLength: resourceList.value?.length });
});

const routeName = computed(() => route.name);

const curGroup = computed(() => {
  for (const key of Object.keys(originResourceGroup.value)) {
    const cur = originResourceGroup.value[key];
    const match = cur?.resources?.find((item: any) => {
      return item.name === curComponentName.value;
    });
    if (match) {
      return cur;
    }
  }
  return null;
});

const resourceGroup = computed(() => {
  const group: any = {};
  let keys = Object.keys(originResourceGroup.value).sort();

  if (keys.includes('默认')) {
    const list = keys.filter(item => item !== '默认');
    keys = [
      '默认',
      ...list,
    ];
  }
  for (const key of keys) {
    const resources: any = [];
    const obj: any = {};
    const item = originResourceGroup.value[key];
    item?.resources?.forEach((resource: any) => {
      if ((resource.name || '').indexOf(keyword.value) > -1 || (resource.description || '').indexOf(keyword.value) > -1) {
        resources.push(resource);
      }
    });
    if (resources.length) {
      obj.labelId = item.labelId;
      obj.labelName = item.labelName;
      obj.resources = resources;
      group[key] = obj;
    }
  }
  return group;
});

const getApigwAPIDetail = async () => {
  try {
    const res = await getGatewaysDetailsDocs(curApigwId.value);
    curApigw.value = res;
  } catch (e) {
    console.log(e);
  }
};

const getApigwStages = async () => {
  if (stageList.value.length) {
    return;
  }
  try {
    const query = {
      limit: 10000,
      offset: 0,
    };
    const res = await getApigwStagesDocs(curApigwId.value, query);
    stageList.value = res;
    if (route.params.stage) {
      curStageId.value = route.params.stage;
    } else if (stageList.value?.length) {
      curStageId.value = stageList.value[0]?.name;
    } else {
      curStageId.value = '';
    }
    // query参数是的环境是否存在
    const queryStage = route.query.stage;
    // prod为默认环境
    const prodStage = stageList.value?.find((item: any) => item.name === 'prod');
    const resStage = prodStage ? prodStage.name : stageList.value[0]?.name;
    if (queryStage) {
      const stageDetils = stageList.value?.filter((item: any) => item.name === queryStage);
      if (stageDetils.length) {
        curStageId.value = queryStage;
      } else {
        curStageId.value = resStage;
        router.push({
          name: 'apigwAPIDetailIntro',
          params: {
            apigwId: curApigwId.value,
          },
          query: {
            stage: curStageId.value,
          },
        });
      }
    } else {
      curStageId.value = resStage;
      router.push({
        name: 'apigwAPIDetailIntro',
        params: {
          apigwId: curApigwId.value,
        },
        query: {
          stage: curStageId.value,
        },
      });
    }
    await getApigwResources();
  } catch (e) {
    console.log(e);
  }
};

const getApigwAPI = async () => {
  if (apigwList.value.length) {
    return;
  }
  const pageParams = {
    limit: 10000,
    offset: 0,
  };
  try {
    const res = await getGatewaysDocs('', pageParams);
    apigwList.value = res?.results;
  } catch (e) {
    console.log(e);
  }
};

const getApigwResources = async () => {
  if (stageList.value.length) {
    try {
      const query = {
        limit: 10000,
        offset: 0,
        stage_name: curStageId.value,
      };
      const res = await getApigwResourcesDocs(curApigwId.value, query);
      const group: any = {};
      const defaultItem: any = {
        labelId: 'default',
        labelName: t('默认'),
        resources: [],
      };
      resourceList.value = res;
      resourceList.value?.forEach((resource: any) => {
        const { labels } = resource;
        if (labels?.length) {
          labels.forEach((label: any) => {
            if (typeof label === 'object') {
              if (group[label.id]) {
                group[label.id]?.resources.push(resource);
              } else {
                if (group[label.name]) {
                  group[label.name]?.resources.push(resource);
                } else {
                  const obj = {
                    labelId: label.id,
                    labelName: label.name,
                    resources: [resource],
                  };
                  group[label.name] = obj;
                }
              }
            } else {
              if (group[label]) {
                group[label]?.resources?.push(resource);
              } else {
                const obj = {
                  labelId: label,
                  labelName: label,
                  resources: [resource],
                };
                group[label] = obj;
              }
            }
          });
        } else {
          defaultItem.resources.push(resource);
        }
      });
      if (defaultItem.resources.length) {
        group['默认'] = defaultItem;
      }
      originResourceGroup.value = group;
    } catch (e) {
      console.log(e);
    }
  } else {
    originResourceGroup.value = {};
    resourceList.value = [];
  }
};

const reset = () => {
  curComponentName.value = '';
};

const handleShowDoc = (resource: any) => {
  curResource.value = resource;
  curComponentName.value = resource.name;

  router.push({
    name: 'apigwAPIDetailDoc',
    params: {
      apigwId: curApigwId.value,
      stage: curStageId.value,
      resourceId: resource.name,
    },
    query: {
      stage: curStageId.value,
    },
  });
};

const handleShowIntro = () => {
  curComponentName.value = '';
  router.push({
    name: 'apigwAPIDetailIntro',
  });
};

const hightlight = (value: string) => {
  if (keyword.value) {
    return value.replace(new RegExp(`(${keyword.value})`), '<em class="ag-keyword">$1</em>');
  }
  return value;
};

const handleApigwChange = async (data: string) => {
  reset();
  stageList.value = [];
  curApigwId.value = data;
  await getApigwStages();
  router.push({
    name: 'apigwAPIDetailIntro',
    params: {
      apigwId: data,
    },
    query: {
      stage: curStageId.value,
    },
  });
};

const handleStageChange = async () => {
  reset();
  await getApigwResources();
  const match = resourceList.value?.find((resource: any) => curResource.value?.name === resource.name);
  if (match) {
    handleShowDoc(match);
  } else {
    handleShowIntro();
  }
  router.push({
    query: { stage: curStageId.value },
  });
};

const init = async () => {
  const curRoute = route as any;
  const routeParams = route.params;
  curApigwId.value = routeParams.apigwId;
  curComponentName.value = routeParams.resourceId;
  // 回到页头
  const container = document.documentElement || document.body;
  container.scrollTo({
    top: 0,
    behavior: 'smooth',
  });
  getApigwAPI();
  if ([
    'apigwAPIDetailIntro',
    'apigwAPIDetailDoc',
  ].includes(curRoute.name)) {
    await getApigwStages();
    return;
  }
  getApigwAPIDetail();
};

watch(
  () => keyword.value,
  (val) => {
    const keys = Object.keys(resourceGroup.value);
    if (val) {
      activeName.value = keys;
    } else if (curGroup.value) {
      activeName.value = [curGroup.value?.labelName];
    } else {
      activeName.value = [keys[0]];
    }
  },
);

watch(
  () => curGroup.value,
  () => {
    if (curGroup.value) {
      activeName.value = [curGroup.value?.labelName];
    }
  },
);

watch(
  () => resourceGroup.value,
  () => {
    if (!activeName.value?.length) {
      activeName.value = [Object.keys(resourceGroup.value)[0]];
    }
  },
);

watch(
  () => route,
  (payload: any) => {
    if (payload.params?.apigwId) {
      curApigw.value = { name: payload.params?.apigwId };
      init();
    }
  },
  { immediate: true, deep: true },
);

</script>

<style lang="scss" scoped>
@import './detail.css';

//.page-wrap {
//  height: 100%;
//}

.page-header {
  position: sticky;
  top: 0;
  padding-inline: 24px;
  background: #fff;
  border-bottom: 1px solid #dcdee5;
  box-shadow: 0 3px 4px 0 #0000000a;
  height: 52px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 1;

  .header-main {
    flex-grow: 1;
    display: flex;
    flex-basis: 52px;
    box-sizing: border-box;
    margin-right: auto;
    color: #313238;
    font-size: 16px;

    .icon-ag-return-small {
      font-size: 32px;
      color: #3a84ff;
      cursor: pointer;
    }

    .title-name {
      display: flex;
      align-items: center;
      margin-left: 8px;

      span {
        width: 1px;
        height: 14px;
        background: #dcdee5;
        margin-right: 8px;
      }

      .name {
        font-size: 14px;
        color: #979ba5;
      }
    }
  }

  .detail-toggle {
    width: 28px;
    height: 28px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #fff;
    border-radius: 2px;
    color: #63656e;
    cursor: pointer;

    &:hover {
      background: #f0f1f5;
    }

    &.active {
      background: #e1ecff;
      color: #3a84ff;
    }
  }
}

.page-content {
  display: flex;
  margin: 16px auto 20px auto;
  align-items: stretch;

  .simple-side-nav {
    min-width: 280px;
    width: auto;

    .side-nav-header {
      padding: 16px 24px 12px;

      .title {
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        font-size: 14px;
        color: #313238;
        letter-spacing: 0;
        line-height: 22px;

        .sub-title {
          margin-left: 8px;
          display: flex;
          justify-content: center;
          align-items: center;
          width: 30px;
          height: 16px;
          background: #f0f1f5;
          border-radius: 2px;
          font-size: 12px;
          color: #979ba5;
        }
      }

      .nav-filters {
        display: flex;
        flex-direction: column;
        gap: 12px;
      }
    }

    .resource-list {
      height: calc(100vh - 282px);
      overflow-y: scroll;

      .resource-item {
        padding-left: 24px;
        height: 52px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        background: #fff;
        cursor: pointer;

        .res-item-name {
          font-size: 14px;
          color: #313238;
          letter-spacing: 0;
          line-height: 22px;
        }

        .res-item-desc {
          font-size: 12px;
          color: #979ba5;
          letter-spacing: 0;
          line-height: 20px;
        }

        &:hover, &.active {
          background: #e1ecff;

          .res-item-name {
            color: #3a84ff;
          }
        }
      }

      &::-webkit-scrollbar {
        width: 4px;
        background-color: lighten(#c4c6cc, 80%);
      }

      &::-webkit-scrollbar-thumb {
        height: 5px;
        border-radius: 2px;
        background-color: #c4c6cc;
      }
    }
  }

  // 去掉左侧伸缩栏的拉伸线
  :deep(.bk-resize-layout-left>.bk-resize-layout-aside) {
    padding-right: 8px;
    border-right: none;
  }

  // 去掉右侧伸缩栏的拉伸线
  :deep(.bk-resize-layout-right>.bk-resize-layout-aside) {
    border-left: none;
  }

  // 隐藏的折叠按钮
  :deep(.bk-resize-layout > .bk-resize-layout-aside .bk-resize-collapse) {
    display: none !important;
  }
}
</style>
