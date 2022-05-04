<template>
	<view>
		<view class="container">
			<tui-navigation-bar backgroundColor="255,255,255" :isFixed="false" :isOpcity="false">
				<view class="tui-content-box">
					<view class="tui-avatar-box">
						<tui-icon name="back" color="#FFE933" :size="64"></tui-icon>
					</view>
					<view class="tui-search-box">
						<view class="tui-search-text">订单管理</view>
					</view>
					<view class="tui-notice-box">
						<text class="tui-add-text">管理</text>
					</view>
				</view>
			</tui-navigation-bar>
		</view>
		<view v-for="(item,index) in Data">
			<view class="demand-info-item">
				<view>
					订单要求:{{item.title}}
				</view>
				<view>
					发布日期:{{item.created_at}}
				</view>
				<view>
					订单状态:{{calculateState(item.state)}}
				</view>
			</view>
			<view class="order-info-detail" v-on:click="goDetail(item.id)">
				详情
			</view>
		</view>
	</view>
</template>

<script>
	import {mapState, mapMutations} from 'vuex'
	import {api} from '@/api'
	export default {
		data() {
			return {
				Data : []
			}
		},
		onLoad:function() {
			this.Data = this.getData()
		},
		computed:{
			...mapState(['userInfo']),
			calculateState: function(stringofstate) {
				if (stringofstate == '1')
					return '待接受'
				else
					if (stringofstate == '2')
						return '进行中'
					else
						if (stringofstate == '3')
							return '已完成'
						else
							return '已被拒绝'
			}
		},
		methods:{
			goDetail:function(stringofid) {
				uni.navigateTo({
					url:'./OrderDetail?id='+stringofid
				})
			},
			async getData() {
				let result
				if (this.userInfo.user_type) {
					result = await api.get('resolution/get-company-resolutions')
				}
				else {
					result = await api.get('resolution/get-scholar-resolutions')
				}
				return result
			},
		}
	}
</script>

<style>
	page {
		background-color: #fff;

	}

	.container {
		padding: 0upx 0 120upx 0;
		box-sizing: border-box;
		position: relative;
	}
	
	.header {
		padding: 80upx 90upx 60upx 90upx;
		box-sizing: border-box;
	}
	
	.title {
		font-size: 34upx;
		color: #333;
		font-weight: 500;
	}
	
	.sub-title {
		font-size: 24upx;
		color: #7a7a7a;
		padding-top: 18upx;
	}
	
	.tui-box-upload {
		padding-left: 25upx;
		margin-bottom: 90upx;
		box-sizing: border-box;
	}
	
	.tui-title {
		width: 100%;
		padding: 50upx 30upx 30upx;
		box-sizing: border-box;
		font-weight: bold;
	}
	
	.tui-header-bg {
		width: 100%;
		margin: 0;
	}
	
	.tui-header-img {
		width: 100%;
		height: 440upx;
		display: block;
	}
	
	.tui-header-icon {
		width: 100%;
		position: fixed;
		top: 0;
		padding: 0 12upx;
		display: flex;
		align-items: center;
		height: 64upx;
		transform: translateZ(0);
		z-index: 99999;
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
		flex-shrink: 0;
	}
	
	.tui-avatar {
		width: 56upx;
		height: 56upx;
		border-radius: 50%;
	}
	
	.tui-search-box {
		height: 64upx;
		margin: 0 28upx;
		border-radius: 36upx;
		font-size: 36upx;
		padding: 0 24upx;
		box-sizing: border-box;
		color: #bfbfbf;
		display: flex;
		align-items: center;
		font-weight: 700;
		color: #000000;
	}
	
	.select-topic-class {
		height: 72upx;
		margin: 20upx 20upx;
		border-radius: 10upx;
		background-color: #f1f1f1;
		padding: 0 24upx;
		box-sizing:border-box;
		color: #bfbfbf;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
	
	.select-title {
		color: #000000;
		font-size: 34upx;
		font-weight: 700;
	}
	.select-desc {
		display: flex;
		align-items: center;
	}
	.add-topic-text{
		box-sizing: border-box;
		width: 100%;
		padding-top: 10upx;
		padding-left: 45upx;
	}
	.tui-bg-white {
		background-color: #ffffff !important;
	}
	
	.tui-search-text {
		padding-left: 10upx;
	}
	
	.tui-add-text {
		color: #000000;
		padding: 10upx 30upx;
		font-size: 28upx;
		box-sizing: border-box;
		font-weight: 700;
		border-radius: 40upx;
		background-color: #FFE933;
	}
	.topic-tilte{
		padding: 10upx 40upx;
		box-sizing: border-box;
		font-weight: 700;
		color:#5677fc;
	}
	.tui-notice-box {
		position: relative;
		flex-shrink: 0;
		font-size: 44upx;
		color: #fff;
	}
	
		.example {
			padding: 15px;
			background-color: #fff;
		}
	
		.segmented-control {
			margin-bottom: 15px;
		}
	
		.button-group {
			margin-top: 15px;
			display: flex;
			justify-content: space-around;
		}
	
		.form-item {
			display: flex;
			align-items: center;
		}
	
		.button {
			display: flex;
			align-items: center;
			height: 35px;
			margin-left: 10px;
		}
	.demand-info-item {
		padding: 20upx 0;
		border-bottom: 1upx solid #EEEEEE;
	}

	.demand-info-item>view {
		color: #AAAAAA;
		font-size: 16upx;
	}

	.demand-info-item>view:first-child {
		color: #333333;
		font-size: 20upx;
		padding: 15upx 0;
	}
	.order-info-detail {
		color: #0A98D5;
		font-size: 20upx;
		padding: 15upx 0;
	}
</style>
