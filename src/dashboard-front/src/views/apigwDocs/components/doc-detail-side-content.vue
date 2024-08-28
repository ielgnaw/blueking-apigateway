<template>
  <div class="intro-side-content-wrap">
    <header class="intro-header">
      <main v-if="curTab === 'apigw'" class="title">{{ t('网关详情') }}</main>
      <main v-else-if="curTab === 'component'" class="title">{{ t('组件详情') }}</main>
      <aside>
        <chat
          v-if="userStore.featureFlags?.ALLOW_CREATE_APPCHAT"
          :default-user-list="userList"
          :owner="curUser.username"
          :name="chatName"
          :content="chatContent"
          :is-query="true"
        >
        </chat>
      </aside>
    </header>
    <main v-if="curTab === 'apigw'" class="component-content">
      <div class="ag-markdown-view" id="markdown">
        <header class="content-title">{{ t('网关描述') }}</header>
        <main class="content-main">{{ curApigw.description }}</main>
        <header class="content-title">{{ t('网关负责人') }}</header>
        <main class="content-main">{{ curApigw.maintainers.join(', ') }}</main>
        <header class="content-title">{{ t('网关访问地址') }}</header>
        <main class="content-main">{{ curApigw.api_url }}</main>
        <template v-if="userStore.featureFlags?.ENABLE_SDK">
          <header class="content-title">{{ t('网关 SDK') }}</header>
          <div class="bk-button-group">
            <bk-button class="is-selected">Python</bk-button>
          </div>
        </template>
      </div>

      <template v-if="userStore.featureFlags?.ENABLE_SDK">
        <bk-table
          style="margin-top: 15px;"
          :data="sdks"
          show-overflow-tooltip
          :border="['outer']"
          :size="'small'"
        >
          <!-- <template #empty>
          <table-empty
            :abnormal="isAbnormal"
            @reacquire="getApigwSDK('python')"
          />
        </template> -->

          <bk-table-column :label="t('网关环境')" field="stage_name">
            <template #default="{ data }">
              {{ data?.stage?.name || '--' }}
            </template>
          </bk-table-column>

          <bk-table-column :label="t('网关API资源版本')" field="resource_version_display">
            <template #default="{ data }">
              {{ data?.resource_version?.version || '--' }}
            </template>
          </bk-table-column>

          <bk-table-column :label="t('SDK 版本号')" field="sdk_version_number">
            <template #default="{ data }">
              {{ data?.sdk?.version || '--' }}
            </template>
          </bk-table-column>

          <bk-table-column :label="t('SDK下载')">
            <template #default="{ data }">
              <template v-if="data?.sdk?.url">
                <bk-button theme="primary" class="mr5" text @click="handleShow(data)"> {{ t('查看') }}</bk-button>
                <bk-button theme="primary" text @click="handleDownload(data)"> {{ t('下载') }}</bk-button>
              </template>
              <template v-else>
                {{ t('未生成-doc') }}
              </template>
            </template>
          </bk-table-column>
        </bk-table>

        <p class="ag-tip mt5">
          <info-line style="margin-right: 8px;" />
          {{ t('若资源版本对应的SDK未生成，可联系网关负责人生成SDK') }}
        </p>
      </template>
    </main>
    <main v-else-if="curTab === 'component'" class="component-content">
      <div class="ag-markdown-view">
        <header class="content-title">{{ t('网关描述') }}</header>
        <main class="content-main">{{ curApigw.comment }}</main>
        <header class="content-title">{{ t('网关负责人') }}</header>
        <main class="content-main">{{ curApigw.maintainers.join(', ') }}</main>
        <header class="content-title">{{ t('组件 API SDK') }}</header>
        <main class="content-main">
          <SdkDetail :params="curSdk"></SdkDetail>
        </main>
      </div>
    </main>
  </div>
</template>

<script lang="ts" setup>
import {
  ref,
  reactive,
  watch,
  nextTick,
  computed,
  onMounted,
  inject,
  Ref,
} from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute } from 'vue-router';
import { slugify } from 'transliteration';
import chat from '@/components/chat/index.vue';
import SdkDetail from './sdk-detail.vue';
import {
  getGatewaysDetailsDocs,
  getApigwSDKDocs,
  getComponenSystemDetail,
  getESBSDKDetail,
} from '@/http';
import { InfoLine } from 'bkui-vue/lib/icon';
import { useUser } from '@/store';
import { TabType } from '@/views/apigwDocs/types';

