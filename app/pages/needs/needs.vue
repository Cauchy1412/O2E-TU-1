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
				<view class="tui-notice-box" @tap="toExperts">
					<text class="tui-add-text">专家</text>
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
		//  this.id = data.id
		// 	this.demandinfo.title = data.title
		// 	this.demandinfo.comName = data.comName
		// 	this.demandinfo.fund = data.fund
		// 	this.demandinfo.period = data.period
		// 	this.demandinfo.place = data.place
		// 	this.demandinfo.content = data.content
		// },
		computed: {
			demandinfo() {
				const o = this.$store.state.demand_detail;
				console.log('detail title', o.title);
				const meta = o.meta || {};
				return {
					id: o.id,
					title: o.title,
					comName: '张三有限公司', // TODO
					fund: meta.fund || '',
					period: meta.period || '',
					place: meta.place || '',
					content: o.description,
				}
			}
		},
		methods: {
			back() {
				uni.navigateBack()
			},
			toExperts() {
				const id = this.demandinfo.id
				uni.navigateTo({
					url: '../experts/experts?id=' + id
				})
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
