<template>
  <div class="page-wrap">
    <header class="page-header">
      <!-- 默认头部 -->
      <main class="flex-row align-items-center header-main">
        <i
          class="icon apigateway-icon icon-ag-return-small"
          @click="router.back()"
        ></i>
        {{ curTargetId }}
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
        ref="outerResizeLayoutRef"
        placement="right"
        :border="false"
        collapsible
        initial-divide="392px"
        :max="480"
        :min="392"
        style="flex-grow: 1;"
        @collapse-change="updateIsRightAsideCollapsed"
      >
        <template #main>
          <bk-resize-layout
            placement="left"
            style="margin-left: 40px;"
            initial-divide="288px"
            :max="400"
            :min="288"
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
                  <main class="resource-list custom-scroll-bar">
                    <template v-if="resourceList.length">
                      <article
                        class="resource-item"
                        v-for="resource in resourceList"
                        :key="resource.id"
                        @click="handleResClick(resource.id)"
                      >
                        <header class="res-item-name">{{ resource.name }}</header>
                        <main class="res-item-desc">{{ resource.description }}</main>
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
              <div class="main-content-wrap">
                <DetailMainContent
                  :resource="curResource"
                  :nav-list="navList"
                  :markdown-html="curResMarkdownHtml"
                  :updated-time="updatedTime"
                ></DetailMainContent>
              </div>
            </template>
          </bk-resize-layout>
        </template>
        <template #aside>
          <aside class="aside-right">
            <main class="apigw-desc-wrap custom-scroll-bar">
              <DocDetailSideContent :target-id="curTargetId"></DocDetailSideContent>
            </main>
          </aside>
        </template>
      </bk-resize-layout>
    </main>
  </div>
</template>

<script lang="ts" setup>
import {
  ref,
  computed,
  watch,
  nextTick,
  onMounted,
  inject,
  Ref,
  provide,
  onBeforeMount,
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
  getApigwResourceDocDocs,
  getComponenSystemDetail,
  getSystemAPIList,
  getSystemComponentDoc,
} from '@/http';
import TableEmpty from '@/components/table-empty.vue';
import DocDetailSideContent from '@/views/apigwDocs/components/doc-detail-side-content.vue';
import {
  IComponent,
  IResource,
  TabType,
} from '@/views/apigwDocs/types';
import DetailMainContent from '@/views/apigwDocs/components/detail-main-content.vue';
import MarkdownIt from 'markdown-it';
import hljs from 'highlight.js';
import { slugify } from 'transliteration';
import { copy } from '@/common/util';
import { ResizeLayout } from 'bkui-vue';

const { t } = useI18n();
const route = useRoute();
const router = useRouter();

const curApigwId = ref<any>(0);
const curTargetId = ref('');
const curApigw = ref<any>({});
const resourceList = ref<IResource[] | IComponent[]>([]);
const stageList = ref<any>([]);
const curStageId = ref<any>('');
const curComponentName = ref<any>('');
const keyword = ref<string>('');
const curResource = ref<IResource | IComponent | null>(null);
const mainContentLoading = ref<boolean>(false);
const navList = ref<{ id: number, name: string }[]>([
  { id: 1, name: t('API 地址') },
  { id: 2, name: t('公共请求参数') },
]);
const outerResizeLayoutRef = ref<InstanceType<typeof ResizeLayout> | null>(null);

const curTab = ref<TabType>('apigw');

// 提供当前 tab 的值
// 注入时请使用：const curTab = inject<Ref<TabType>>('curTab');
provide('curTab', curTab);

const searchPlaceholder = computed(() => {
  return t('在{resourceLength}个资源中搜索...', { resourceLength: resourceList.value?.length });
});

const getApigwAPIDetail = async () => {
  try {
    const res = await getGatewaysDetailsDocs(curTargetId.value);
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
    const res = await getApigwStagesDocs(curTargetId.value, query);
    stageList.value = res;
    if (route.params.stage) {
      curStageId.value = route.params.stage;
    } else if (stageList.value?.length) {
      curStageId.value = stageList.value[0]?.name;
    } else {
      curStageId.value = '';
    }
    await fetchResources();
  } catch (e) {
    console.log(e);
  }
};

const getApigwAPI = async () => {
  const pageParams = {
    limit: 10000,
    offset: 0,
  };
  try {
    const res = await getGatewaysDocs('', pageParams);
  } catch (e) {
    console.log(e);
  }
};