const userStore = useUser();
const route = useRoute();
const { t } = useI18n();
const sdks = ref<any>([]);
const sdkConfig = reactive({
  title: '',
  isShow: false,
});
const curSdk = ref<any>({});
const curApigw = ref<any>({
  id: 2,
  name: '',
  description: '',
  maintainers: [],
  is_official: '',
  api_url: '',
});
const isAbnormal = ref<boolean>(false);
const curApigwId = ref();

// 注入当前的总 tab 变量
const curTab = inject<Ref<TabType>>('curTab');

const props = defineProps({
  targetId: {
    type: String,
    default: '',
  },
});

const curUser = computed(() => userStore?.user);
const userList = computed(() => {
  // 去重
  const set = new Set([
    curUser.value?.username,
    ...curApigw.value?.maintainers,
  ]);
  return [...set];
});
const chatName = computed(() => `${t('[蓝鲸网关API咨询] 网关')}${curApigw.value?.name}`);
const chatContent = computed(() => `${t('网关API文档')}:${location.href}`);

const handleShow = (data: any) => {
  curSdk.value = data;
  sdkConfig.title = `${t('网关API SDK')}：${curApigwId.value}`;
  sdkConfig.isShow = true;
};

const handleDownload = (data: any) => {
  window.open(data?.sdk?.url);
};

const initMarkdownHtml = () => {
  nextTick(() => {
    const markdownDom = document.getElementById('markdown');
    // 复制代码
    markdownDom.querySelectorAll('a').forEach((item) => {
      item.target = '_blank';
    });
    markdownDom.querySelectorAll('pre').forEach((item) => {
      const btn = document.createElement('button');
      const codeBox = document.createElement('div');
      const code = item.querySelector('code').innerText;
      btn.className = 'ag-copy-btn';
      codeBox.className = 'code-box';
      btn.innerHTML = '<span :title="t(`复制`)"><i class="bk-icon icon-clipboard mr5"></i></span>';
      btn.setAttribute('data-clipboard-text', code);
      item.appendChild(btn);
      codeBox.appendChild(item.querySelector('code'));
      item.appendChild(codeBox);
    });
  });
};

const getApigwAPIDetail = async () => {
  try {
    const res = await getGatewaysDetailsDocs(curApigwId.value);
    curApigw.value = res;
  } catch (e) {
    console.log(e);
  } finally {
  }
};

// 获取当前system 的信息
const getSystemDetail = async () => {
  try {
    const res = await getComponenSystemDetail('default', curApigwId.value);
    curApigw.value = res;
  } catch (error) {
    console.log('error', error);
  }
};

const getApigwSDK = async (language: string) => {
  try {
    const query = {
      limit: 10000,
      offset: 0,
      language,
    };
    const res = await getApigwSDKDocs(curApigwId.value, query);
    sdks.value = res;
    isAbnormal.value = false;
  } catch (e) {
    isAbnormal.value = true;
    console.log(e);
  }
};

// 获取当前SDK的信息
const getSDKDetail = async () => {
  try {
    const res = await getESBSDKDetail('default', { language: 'python' });
    curSdk.value = {
      sdk: {
        name: res.sdk_name,
        version: res.sdk_version_number,
        url: res.sdk_download_url,
        install_command: res.sdk_install_command,
      },
    };
  } catch (error) {
    console.log('error', error);
  }
};

const init = async () => {
  curApigwId.value = props.targetId;
  if (curTab.value === 'apigw') {
    await getApigwAPIDetail();
  } else if (curTab.value === 'component') {
    await getSystemDetail();
    await getSDKDetail();
  }
  await getApigwSDK('python');
  initMarkdownHtml();
};

onMounted(() => {
  init();
});

</script>

<style lang="scss" scoped>
.intro-side-content-wrap {
  padding: 0 24px 12px 24px;

  .intro-header {
    margin-bottom: 12px;
    height: 48px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .component-content {
    width: auto;

    .ag-markdown-view {
      .content-title,
      .content-main {
        font-size: 14px;
        color: #63656E;
        letter-spacing: 0;
        line-height: 22px;
      }

      .content-title {
        margin-bottom: 12px;
        font-weight: 700;
      }

      .content-main {
        margin-bottom: 32px;
      }
    }
  }
}
</style>
