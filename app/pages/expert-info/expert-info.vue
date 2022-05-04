<template>
	<view class="container">
		<tui-navigation-bar backgroundColor="255,255,255" :isFixed="false" :isOpcity="false">
			<view class="tui-content-box">
				<view class="tui-avatar-box" @tap="back">
					<tui-icon name="back" color="#FFE933" :size="64"></tui-icon>
				</view>
				<view class="tui-search-box">
					<view class="tui-search-text">专家详情</view>
				</view>
				<view class="tui-notice-box" @tap="chat">
					<text class="tui-add-text">会话</text>
				</view>
			</view>
		</tui-navigation-bar>
		<view class="expert-info">
			<view class="expert-info-item">
				<view>{{ expertinfo.name}} </view>
				<image :src="expertinfo.img" mode="aspectFit"></image>
				<view>性别: {{expertinfo.sex}}</view>
				<view>职称: {{expertinfo.title}}</view>
				<view>研究领域: {{expertinfo.field}}</view>
			</view>
			<view class="expert-info-detail">
				<view>简介： </view>
				<view>{{ expertinfo.info}} </view>
			</view>
		</view>
		<view class="subBtnBox"  @tap="createOrder">
			<view class="subBtn">发起订单 </view>
		</view>
	</view>
</template>

<script>
	export default {
		onLoad(data) {
			this.expertinfo = data
			this.demandId = data.demandId
		},
		data() {
			return {
				demandId: '',
				expertinfo: {
					id: '',
					img: '',
					name: '',
					sex: '',
					title: '',
					field: '',
					info: ''
				}
			}
		},
		methods: {
			back() {
				uni.navigateBack()
			},
			chat() {
				uni.navigateTo({
					url: '../user-chat/user-chat?demandId=' + this.demandId + '&expertId=' + this.expertinfo.id 
				})
			},
			createOrder() {
				
			}
		}
	}
</script>

<style>
	.container {
		padding: 0upx 0 120upx 0;
		box-sizing: border-box;
		position: relative;
	}

	.header {
		padding: 80upx 90upx 60upx 90upx;
		box-sizing: border-box;
	}

	.tui-content-box {
		width: 100%;
		height: 88upx;
		padding: 0 30upx;
		box-sizing: border-box;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.tui-avatar-box {
		width: 60upx;
		height: 60upx;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.tui-search-box {
		height: 55upx;
		align-items: center;
		font-weight: 700;
		color: #000000;
	}

	.tui-notice-box {
		height: 95upx;
		position: relative;
		flex-shrink: 0;
		font-size: 44upx;
		color: #fff;
	}

	.tui-add-text {
		color: #000000;
		padding: 10upx 20upx;
		font-size: 24upx;
		box-sizing: border-box;
		font-weight: 600;
		border-radius: 40upx;
		background-color: #FFE933;
	}

	.expert-info {
		padding: 0 30upx;
	}

	.expert-info-item {
		padding: 20upx 0;
		border-bottom: 1upx solid #EEEEEE;
	}

	.expert-info-item>view {
		color: #AAAAAA;
		font-size: 16upx;
	}

	.expert-info-item>view:first-child {
		color: #333333;
		font-size: 32upx;
		font-weight: 700;
		padding: 15upx 0;
	}
	
	.expert-info-detail {
		padding: 20upx 0;
		border-bottom: 1upx solid #EEEEEE;
	}
	
	.expert-info-detail>view {
		color: #AAAAAA;
		font-size: 16upx;
	}
	
	.expert-info-detail>view:first-child {
		color: #333333;
		font-size: 20upx;
		padding: 15upx 0;
	}
	
	.subBtnBox{
	width:100%;
	position: fixed;
	bottom:0;
	}
	
	.subBtn{
	width: 80%;
	height: 72rpx;
	background: linear-gradient(90deg, #ffff00 0%, #f0f000 100%);
	border-radius: 44rpx;
	text-align: center;
	line-height:72rpx;
	font-size: 32rpx;
	font-weight: 600;
	color:#000000;
	margin:46rpx auto;
	}
</style>
