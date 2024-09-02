<template>
  <div class="page-wrap">
    <header class="page-header">
      <!-- 默认头部 -->
      <main class="flex-row align-items-center header-main">
        <i
          class="icon apigateway-icon icon-ag-return-small"
          @click="handleGoBack()"
        ></i>
        {{ curTargetName }}
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
        :min="293"
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
              <div class="left">
                <div class="left-aside-wrap">
                  <header class="left-aside-header">
                    <header class="title">
                      {{ curTab === 'apigw' ? t('资源列表') : t('API列表') }}
                      <aside v-if="resourceList.length" class="sub-title">{{ filteredResourceList.length }}</aside>
                    </header>
                    <main class="nav-filters">
                      <article v-if="curTab === 'apigw'">
                        <bk-select
                          v-model="curStageName"
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
                        <bk-input
                          type="search"
                          v-model="keyword"
                          :placeholder="searchPlaceholder"
                          clearable
                        >
                        </bk-input>
                      </article>
                    </main>
                  </header>
                  <main class="resource-list custom-scroll-bar">
                    <template v-if="filteredResourceList.length">
                      <article
                        class="resource-item"
                        v-for="resource in filteredResourceList"
                        :key="resource.id"
                        :class="{ active: resource.id === curResource.id }"
                        @click="handleResClick(resource.id)"
                      >
                        <!-- eslint-disable-next-line vue/no-v-html -->
                        <header class="res-item-name" v-html="getHighlightedHtml(resource.name)" v-bk-overflow-tips
                        ></header>
                        <!-- eslint-disable-next-line vue/no-v-html -->
                        <main class="res-item-desc" v-html="getHighlightedHtml(resource.description)"></main>
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
                <DocDetailMainContent
                  :resource="curResource"
                  :nav-list="navList"
                  :markdown-html="curResMarkdownHtml"
                  :updated-time="updatedTime"
                  @show-sdk-instruction="isSdkInstructionSliderShow = true"
                ></DocDetailMainContent>
              </div>
            </template>
          </bk-resize-layout>
        </template>
        <template #aside>
          <aside class="aside-right">
            <main class="apigw-desc-wrap custom-scroll-bar">
              <DocDetailSideContent
                :basics="curTargetBasics"
                :sdks="sdks"
              ></DocDetailSideContent>
            </main>
          </aside>
        </template>
      </bk-resize-layout>
    </main>
    <!--  SDK使用说明 Slider  -->
    <SdkInstructionSlider v-model="isSdkInstructionSliderShow"></SdkInstructionSlider>
  </div>
</template>

<script lang="ts" setup>
import {
  computed,
  nextTick,
  onBeforeMount,
  provide,
  ref,
} from 'vue';
import { useI18n } from 'vue-i18n';
import {
  useRoute,
  useRouter,
} from 'vue-router';
import {
  getApigwResourceDocDocs,
  getApigwResourcesDocs,
  getApigwSDKDocs,
  getApigwStagesDocs,
  getComponenSystemDetail,
  getESBSDKDetail,
  getGatewaysDetailsDocs,
  getSystemAPIList,
  getSystemComponentDoc,
} from '@/http';
import {
  IApiGatewayBasics,
  IApiGatewaySdkDoc,
  IComponent,
  IComponentSdk,
  INavItem,
  IResource,
  IStage,
  ISystemBasics,
  LanguageType,
  TabType,
} from '@/views/apiDocs/types';
import MarkdownIt from 'markdown-it';
import { ResizeLayout } from 'bkui-vue';
import DocDetailMainContent from '@/views/apiDocs/components/doc-detail-main-content.vue';
import DocDetailSideContent from '@/views/apiDocs/components/doc-detail-side-content.vue';
import SdkInstructionSlider from '@/views/apiDocs/components/sdk-instruction-slider.vue';
import TableEmpty from '@/components/table-empty.vue';

const { t } = useI18n();
const route = useRoute();
const router = useRouter();

const curTab = ref<TabType>('apigw');
const board = ref('default');
// 提供当前 tab 的值
// 注入时请使用：const curTab = inject<Ref<TabType>>('curTab');
provide('curTab', curTab);

const stageList = ref<IStage[]>([]);
const curStageName = ref('');
const keyword = ref('');
const curTargetName = ref('');
const curTargetBasics = ref<IApiGatewayBasics & ISystemBasics | null>(null);
const resourceList = ref<(IResource & IComponent)[]>([]);
const curComponentName = ref('');
const curResource = ref<IResource & IComponent | null>(null);
const curResMarkdownHtml = ref('');
const updatedTime = ref<string | null>(null);
const sdks = ref<IApiGatewaySdkDoc[] & IComponentSdk[]>([]);
const isSdkInstructionSliderShow = ref(false);
const navList = ref<INavItem[]>([]);
const outerResizeLayoutRef = ref<InstanceType<typeof ResizeLayout> | null>(null);
// 记录右栏折叠状态
const isAsideVisible = ref(true);

const searchPlaceholder = computed(() => {
  return t(
    '在{resourceLength}个{type}中搜索...',
    {
      resourceLength: resourceList.value.length,
      type: curTab.value === 'apigw' ? t('资源') : 'API',
    },
  );
});

const filteredResourceList = computed(() => {
  return resourceList.value.filter(res => res.name.includes(keyword.value) || res.description.includes(keyword.value));
});

