<template>
  <view class="my-page">
    <!-- 头部区域 -->
    <view class="header">
      <image src="/static/avatar.png" class="avatar"></image>
      <text class="username">{{ userInfo.name || '未登录' }}</text>
      <text class="email">{{ userInfo.email || '请登录' }}</text>
    </view>

    <!-- 功能卡片 -->
    <view class="card-container">
      <navigator url="/pages/history/index" class="card">
        <text class="icon">📄</text>
        <text class="title">咨询记录</text>
        <text class="desc">查看历史问答记录</text>
      </navigator>

      <navigator url="/pages/favorites/index" class="card">
        <text class="icon">⭐</text>
        <text class="title">收藏案例</text>
        <text class="desc">查看已收藏的判例</text>
      </navigator>

      <navigator url="/pages/settings/index" class="card">
        <text class="icon">⚙️</text>
        <text class="title">设置</text>
        <text class="desc">语言、通知等设置</text>
      </navigator>

      <navigator url="/pages/help/index" class="card">
        <text class="icon">❓</text>
        <text class="title">帮助中心</text>
        <text class="desc">常见问题与使用指南</text>
      </navigator>
    </view>

    <!-- 退出登录按钮 -->
    <button class="logout-btn" @click="logout">退出登录</button>

    <!-- 底部导航栏（可选） -->
    <navigation-bar></navigation-bar>
  </view>
</template>

<script>
export default {
  data() {
    return {
      userInfo: {
        name: '',
        email: ''
      }
    };
  },

  onLoad() {
    this.loadUserInfo();
  },

  methods: {
    loadUserInfo() {
      const user = uni.getStorageSync('userInfo');
      if (user) {
        this.userInfo = user;
      }
    },

    logout() {
      uni.removeStorageSync('userInfo');
      uni.showToast({
        title: '已退出',
        icon: 'success'
      });
      setTimeout(() => {
        uni.reLaunch({
          url: '/pages/login/index'
        });
      }, 1500);
    }
  }
};
</script>

<style scoped>
.my-page {
  background-color: #f8f9fa;
  padding: 20px;
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  background-color: #ccc;
  margin: 0 auto 16rpx;
}

.username {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.email {
  font-size: 24rpx;
  color: #666;
}

.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
}

.card {
  width: calc(50% - 10rpx);
  background: white;
  border-radius: 16rpx;
  padding: 30rpx;
  text-align: center;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.1);
  color: #333;
  text-decoration: none;
}

.card .icon {
  font-size: 48rpx;
  margin-bottom: 16rpx;
}

.card .title {
  font-size: 30rpx;
  font-weight: 500;
}

.card .desc {
  font-size: 24rpx;
  color: #999;
  margin-top: 8rpx;
}

.logout-btn {
  margin-top: 40rpx;
  width: 100%;
  background-color: #ff4d4f;
  color: white;
  border: none;
  border-radius: 16rpx;
  font-size: 30rpx;
  padding: 20rpx;
}
</style>