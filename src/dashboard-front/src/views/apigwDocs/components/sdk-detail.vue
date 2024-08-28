<template>
  <div class="data-box wrapper">
    <div class="row-item mb10">
      <div class="key">
        <span class="column-key"> {{ t('SDK包名称') }}: </span>
      </div>
      <div class="value">
        <span class="column-value" v-bk-overflow-tips>{{params?.sdk?.name || '--'}}</span>
      </div>
    </div>
    <div class="row-item mb10">
      <div class="key">
        <span class="column-key"> {{ t('SDK版本') }}: </span>
      </div>
      <div class="value">
        <span class="column-value" v-bk-overflow-tips>{{params?.sdk?.version || '--'}}</span>
      </div>
    </div>

    <div class="row-item mb10">
      <div class="key">
        <span class="column-key"> {{ t('SDK地址') }}: </span>
      </div>
      <div class="value">
        <bk-popover placement="top" width="600" :disabled="!params.sdk?.url">
          <main class="column-value vm">{{params?.sdk?.url || '--'}}</main>
          <template #content>
            <div style="white-space: normal;word-break: break-all;">
              {{ params?.sdk?.url }}
            </div>
          </template>
        </bk-popover>
      </div>
      <aside class="suffix">
        <i
          class="doc-copy vm icon-hover apigateway-icon icon-ag-copy ag-doc-icon"
          v-if="params?.sdk?.url"
          v-bk-tooltips="t('复制')"
          @click="copy(params?.sdk?.url)"
        >
        </i>
        <i
          class="ag-doc-icon doc-download-line vm icon-hover apigateway-icon icon-ag-download-line"
          v-if="params?.sdk?.url"
          v-bk-tooltips="t('下载')"
          @click="handleDownload">
        </i>
      </aside>
    </div>

    <div class="row-item mb10">
      <div class="key">
        <span class="column-key"> {{ t('安装') }}: </span>
      </div>
      <div class="value">
        <bk-popover placement="top" width="600" v-if="params?.sdk?.install_command">
          <main class="column-value vm">{{params?.sdk?.install_command}}</main>
          <template #content>
            <div style="white-space: normal;word-break: break-all;">
              {{ params?.sdk?.install_command }}
            </div>
          </template>
        </bk-popover>
        <span v-else>--</span>
      </div>
      <aside class="suffix">
        <i
          class="ag-doc-icon doc-copy vm icon-hover apigateway-icon icon-ag-copy"
          v-if="params?.sdk?.install_command"
          v-bk-tooltips="t('复制')"
          @click="copy(params?.sdk?.install_command)"
        >
        </i>
      </aside>
    </div>

    <template v-if="isApigw">
      <div class="row-item mb10">
        <div class="key">
          <span class="column-key">
            {{ t('资源版本') }}
            <help-fill style="font-size: 16px; margin-left: 4px;" v-bk-tooltips="t('该SDK关联的API资源版本')" />
            :
          </span>
        </div>
        <div class="value">
          <span
            class="column-value"
            v-bk-tooltips.top="{ content: params?.resource_version?.version, allowHTML: false }">
            {{params?.resource_version?.version || '--'}}
          </span>
        </div>
      </div>

      <div class="row-item mb10" v-if="params?.stage?.name">
        <div class="key">
          <span class="column-key">
            {{ t('版本已发环境') }}:
          </span>
        </div>
        <div class="value">
          <span class="column-value" v-bk-tooltips.top="params.stage.name">{{params.stage.name || '--'}}</span>
        </div>
      </div>
    </template>
  </div>
</template>

<script lang="ts" setup>
// import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { copy } from '@/common/util';
import { HelpFill } from 'bkui-vue/lib/icon';

const { t } = useI18n();

const props = defineProps({
  isApigw: {
    type: Boolean,
    default: false,
  },
  params: {
    type: Object,
    default: () => {
      return {
        resource_version: {},
        sdk: {},
        stage: {},
      };
    },
  },
});

// const stageText = computed(() => {
//   let texts = [];
//   if (props.params?.released_stages) {
//     texts = props.params?.released_stages.map((item: any) => item.name);
//   }

//   return texts.join(', ');
// });

const handleDownload = () => {
  if (props.params?.sdk?.url) {
    window.open(props.params?.sdk?.url);
  }
};
</script>

<style lang="scss" scoped>
.data-box {
  padding: 12px 16px;
  background: #fafbfd;

  .row-item {
    display: flex;

    .key {
      flex-shrink: 0;
      width: 90px;
      padding-right: 10px;
      text-align: right;
    }

    .value {
      width: calc(100% - 140px);
    }

    .suffix {
      flex-shrink: 0;
      padding-left: 4px;
      width: 50px;
      display: flex;
      align-items: center;
    }
  }
}
.column-key {
  font-size: 14px;
  color: #63656E;
  line-height: 22px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.column-value {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.ag-doc-icon {
  font-size: 16px;
  color: #979BA5;
  cursor: pointer;
  margin-right: 5px;
}

.icon-hover:hover {
  color: #3a84ff;
}
</style>
