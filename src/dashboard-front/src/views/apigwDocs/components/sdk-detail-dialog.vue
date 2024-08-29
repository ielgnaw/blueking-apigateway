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
        <div class="bk-button-group mb24">
          <bk-button class="is-selected" style="width: 150px">Python</bk-button>
          <bk-button style="width: 150px">Java</bk-button>
          <!-- <bk-button disabled style="width: 150px">GO</bk-button> -->
        </div>
        <div class="data-box">
          <article class="row-item">
            <aside class="key">
              <span class="column-key"> {{ t('SDK包名称') }}: </span>
            </aside>
            <main class="value">
              <span class="column-value" v-bk-overflow-tips>{{ curParams.sdk_name || '--' }}</span>
            </main>
          </article>
          <article class="row-item">
            <aside class="key">
              <span class="column-key"> {{ t('SDK版本') }}: </span>
            </aside>
            <main class="value">
              <span class="column-value" v-bk-overflow-tips>{{ curParams.sdk_version_number || '--' }}</span>
            </main>
          </article>
          <article class="row-item">
            <aside class="key">
              <span class="column-key"> {{ t('SDK地址') }}: </span>
            </aside>
            <main class="value flex-row align-items-center">
              <bk-popover placement="top" width="600" theme="dark" :disabled="curParams.sdk_download_url === ''">
                <span class="column-value vm">{{ curParams.sdk_download_url || '--' }}</span>
                <template #content>
                  <div class="popover-text">
                    {{ curParams.sdk_download_url }}
                  </div>
                </template>
              </bk-popover>
              <i
                @click="copy(curParams.sdk_download_url)"
                class="doc-copy vm icon-hover apigateway-icon icon-ag-copy ag-doc-icon"
                v-if="curParams.sdk_download_url" v-bk-tooltips="t('复制')"
                :data-clipboard-text="curParams.sdk_download_url"
              ></i>
              <i
                class="ag-doc-icon doc-download-line vm icon-hover apigateway-icon icon-ag-download-line"
                v-if="curParams.sdk_download_url" v-bk-tooltips="t('下载')" @click="handleDownload"
              ></i>
            </main>
          </article>
          <article class="row-item">
            <aside class="key">
              <span class="column-key"> {{ t('安装') }}: </span>
            </aside>
            <main class="value flex-row align-items-center">
              <bk-popover placement="top" width="600" theme="dark" :disabled="curParams.sdk_install_command === ''">
                <span class="column-value vm">{{ curParams.sdk_install_command || '--' }}</span>
                <template #content>
                  <div class="popover-text">
                    {{ curParams.sdk_install_command }}
                  </div>
                </template>
              </bk-popover>
              <i
                @click="copy(curParams.sdk_install_command)"
                class="ag-doc-icon doc-copy vm icon-hover apigateway-icon icon-ag-copy"
                v-if="curParams.sdk_install_command" v-bk-tooltips="t('复制')"
                :data-clipboard-text="curParams.sdk_install_command"
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
                v-bk-tooltips.top="{ content: curParams.resource_version_display, allowHTML: false }"
              >
                {{ curParams.resource_version_display || '--' }}
              </span>
            </main>
          </article>
          <article class="row-item" v-if="stageText">
            <aside class="key">
              <span class="column-key">
                {{ t('版本已发环境') }}:
              </span>
            </aside>
            <main class="value">
              <span class="column-value" v-bk-tooltips.top="stageText">{{ stageText || '--' }}</span>
            </main>
          </article>
        </div>
      </div>
    </main>
  </bk-dialog>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { computed, defineModel, ref } from 'vue';
import { copy } from '@/common/util';

const { t } = useI18n();

const isShow = defineModel<boolean>({
  required: true,
  default: false,
});

const curParams = ref({
  sdk_name: '',
  sdk_version_number: '',
  sdk_download_url: '',
  sdk_install_command: '',
  resource_version_display: '',
  released_stages: [],
});

const type = ref<string | any>('');

// 获取所有stage的name
const stageText = computed(() => {
  const text = curParams.value.released_stages.map((item: any) => item.name);
  return text.join('，');
});

// 下载
const handleDownload = () => {
  if (curParams.value.sdk_download_url) {
    window.open(curParams.value.sdk_download_url);
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