const fetchBasics = async () => {
  try {
    if (curTab.value === 'apigw') {
      curTargetBasics.value = await getGatewaysDetailsDocs(curTargetName.value);
    } else if (curTab.value === 'component') {
      curTargetBasics.value = await getComponenSystemDetail(board.value, curTargetName.value);
    }
  } catch {
    curTargetBasics.value = null;
  }
};

const fetchSdks = async (language: LanguageType = 'python') => {
  try {
    if (curTab.value === 'apigw') {
      const query = {
        limit: 10000,
        offset: 0,
        language,
      };
      sdks.value = await getApigwSDKDocs(curTargetName.value, query);
    } else if (curTab.value === 'component') {
      const res = await getESBSDKDetail(board.value, { language });
      sdks.value = res ? [{ language, ...res }] : [];
    }
  } catch {
    sdks.value = [];
  }
};

const fetchApigwStages = async () => {
  try {
    const query = {
      limit: 10000,
      offset: 0,
    };
    stageList.value = await getApigwStagesDocs(curTargetName.value, query);
    curStageName.value = stageList.value[0]?.name ?? '';
  } catch {
    stageList.value = [];
  }
};

const fetchResources = async () => {
  try {
    let res: (IResource & IComponent)[] = [];
    if (curTab.value === 'apigw') {
      const query = {
        limit: 10000,
        offset: 0,
        stage_name: curStageName.value,
      };
      res = await getApigwResourcesDocs(curTargetName.value, query) as (IResource & IComponent)[];
    } else if (curTab.value === 'component') {
      res = await getSystemAPIList(board.value, curTargetName.value) as (IResource & IComponent)[];
    }
    resourceList.value = res ?? [];
    if (curComponentName.value) {
      curResource.value = resourceList.value.find(resource => resource.name === curComponentName.value) ?? null;
    } else {
      curResource.value = resourceList.value[0] ?? null;
    }
    if (curResource.value) {
      await getApigwResourceDoc();
    }
  } catch {
    resourceList.value = [];
  }
};

const handleResClick = async (resId: number) => {
  if (curResource.value.id === resId) return;
  navList.value = [];
  curResource.value = resourceList.value.find(res => res.id === resId) ?? null;
  if (curResource.value) {
    await getApigwResourceDoc();
  }
};

const md = new MarkdownIt({
  linkify: false,
  html: true,
  breaks: true,
});

md.renderer.rules.heading_open = function (tokens, idx, options, env, self) {
  const curToken = tokens[idx];
  const nextToken = tokens[idx + 1];
  let count = 2;
  if (curToken.markup === '###' && nextToken?.type === 'inline') {
    let headingText = nextToken.content;
    if (navList.value.find(item => item.name === headingText)) {
      headingText = `${headingText}${count}`;
      count = count + 1;
    }
    curToken.attrPush(['id', headingText]);
    navList.value.push({ id: headingText, name: headingText });
  }
  return self.renderToken(tokens, idx, options);
};

const getApigwResourceDoc = async () => {
  let res: any;
  if (curTab.value === 'apigw') {
    const query = {
      stage_name: curStageName.value,
    };
    res = await getApigwResourceDocDocs(curTargetName.value, curResource.value.name, query);
  } else if (curTab.value === 'component') {
    res = await getSystemComponentDoc(board.value, curTargetName.value, curResource.value.name);
  }
  const { content, updated_time } = res;
  curResMarkdownHtml.value = md.render(content);
  updatedTime.value = updated_time;
};

const handleStageChange = async () => {
  await fetchResources();
};

const getHighlightedHtml = (value: string) => {
  if (keyword.value) {
    return value.replace(new RegExp(`(${keyword.value})`), '<em class="ag-keyword">$1</em>');
  }
  return value;
};

const init = async () => {
  if (curTab.value === 'apigw') {
    await fetchApigwStages();
  }
  await fetchBasics();
  await fetchSdks();
  await fetchResources();
};

const toggleAsideVisible = () => {
  nextTick(() => {
    outerResizeLayoutRef.value?.setCollapse(isAsideVisible.value);
  });
};

const updateIsRightAsideCollapsed = (collapsed: boolean) => {
  isAsideVisible.value = !collapsed;
};

const handleGoBack = () => {
  router.push({
    name: 'apiDocs',
    params: {
      curTab: curTab.value,
    },
  });
}

onBeforeMount(() => {
  const { params } = route;
  curTab.value = params.curTab as TabType || 'apigw';
  curTargetName.value = params.targetName as string;
  curComponentName.value = params.componentName as string || '';
  init();
});

</script>

<style lang="scss" scoped>

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
  margin: 0 auto;

  .left {
    padding: 16px 8px 0 0;
  }

  .left-aside-wrap {
    min-width: 280px;
    width: auto;
    box-shadow: 0 2px 4px 0 #1919290d;
    border-radius: 2px;
    background-color: #ffffff;

    .left-aside-header {
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

        .res-item-name,
        .res-item-desc {
          display: -webkit-box;
          -webkit-line-clamp: 1;
          -webkit-box-orient: vertical;
          overflow: hidden;
        }

        .res-item-name {
          font-size: 14px;
          color: #313238;
          line-height: 22px;
        }

        .res-item-desc {
          font-size: 12px;
          color: #979ba5;
          line-height: 20px;
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

  .main-content-wrap {
    padding-top: 16px;
  }

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
