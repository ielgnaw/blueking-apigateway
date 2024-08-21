<template>
  <!--  查看 SDK 弹窗  -->
  <bk-dialog
    v-model:is-show="isShow"
    title="网关API SDK:"
    class="custom-main-dialog"
    width="640"
    mask-close
  >
    <div class="dialog-content">
      <div class="dialog-main">
        <div class="bk-button-group mb15">
          <bk-button class="is-selected">Python</bk-button>
          <!-- <bk-button disabled>GO</bk-button> -->
        </div>
        <div class="data-box wrapper">
          <div class="row-item mb10">
            <div class="key">
              <span class="column-key"> {{ t('SDK包名称') }}: </span>
            </div>
            <div class="value">
              <span class="column-value" v-bk-overflow-tips>{{ curParams.sdk_name || '--' }}</span>
            </div>
          </div>
          <div class="row-item mb10">
            <div class="key">
              <span class="column-key"> {{ t('SDK版本') }}: </span>
            </div>
            <div class="value">
              <span class="column-value" v-bk-overflow-tips>{{ curParams.sdk_version_number || '--' }}</span>
            </div>
          </div>

          <div class="row-item mb10">
            <div class="key">
              <span class="column-key"> {{ t('SDK地址') }}: </span>
            </div>
            <div class="value flex-row align-items-center">
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
                :data-clipboard-text="curParams.sdk_download_url"></i>
              <i
                class="ag-doc-icon doc-download-line vm icon-hover apigateway-icon icon-ag-download-line"
                v-if="curParams.sdk_download_url" v-bk-tooltips="t('下载')" @click="handleDownload"></i>
            </div>
          </div>

          <div class="row-item mb10">
            <div class="key">
              <span class="column-key"> {{ t('安装') }}: </span>
            </div>
            <div class="value  flex-row align-items-center">
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
                :data-clipboard-text="curParams.sdk_install_command">
              </i>
            </div>
          </div>

          <template v-if="type === 'apigateway'">
            <div class="row-item mb10">
              <div class="key">
                <span class="column-key">
                  {{ t('资源版本') }}
                  <span v-bk-tooltips="t('该SDK关联的API资源版本')">
                    <i class="icon apigateway-icon icon-ag-help"></i>
                  </span>
                  :
                </span>
              </div>
              <div class="value">
                <span
                  class="column-value"
                  v-bk-tooltips.top="{ content: curParams.resource_version_display, allowHTML: false }">
                  {{ curParams.resource_version_display || '--' }}
                </span>
              </div>
            </div>

            <div class="row-item mb10" v-if="stageText">
              <div class="key">
                <span class="column-key">
                  {{ t('版本已发环境') }}:
                </span>
              </div>
              <div class="value">
                <span class="column-value" v-bk-tooltips.top="stageText">{{ stageText || '--' }}</span>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>
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
  :deep(.bk-modal-footer) {
    display: none;
  }

  .dialog-content {

    .dialog-main {
      .import-tips {
        background: #F5F6FA;
        border-radius: 2px;
        margin-bottom: 25px;
        padding: 12px 16px;
        color: #63656E;

        span {
          font-weight: 700;
        }
      }
    }
  }
}

.wrapper {
  margin-top: 10px;
  padding: 10px 5px;
  background: #fafbfd;
}

.data-box {
  .row-item {
    display: flex;

    .key {
      width: 120px;
      text-align: right;
      padding-right: 10px;
    }

    .value {
      flex: 1;
      white-space: nowrap;
    }
  }
}
</style>
