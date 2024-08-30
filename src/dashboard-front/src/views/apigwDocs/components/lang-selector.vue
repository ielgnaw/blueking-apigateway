<template>
  <div class="lang-selector-wrap bk-button-group">
    <bk-button
      v-for="lang in langList"
      :key="lang"
      :class="{ 'is-selected': lang === language }"
      :style="{
        width: `${width}px`,
        'margin-bottom': `${marginBottom}px`,
      }"
      @click="handleSelect(lang)"
    >
      {{ useChangeCase(lang, 'capitalCase') }}
    </bk-button>
  </div>
</template>

<script setup lang="ts">
import {
  ref,
  toRefs,
} from 'vue';
import { useChangeCase } from '@vueuse/integrations/useChangeCase';
import { LanguageType } from '@/views/apigwDocs/types';

const language = defineModel<LanguageType>({
  default: 'python',
});

interface IProps {
  width: number;
  marginBottom: number;
}

const props = withDefaults(defineProps<IProps>(), {
  width: 150,
  marginBottom: 24,
});

const { width } = toRefs(props);

const langList = ref<LanguageType[]>([
  'python',
  'java',
]);

const emit = defineEmits<{
  'select': [language: LanguageType]
}>();

const handleSelect = (lang: LanguageType) => {
  language.value = lang;
  emit('select', language.value);
};

</script>

<style scoped lang="scss">

</style>
