<template>
  <bk-sideslider
    v-model:isShow="isShow"
    quick-close
    :title="resource.name"
    width="780"
    ext-cls="doc-sideslider-cls doc-sides"
  >
    <template #default>
      <ResourcesDoc
        :cur-resource="resource"
        source="side"
        doc-root-class="doc-sideslider"
        :show-footer="false"
        :show-create-btn="false"
        :is-preview="!resource.doc || resource.doc.length < 1"
      >
      </ResourcesDoc>
    </template>
  </bk-sideslider>
</template>
<script setup lang="ts">
import { defineModel, toRefs } from 'vue';
import ResourcesDoc from '@/views/components/resources-doc/index.vue';

const props = defineProps({
  resource: { type: Object, default: () => ({}) },
});

const isShow = defineModel<boolean>({
  required: true,
  default: false,
});

const { resource } = toRefs(props);

</script>
<style scoped lang="scss">

:deep(.bk-modal-content) {
  max-height: calc(100vh - 52px);
  overflow: hidden;
  background-color: #f5f7fa;
}

:deep(.bk-modal-body),
:deep(.bk-sideslider-footer) {
  background-color: #f5f7fa;
}
</style>
