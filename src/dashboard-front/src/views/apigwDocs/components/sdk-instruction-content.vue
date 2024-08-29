<template>
  <!--  SDK使用说明 Slider 的内容  -->
  <div class="sdk-wrapper">
    <div class="bk-button-group ">
      <bk-button :class="{ 'is-selected': language === 'python' }" @click="changeLanguage('python')">Python</bk-button>
      <bk-button :class="{ 'is-selected': language === 'java' }" @click="changeLanguage('java')">Java</bk-button>
    </div>
    <!-- eslint-disable-next-line vue/no-v-html -->
    <div class="ag-markdown-view" id="markdown" :key="renderHtmlIndex" v-html="markdownHtml"></div>
  </div>
</template>

<script setup lang="ts">
import {
  ref,
  watch,
  nextTick,
  inject,
  Ref,
} from 'vue';
import MarkdownIt from 'markdown-it';
import hljs from 'highlight.js';
import 'highlight.js/styles/monokai-sublime.css';

import { copy } from '@/common/util';

import {
  getGatewaySDKlist,
  getESBSDKlist,
  getGatewaySDKDoc,
  getESBSDKDoc,
} from '@/http';
import {
  LanguageType,
  TabType,
} from '@/views/apigwDocs/types';

const curTab = inject<Ref<TabType>>('curTab');

const language = ref<LanguageType>('python');
const board = ref<string>('-');
const sdkDoc = ref<string>('');
const markdownHtml = ref<string>('');
const active = ref<string>('sdk');
const renderKey = ref<number>(0);
const renderHtmlIndex = ref<number>(0);
const keyword = ref<string>('');
const isLoading = ref<boolean>(false);
const pagination = ref({
  offset: 0,
  count: 0,
  limit: 10,
});
const curPageData = ref([]);


// 监听搜索关键词的变化
watch(
  () => keyword.value,
  (v: string) => {
    getSDKlist(v);
  },
);

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

const initMarkdownHtml = (content: string) => {
  markdownHtml.value = md.render(content);
  // eslint-disable-next-line no-plusplus
  renderHtmlIndex.value++;
  nextTick(() => {
    const markdownDom = document.getElementById('markdown');

    // 复制代码
    markdownDom.querySelectorAll('a')
      .forEach((item: any) => {
        item.target = '_blank';
      });
    markdownDom?.querySelectorAll('pre')
      ?.forEach((item) => {
        const parentDiv = document.createElement('div');
        const btn = document.createElement('button');
        const codeBox = document.createElement('div');
        const code = item?.querySelector('code')?.innerText;
        parentDiv.className = 'pre-wrapper';
        btn.className = 'ag-copy-btn';
        codeBox.className = 'code-box';
        btn.innerHTML = '<span title="复制"><i class="apigateway-icon icon-ag-copy-info"></i></span>';
        btn.setAttribute('data-copy', code);
        parentDiv?.appendChild(btn);
        codeBox?.appendChild(item?.querySelector('code'));
        item?.appendChild(codeBox);
        item?.parentNode?.replaceChild(parentDiv, item);
        parentDiv?.appendChild(item);
      });
    setTimeout(() => {
      const copyDoms = Array.from(document.getElementsByClassName('ag-copy-btn'));
      const handleCopy = function (this: any) {
        copy(this.dataset?.copy);
      };
      copyDoms.forEach((dom: any) => {
        dom.onclick = handleCopy;
      });
    }, 1000);
  });
};

// 获取SDK list
const getSDKlist = async (keyword: any | string = null) => {
  const pageParams = {
    limit: pagination.value.limit,
    offset: pagination.value.offset,
    language: language.value,
    keyword,
  };
  isLoading.value = true;
  try {
    if (curTab.value === 'apigw') {
      const res = await getGatewaySDKlist(pageParams);
      curPageData.value = res.results;
      pagination.value.count = res.count;
    } else {
      const res = await getESBSDKlist(board.value, pageParams);
      curPageData.value = res;
      pagination.value.count = res.length;
    }
    isLoading.value = false;
  } catch {
    isLoading.value = false;
  }
};

// 获取SDK 说明
const getSDKDoc = async () => {
  const params = { language: language.value };
  isLoading.value = true;
  try {
    if (curTab.value === 'apigw') {
      const res = await getGatewaySDKDoc(params);
      sdkDoc.value = res.content;
    } else {
      const res = await getESBSDKDoc(board.value, params);
      sdkDoc.value = res.content;
    }
    isLoading.value = false;
    initMarkdownHtml(sdkDoc.value);
  } catch {
    isLoading.value = false;
  }
};

