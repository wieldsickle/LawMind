<!-- /src/pages/law-webview/index.vue -->
<template>
  <view class="law-webview-container">
    <web-view :src="lawUrl"></web-view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      lawUrl: 'https://esign.qq.com' // 默认网址
    };
  },

  // ✅ 正确：使用 onLoad 接收参数
  onLoad(options) {
    // options 是页面跳转时传入的参数对象
    if (options.url) {
      try {
        this.lawUrl = decodeURIComponent(options.url);
      } catch (e) {
        console.error('URL 解码失败，使用默认地址', e);
      }
    }
  }
};
</script>

<style scoped>
.law-webview-container {
  width: 100%;
  height: 100vh;
}
</style>