const fetchResources = async () => {
  try {
    let res: IResource[] | IComponent[] = [];
    if (curTab.value === 'apigw') {
      if (stageList.value.length) {
        const query = {
          limit: 10000,
          offset: 0,
          stage_name: curStageId.value,
        };
        res = await getApigwResourcesDocs(curTargetId.value, query) as IResource[];
      } else {
        resourceList.value = [];
      }
    } else if (curTab.value === 'component') {
      res = await getSystemAPIList('default', curTargetId.value) as IComponent[];
    }
    resourceList.value = res ?? [];
    curResource.value = resourceList.value[0] ?? null;
    if (curResource.value) {
      await getApigwResourceDoc();
    }
  } catch {
    resourceList.value = [];
  }
};

const reset = () => {
  curComponentName.value = '';
};

const handleResClick = async (resId: number) => {
  curResource.value = resourceList.value.find(res => res.id === resId) ?? null;
  if (curResource.value) {
    await getApigwResourceDoc();
  }
};

const md = new MarkdownIt({
  linkify: false,
  html: true,
  breaks: true,
  highlight(str: string, lang: string) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(lang, str, true).value;
      } catch (__) {
      }
    }

    return '';
  },
});

const curResMarkdownHtml = ref('');
const updatedTime = ref<string | null>(null);

const getApigwResourceDoc = async () => {
  try {
    let res: any;
    if (curTab.value === 'apigw') {
      const query = {
        stage_name: curStageId.value,
      };
      res = await getApigwResourceDocDocs(curTargetId.value, curResource.value.name, query);
    } else if (curTab.value === 'component') {
      res = await getSystemComponentDoc('default', curTargetId.value, curResource.value.name);
    }
    const { content, updated_time } = res;
    curResMarkdownHtml.value = md.render(content);
    updatedTime.value = updated_time;
  } catch (e) {
    console.log(e);
  } finally {
  }
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
  // router.push({
  //   name: 'apigwAPIDetailIntro',
  // });
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
  // router.push({
  //   name: 'apigwAPIDetailIntro',
  //   params: {
  //     apigwId: data,
  //   },
  //   query: {
  //     stage: curStageId.value,
  //   },
  // });
};

const handleStageChange = async () => {
  reset();
  await fetchResources();
  const match = resourceList.value?.find((resource: any) => curResource.value?.name === resource.name);
  if (match) {
    // handleShowDoc(match);
  } else {
    handleShowIntro();
  }
  // router.push({
  //   query: { stage: curStageId.value },
  // });
};

const init = async () => {
  // getApigwAPI();
  if (curTab.value === 'apigw') {
    await getApigwStages();
  } else if (curTab.value === 'component') {
    await fetchResources();
  }
  await getApigwAPIDetail();
};

// 记录右栏折叠状态
const isAsideVisible = ref(true);

const toggleAsideVisible = () => {
  nextTick(() => {
    outerResizeLayoutRef.value?.setCollapse(isAsideVisible.value);
  });
};

const updateIsRightAsideCollapsed = (collapsed: boolean) => {
  isAsideVisible.value = !collapsed;
};

onBeforeMount(() => {
  const params = route.params;
  curTargetId.value = params.targetId as string;
  curTab.value = params.curTab as TabType || 'apigw';
  init();
});

// onBeforeRouteUpdate((to, from) => {
//   console.log(to);
//   console.log(from);
// });

// watch(
//   () => route,
//   (payload: any) => {
//     console.log('doc-detail.vue');
//     if (payload.params?.apigwId) {
//       console.log('=>(doc-detail.vue:538) payload', payload.params);
//       curApigw.value = { name: payload.params.apigwId };
//       curTab.value = payload.params?.curTab || 'apigw';
//       init();
//     }
//   },
//   { immediate: true, deep: true },
// );

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
  //align-items: stretch;

  .simple-side-nav {
    min-width: 280px;
    width: auto;
    box-shadow: 0 2px 4px 0 #1919290d;
    border-radius: 2px;

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
          line-height: 20px;
          display: -webkit-box;
          -webkit-line-clamp: 1;
          -webkit-box-orient: vertical;
          overflow-y: hidden;
        }

        &:hover, &.active {
          background: #e1ecff;

          .res-item-name {
            color: #3a84ff;
          }
        }
      }
    }
  }

  //.main-content-wrap {
  //  width: calc(100vw - 612px);
  //}

  .aside-right {
    .apigw-desc-wrap {
      height: calc(100vh - 144px);
      overflow-y: scroll;
      background-color: #fff;
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

.custom-scroll-bar {
  &::-webkit-scrollbar {
    width: 4px;
    background-color: lighten(#c4c6cc, 80%);
  }

  &::-webkit-scrollbar-thumb {
    height: 5px;
    border-radius: 2px;
    background-color: #c4c6cc;
  }

  &::-webkit-scrollbar-track {
    background: transparent;
  }
}
</style>
