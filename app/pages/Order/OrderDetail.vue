<template>
	<view class='index-icontainer'>
		<view class="">
			<tui-navigation-bar backgroundColor="255,255,255" :isFixed="false" :isOpcity="false">
				<view class="tui-content-box">
					<view class="tui-avatar-box" v-on:click="goBack()">
						<tui-icon name="back" color="#FFE933" :size="64"></tui-icon>
					</view>
					<view class="tui-search-box">
						<view class="tui-search-text">订单详情</view>
					</view>
					<view class="tui-avatar-box" @tap="goBack">
						<tui-icon name="back" color="#ffffff" :size="64"></tui-icon>
					</view>
				</view>
			</tui-navigation-bar>
		</view>
		<uni-section title="订单标题":note="d.title" type="line">
			<uni-list>
				<uni-list-item title="发布公司":note="ent.name"></uni-list-item>
				<uni-list-item title="需求经费":note="d.price + ' 万元'"></uni-list-item>
				<uni-list-item title="需求周期":note="d.time"></uni-list-item>
				<uni-list-item title="发起时间":note="formatDate(d.created_at)" ></uni-list-item>
				<uni-list-item v-if="!userInfo.user_type" title="联系企业" clickable @click="goToChat(d.company_id)"></uni-list-item>
			</uni-list>
		</uni-section>
		<uni-section title="专家信息":note="sch.name" type="line">
			<uni-list>
				<uni-list-item title="性别":note="sch.gender" ></uni-list-item>
				<uni-list-item title="职位":note="sch.professor" ></uni-list-item>
				<uni-list-item title="擅长领域":note="getDomain(sch.domains)" ></uni-list-item>
				<uni-list-item v-if="userInfo.user_type" title="联系专家" clickable @click="goToChat(d.scholar_id)"></uni-list-item>
			</uni-list>
		</uni-section>
		<view v-if="!userInfo.user_type">
			<button class="buttonx" type="primary" v-on:click="Accept()">
				接受
			</button>
			<button class="buttonx" type="warn" v-on:click="Refuse()">
				拒绝
			</button>
		</view>
		<view v-else="userInfo.user_type">
			<view v-if="AnalyzeState()">
				<button class="buttonx" type="warn" v-on:click="Complete()">
					完成订单
				</button>
			</view>
			<view v-else="AnalyzeState()">
				<button class="buttonx" type="warn" v-on:click="Cancel()">
					取消订单
				</button>
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
				order_id: null,
				d: {}
			}
		},
		onLoad: function(option){
			this.order_id = option.id;
			this.getData(option.id)
		},
		computed: {
			...mapState(['userInfo']),
			sch() {
				return this.d.scholar_meta || {};
			},
			ent() {
				return this.d.company_meta || {};
			}
		},
		methods: {
			async goToChat(eid) {
				const uid = this.userInfo.id;
				const demand_id = this.demandId;
				const res = await api.post('chat/create', {
					chatroom_name: "聊天",
					from_user_id: uid,
					to_user_id: eid,
					demand_id: this.d.demand_id
				});
				uni.navigateTo({
					url: '../user-chat/user-chat?cid=' + res.id + '&fid=' + eid
				});
			},
			goBack() {
				uni.navigateBack()
			},
			getDomain(x) {
				if (x)
					return typeof(x) === 'string' ? x : (x.join('，'))
				return '';
			},
			AnalyzeState() {
				return this.d.state != 1
			},
			async getData(stringofid) {
				const result = await api.get('resolution/'+stringofid)
				// console.log('got res ' + JSON.stringify(result));
				this.d = result;
				return result
			},
			async Complete() {
				//if (this.state==1) {
					const change_state=3
					const resp = await api.post('resolution/update-resolution-state', {
						id:this.order_id,state:change_state
					});
					if (resp.msg) {
						uni.navigateBack({
							complete() {
								setTimeout(() => {
									uni.showToast({
										title: '订单完成',
										icon: "success",
										duration: 1000
									});
								}, 100);
							}
						});
					}
					this.toast('完成失败');
				//}
			},
			async Cancel() {
				//if (this.state==1) {
					const change_state=0
					const resp = await api.post('resolution/update-resolution-state', {
						id:this.order_id,state:change_state
					});
					if (resp.msg) {
						uni.navigateBack({
							complete() {
								setTimeout(() => {
									uni.showToast({
										title: '订单取消',
										icon: "success",
										duration: 1000
									});
								}, 100);
							}
						});
					}
					this.toast('取消失败');
				//}
			},
			async Accept (){
				//if (this.state==1) {
					const change_state=2
					const resp = await api.post('resolution/update-resolution-state', {
						id:this.order_id,state:change_state
					});
					if (resp.msg) {
						uni.navigateBack({
							complete() {
								setTimeout(() => {
									uni.showToast({
										title: '接受成功',
										icon: "success",
										duration: 1000
									});
								}, 100);
							}
						});
					}
					this.toast('接受失败');
				//}
			},
			async Refuse(){
				//if (this.state==1) {
					const change_state=4
					const resp = await api.post('resolution/update-resolution-state', {
						id:this.order_id,state:change_state
					});
					if (resp.msg) {
						uni.navigateBack({
							complete() {
								setTimeout(() => {
									uni.showToast({
										title: '拒绝成功',
										icon: "success",
										duration: 1000
									});
								}, 100);
							}
						});
					}
					this.toast('拒绝失败');
				//}
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
	.order-info-detail-receive {
		color:#0062CC;
		font-size: 40upx;
		margin-top:40rpx;
		margin-left: 20rpx;
	}
	.order-info-detail-refuse {
		color: #CD1225;
		font-size: 40upx;
		margin-top: 40rpx;
		margin-left: 20rpx;
		}
	.order-info-detail-Complete {
		color: #01B90B;
		font-size: 40upx;
		margin-top: 25rpx;
		margin-left: 20rpx;
		}
	.buttonx {
		margin-bottom: 25rpx;
		margin-left: 20rpx;
		margin-right: 20rpx;
		}
</style>