const changeLanguage = (lang: LanguageType) => {
  if (lang === language.value) return;
  language.value = lang;
  init();
};

const init = () => {
  try {
    getSDKlist();
    getSDKDoc();
  } catch {
    sdkDoc.value = '';
    markdownHtml.value = '';
    curPageData.value = [];
    pagination.value = {
      offset: 0,
      count: 0,
      limit: 10,
    };
  }
};

// 监听type的变化
watch(
  () => curTab.value,
  () => {
    active.value = 'sdk';
    curPageData.value = [];
    // eslint-disable-next-line no-plusplus
    renderKey.value++;
    init();
  },
  { immediate: true, deep: true },
);

</script>

<style lang="scss" scoped>
$primary-color: #3a84ff;
$code-bc: #f5f7fa;
$code-color: #63656e;

.sdk-wrapper {
  padding: 24px 40px;
}

:deep(.bk-button-group) {
  .is-selected {
    background-color: #f6f9ff !important;
  }
}

:deep(.ag-markdown-view) {
  font-size: 14px;
  text-align: left;
  color: $code-color;
  line-height: 19px;
  font-style: normal;

  .pre-wrapper {
    .ag-copy-btn {
      right: 12px;
      top: 12px;
      background-color: $code-bc;
      color: $primary-color;
    }
  }

  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    padding: 0;
    margin: 25px 0 10px 0 !important;
    font-weight: bold;
    text-align: left;
    color: #313238;
    line-height: 21px;
  }

  h1 {
    font-size: 18px;
  }

  h2 {
    font-size: 17px;
  }

  h3 {
    font-size: 16px;
  }

  h4 {
    font-size: 13px;
  }

  h5 {
    font-size: 12px;
  }

  h6 {
    font-size: 12px;
  }

  p {
    font-size: 14px;
    color: $code-color;
    line-height: 22px;
    white-space: normal;
    word-break: break-all;
  }

  ul {
    padding-left: 17px;
    line-height: 22px;

    li {
      list-style: disc;
      margin-bottom: 8px;

      &:last-child {
        margin-bottom: 0;
      }
    }
  }

  ol {
    padding-left: 15px;
    line-height: 22px;
    margin: 14px 0;

    li {
      list-style: decimal;
      margin-bottom: 8px;

      &:last-child {
        margin-bottom: 0;
      }
    }
  }

  a {
    color: #3a84ff;
  }

  tt {
    margin: 0 2px;
    padding: 0 5px;
    white-space: nowrap;
    border: 1px solid #eaeaea;
    background-color: #f8f8f8;
    border-radius: 3px;
    font-size: 75%;
  }

  table {
    font-size: 14px;
    color: $code-color;
    width: 100%;
    text-align: left;
    margin: 10px 0;
    font-style: normal;
    border: 1px solid #dcdee5;

    &.field-list {
      th {
        width: 12%;
      }
    }

    em {
      font-style: normal;
    }

    th {
      background: #f0f1f5;
      font-size: 13px;
      font-weight: bold;
      color: $code-color;
      border-bottom: 1px solid #dcdee5;
      padding: 10px;
      min-width: 70px;

    }

    th:nth-child(1) {
      width: 20%;
    }

    td {
      padding: 10px;
      font-size: 13px;
      color: $code-color;
      border-bottom: 1px solid #dcdee5;
      max-width: 250px;
      font-style: normal;
      word-break: break-all;
    }
  }

  pre {
    border-radius: 2px;
    background: $code-bc;
    padding: 10px;
    font-size: 14px;
    text-align: left;
    color: $code-color;
    line-height: 24px;
    position: relative;
    overflow: auto;
    margin: 14px 0;

    code {
      font-family: "Lucida Console", "Courier New", "Monaco", monospace;
      color: $code-color;
    }

    .hljs {
      margin: -10px;
    }
  }
}

:deep(.code-box) {
  // 代码块高亮字体颜色
  .hljs-string {
    color: #ff9c01;
  }

  .hljs-keyword {
    color: #ea3636;
  }

  .hljs-comment {
    color: #c4c6cc;
  }
}
</style>
