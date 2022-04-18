<template>
	<view class="container">
		<tui-navigation-bar backgroundColor="255,255,255" :isFixed="false" :isOpcity="false">
			<view class="tui-content-box">
				<view class="tui-avatar-box" @tap="back">
					<tui-icon name="back" color="#FFE933" :size="64"></tui-icon>
				</view>
				<view class="tui-search-box">
					<view class="tui-search-text">需求详情</view>
				</view>
				<view class="tui-notice-box">
					<text class="tui-add-text"></text>
				</view>
			</view>
		</tui-navigation-bar>
		<view class="demand-info">
			<view class="demand-info-item">
				<view>需求题目：{{ demandinfo.title}} </view>
				<view>企业名称：{{ demandinfo.comName}} </view>
				<view>研发经费：{{ demandinfo.fund}} </view>
				<view>研发周期：{{ demandinfo.period}} </view>
				<view>研发地点：{{ demandinfo.place}} </view>
			</view>
			<view class="demand-info-item">
				<view>需求内容： </view>
				<view>{{ demandinfo.content}} </view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		// onLoad(data) {
		// 	this.demandinfo.title = data.title
		// 	this.demandinfo.comName = data.comName
		// 	this.demandinfo.fund = data.fund
		// 	this.demandinfo.period = data.period
		// 	this.demandinfo.place = data.place
		// 	this.demandinfo.content = data.content
		// },
		data() {
			return {
				demandinfo: {
					title: '自动驾驶开发',
					comName: '张三有限公司',
					fund: '200,000元',
					period: '1个月',
					place: '北京',
					content: '自动驾驶汽车（Autonomous vehicles；Self-driving automobile ）又称无人驾驶汽车、电脑驾驶汽车、或轮式移动机器人，是一种通过电脑系统实现无人驾驶的智能汽车。在20世纪已有数十年的历史，21世纪初呈现出接近实用化的趋势。'
				}
			}
		},
		methods: {
			back() {
				// uni.reLaunch({
				// 	url: '/'
				// });
				uni.navigateBack()
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
		display: flex;
		align-items: center;
		font-weight: 700;
		color: #000000;
	}

	.tui-notice-box {
		width: 60upx;
	}

	.demand-info {
		padding: 0 30upx;
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
</style>
