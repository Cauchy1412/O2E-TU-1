<template>
	<view>
		<view class="index-icontainer">
			<tui-navigation-bar backgroundColor="255,255,255" :isFixed="false" :isOpcity="false">
				<view class="tui-content-box">
					<view class="tui-avatar-box" v-on:click="goBack()">
						<tui-icon name="back" color="#FFE933" :size="64"></tui-icon>
					</view>
					<view class="tui-search-box">
						<view class="tui-search-text">订单管理</view>
					</view>
					<view class="tui-avatar-box" v-on:click="goBack()">
						<tui-icon name="back" color="#ffffff" :size="64"></tui-icon>
					</view>
				</view>
			</tui-navigation-bar>
		</view>

		<template v-if='sects.length'>
			<uni-section v-for='s in sects' :title='s.name' type="line">
				<uni-list>
					<uni-list-item
						v-for="o in s.items"
						:title='getTitle(o)'
						:note='formatDate(o.created_at)'
						:rightText='getStatus(o)'
						@click="goDetail(o.id)"
					></uni-list-item>
				</uni-list>
			</uni-section>
		</template>
		<view v-else>
			<no-thing></no-thing>
		</view>
	</view>
</template>

<script>
	import {mapState, mapMutations} from 'vuex'
	import {api} from '@/api'
	import noThing from "@/components/common/no-thing";

	export default {
		components: {
			noThing
		},
		data() {
			return {
				data: []
			}
		},
		onLoad() {
			this.getData();
		},
		computed:{
			...mapState(['userInfo']),
			sects() {
				const r = ['???', '待接受', '进行中', '已完成', '已拒绝'].map(s => ({
					name: s,
					items: [],
				}));
				for (const o of this.data) {
					const s = r[Number(o.state)];
					if (s)
						s.items.push(o);
				}
				return r.filter(s => s.items.length);
 			}
		},
		methods:{
			goBack:function() {
				uni.switchTab({
					url:'../home/home',
				})
			},
			goDetail:function(stringofid) {
				uni.navigateTo({
					url:'./OrderDetail?id='+stringofid
				})
			},
			async getData() {
				let result
				if (this.isEnterprise()) {
					result = await api.get('resolution/get-company-resolutions')
				}
				else {
					result = await api.get('resolution/get-scholar-resolutions')
				}
				this.data = result.resolution_list;
				return result
			},
			getTitle(o) {
				const name = this.isEnterprise() ? o.scholar_meta?.name : o.company_meta?.name;
				if (name)
					return o.title + ' - ' + name;
				return o.title;
			},
			getStatus(o) {
				const s = ['???', '待接受', '进行中', '已完成', '已拒绝'];
				return s[Number(o.state)];
			}
		}
	}
</script>

<style>
	page {
		background-color: #f8f8f8;
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
		border-radius: 10upx;
		background-color: #f1f1f1;
		padding: 0 24upx;
		box-sizing:border-box;
		color: #5C8DFF;
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
	.order-info-detail2 {
		color: #CD1225;
		font-size: 20upx;
		padding: 15upx 0;
	}
</style>
