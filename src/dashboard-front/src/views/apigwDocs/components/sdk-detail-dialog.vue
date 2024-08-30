<template>
  <!--  查看 SDK 弹窗  -->
  <bk-dialog
    v-model:is-show="isShow"
    title="网关API SDK:"
    class="custom-main-dialog"
    width="640"
    mask-close
  >
    <main class="dialog-content">
      <div class="dialog-main">
        <LangSelector v-model="language" :sdk-languages="sdks.map(item => item.language)"></LangSelector>
        <div class="data-box">
          <article class="row-item">
            <aside class="key">
              <span class="column-key"> {{ t('SDK包名称') }}: </span>
            </aside>
            <main class="value">
              <span class="column-value" v-bk-overflow-tips>{{ curSdk.name ?? '--' }}</span>
            </main>
          </article>
          <article class="row-item">
            <aside class="key">
              <span class="column-key"> {{ t('SDK版本') }}: </span>
            </aside>
            <main class="value">
              <span class="column-value" v-bk-overflow-tips>{{ curSdk.version ?? '--' }}</span>
            </main>
          </article>
          <article class="row-item">
            <aside class="key">
              <span class="column-key"> {{ t('SDK地址') }}: </span>
            </aside>
            <main class="value flex-row align-items-center">
              <bk-popover placement="top" width="600" theme="dark" :disabled="!curSdk.url">
                <span class="column-value vm">{{ curSdk.url ?? '--' }}</span>
                <template #content>
                  <div class="popover-text">
                    {{ curSdk.url }}
                  </div>
                </template>
              </bk-popover>
              <i
                @click="copy(curSdk.url)"
                class="doc-copy vm icon-hover apigateway-icon icon-ag-copy ag-doc-icon"
                v-if="curSdk.url" v-bk-tooltips="t('复制')"
                :data-clipboard-text="curSdk.url"
              ></i>
              <i
                class="ag-doc-icon doc-download-line vm icon-hover apigateway-icon icon-ag-download-line"
                v-if="curSdk.url" v-bk-tooltips="t('下载')" @click="handleDownload"
              ></i>
            </main>
          </article>
          <article class="row-item">
            <aside class="key">
              <span class="column-key"> {{ t('安装') }}: </span>
            </aside>
            <main class="value flex-row align-items-center">
              <bk-popover placement="top" width="600" theme="dark" :disabled="!curSdk.install_command">
                <span class="column-value vm">{{ curSdk.install_command || '--' }}</span>
                <template #content>
                  <div class="popover-text">
                    {{ curSdk.install_command }}
                  </div>
                </template>
              </bk-popover>
              <i
                @click="copy(curSdk.install_command)"
                class="ag-doc-icon doc-copy vm icon-hover apigateway-icon icon-ag-copy"
                v-if="curSdk.install_command" v-bk-tooltips="t('复制')"
                :data-clipboard-text="curSdk.install_command"
              >
              </i>
            </main>
          </article>
          <article class="row-item">
            <aside class="key">
              <span class="column-key">
                {{ t('资源版本') }}
                <span v-bk-tooltips="t('该SDK关联的API资源版本')">
                  <i class="icon apigateway-icon icon-ag-help"></i>
                </span>
                :
              </span>
            </aside>
            <main class="value">
              <span
                class="column-value"
                v-bk-tooltips.top="{ content: curSdk.version, allowHTML: false }"
              >
                {{ curSdk.version ?? '--' }}
              </span>
            </main>
          </article>
        </div>
      </div>
    </main>
  </bk-dialog>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import {
  computed,
  defineModel,
  ref,
  toRefs,
} from 'vue';
import { copy } from '@/common/util';
import LangSelector from '@/views/apigwDocs/components/lang-selector.vue';
import {
  IApiGatewaySdk,
  LanguageType,
} from '@/views/apigwDocs/types';

const { t } = useI18n();

const isShow = defineModel<boolean>({
  required: true,
  default: false,
});

interface IProps {
  sdks: IApiGatewaySdk[];
}

const props = withDefaults(defineProps<IProps>(), {
  sdks: () => [],
});

const { sdks } = toRefs(props);

const language = ref<LanguageType>('python');

const curSdk = computed(() => {
  const sdk = sdks.value.find((item: IApiGatewaySdk) => item.language === language.value);
  return sdk || {
    language: 'python',
    name: '--',
    version: '--',
    url: '--',
    install_command: '--',
  };
});

// 下载
const handleDownload = () => {
  if (curSdk.value?.url) {
    window.open(curSdk.value.url);
  }
};
</script>

<style scoped lang="scss">
.custom-main-dialog {
  :deep(.bk-dialog-title) {
    line-height: 28px;
  }

  :deep(.bk-dialog-content) {
    margin-top: 20px;
    padding-right: 8px;
  }

  :deep(.bk-modal-footer) {
    display: none;
  }

  .dialog-content {

    .dialog-main {

      .data-box {
        padding: 24px 12px;
        background: #f5f7fa;

        .row-item {
          display: flex;
          line-height: 40px;

          .key {
            width: 100px;
            text-align: right;
            padding-right: 10px;
          }

          .value {
            flex: 1;
            white-space: nowrap;
            color: #313238;
          }
        }
      }
    }
  }
}
</style>
