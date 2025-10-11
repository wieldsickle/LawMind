<template>
    <view class="container">
        <!-- 导航栏 -->
        <view class="navbar">
            <text class="navbar-brand">法律服务</text>   
        </view>
		<swiper class="swiper-container" :indicator-dots="true" indicator-color="#007aff" indicator-active-color="red"
		        :autoplay="true" :interval="3000" :duration="300" :circular="true" :vertical="false" next-margin="20rpx">
		    <swiper-item>
		        <view class="swiper-item-content">
		            <image class="img1" src="/static/zw1.png" mode="aspectFill"></image>
		        </view>
		    </swiper-item>
		    <swiper-item>
		        <view class="swiper-item-content">
		            <image class="img1" src="/static/zw2.png" mode="aspectFill"></image>
		        </view>
		    </swiper-item>
		</swiper>

        <!-- 主内容区域 -->
        <view class="main-content">
            <view class="hero-section">
                <text class="hero-title">智能法律服务触手可及</text>
                <text class="hero-subtitle">提供高效、便捷的法律咨询与查询工具</text>
            </view>

            <!-- 功能网格 -->
            <view class="features-grid">
                <view class="feature-card" @click="goToPage('/pages/aichat/aichat')">
                    <text class="icon">&#xe600;</text> <!-- 示例图标，实际请使用iconfont或图片 -->
                    <text class="card-title">智能法律问答</text>
                    <text class="card-desc">快速获取法律解答</text>
                </view>

                <view class="feature-card" @click="goToPage('/pages/cases/cases')">
                    <text class="icon">&#xe601;</text>
                    <text class="card-title">类案检索</text>
                    <text class="card-desc">查询相关判例与案例</text>
                </view>

                <view class="feature-card" @click="goToPage('/pages/law-webview/law-webview')">
                    <text class="icon">&#xe602;</text>
                    <text class="card-title">法条速查</text>
                    <text class="card-desc">精准查找法律法规</text>
                </view>

                <view class="feature-card" @click="goToPage('/pages/contract/contract')">
                    <text class="icon">&#xe603;</text>
                    <text class="card-title">合同审查</text>
                    <text class="card-desc">智能分析与审查合同</text>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    data() {
        return {
            // 这里可以放置组件数据
        };
    },
    methods: {
        goToPage(url) {
            uni.navigateTo({
                url: url
            });
        }
    },
    onLoad() {
        // 页面加载时的生命周期函数
        console.log('首页加载完成');
    }
};
</script>

<style>
/* 可以在这里引入或定义字体图标 */
/* 例如：@font-face { font-family: 'iconfont'; src: url('~@/static/iconfont.ttf') format('truetype'); } */

.container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background-color: #f4f7f6;
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    background-color: #ffffff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.navbar-brand {
    font-size: 24px;
    font-weight: bold;
    color: #333;
}

.nav-links {
    display: flex;
}

.nav-item {
    margin-left: 20px;
    color: #555;
    font-size: 16px;
    text-decoration: none;
}

.nav-item:hover {
    color: #007bff;
}
.swiper-container {
    width: 100%; /* 宽度设为100%，以占据其父元素的全部宽度 */
    height: 400rpx; /* 根据需要调整高度 */
}

/* 每个轮播项的内容容器 */
.swiper-item-content {
    display: flex;
    justify-content: center; /* 水平居中 */
    align-items: center; /* 垂直居中 */
    width: 100%;
    height: 100%;
}

.img1 {
    width: 750rpx; 
    height: 400rpx; 
    object-fit: cover; 
}

.main-content {
    flex: 1;
    padding: 30px 20px;
    text-align: center;
}

.hero-section {
    margin-bottom: 40px;
}

.hero-title {
    font-size: 32px;
    font-weight: bold;
    color: #333;
    margin-bottom: 10px;
    display: block; /* 确保标题独占一行 */
}

.hero-subtitle {
    font-size: 16px;
    color: #666;
    line-height: 1.6;
    display: block; /* 确保副标题独占一行 */
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); /* 适应不同屏幕尺寸 */
    gap: 20px;
    max-width: 900px;
    margin: 0 auto;
}

.feature-card {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    min-height: 150px; /* 确保卡片有最小高度 */
}

.feature-card:active { /* 移动端点击效果 */
    transform: translateY(-3px);
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
}

.icon {
    /* 如果使用iconfont，这里设置font-family和unicode */
    font-family: 'iconfont'; /* 假设你引入了iconfont */
    font-size: 36px;
    color: #007bff;
    margin-bottom: 15px;
}

/* 示例iconfont图标对应的unicode编码，请替换为你实际使用的图标 */
/* 例如：在 @font-face 中定义好之后，这里只需要通过 &#x图标代码; 来显示 */
/* 如果不使用iconfont，你可以用图片代替图标 */

.card-title {
    font-size: 18px;
    font-weight: bold;
    color: #333;
    margin-bottom: 8px;
    display: block;
}

.card-desc {
    font-size: 13px;
    color: #777;
    text-align: center;
    display: block;
}
</style>