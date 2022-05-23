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
				<image :src="expertinfo.img" mode="aspectFit" v-if='expertinfo.img'></image>
				<view>性别: {{expertinfo.sex || expertinfo.gender}}</view>
				<view>职称: {{expertinfo.title || expertinfo.professor}}</view>
				<view>研究领域: {{domain}}</view>
			</view>
		</view>
		<swiper-tab-head :tabBars="tabBars" :tabIndex="tabIndex" @tabtap="tabtap">
		</swiper-tab-head>
		<view class="uni-tab-bar">
			<swiper class="swiper-box" :style="{height:swiperheight+'px'}" :current="tabIndex">
				<swiper-item v-for="(items,index) in newslist" :key="index">
					<scroll-view scroll-y class="list" refresher-enabled :refresher-triggered="refreshing"
						refresher-background="#fafafa" enable-back-to-top :refresher-threshold="100"
						@refresherrefresh="onrefresh">
						<template v-if="tabIndex == 0">
							<view class="expert-info" v-if="expertinfo.info">
								<view class="expert-info-detail">
									<view>{{ expertinfo.info}} </view>
								</view>
							</view>
							<view v-else>
								<no-thing></no-thing>
							</view>
							<view class="subBtnBox" @tap="createOrder">
								<view class="subBtn">发起订单 </view>
							</view>
						</template>
						<template v-if="tabIndex == 1">
							<view>
								<view class="uni-comment u-comment">
									<block v-for="(item,index1) in commentlist" :key="index1">
										<view class="uni-comment-list">
											<view class="uni-comment-face" v-if='item.userpic == ""'>
												<image :src="item.userpic" mode="widthFix"></image>
											</view>
											<view class="uni-comment-face" v-else>
												<image :src="src" mode="widthFix"></image>
											</view>
											<view class="uni-comment-body">
												<view class="uni-comment-top">
													<text>{{item.username}}</text>
												</view>
												<view class="uni-comment-content">
													<text style="word-break:break-all;">{{item.text}}</text>
												</view>
												<view class="uni-comment-date">
													<view>{{item.time}}</view>
												</view>
											</view>
										</view>
									</block>
									<template v-if="commentlist.length==0">
										<view>还没有评论,快来说两句~</view>
									</template>
								</view>
								<view class="example" @click="inputDialogToggle">
									<uni-forms>
										<uni-forms-item>
											<uni-easyinput placeholder='发一条友善的评论' />
										</uni-forms-item>
									</uni-forms>
								</view>
							</view>
						</template>
					</scroll-view>
				</swiper-item>
			</swiper>
		</view>
		<view>
			<uni-popup ref="inputDialog" type="dialog">
				<uni-popup-dialog ref="inputClose" mode="input" title="发布评论"  placeholder="请输入您的评论"
					@confirm="dialogInputConfirm"></uni-popup-dialog>
			</uni-popup>
		</view>
	</view>
</template>

<script>
	import {
		api
	} from '@/api';
	import swiperTabHead from "../../components/index/swiper-tab-head.vue";
	import noThing from "../../components/common/no-thing.vue";
	import {
		mapState
	} from "vuex";
	export default {
		components: {
			swiperTabHead,
			noThing,
		},
		onLoad(data) {
			this.resolusionId = data.rid
			this.demandId = data.demandId
		},
		mounted() {
			this.requestData()
		},
		data() {
			return {
				nvueWidth: 730,
				value: '',
				src: '../../static/images/avatar/Default_Avatar.jpg',
				demandId: '',
				resolusionId: 111,
				input: '',
				tabIndex: 0,
				size: 400,
				isize: 48,
				swiperheight: 500,
				refreshing: false,
				tabBars: [{
						name: "简介",
						id: "info",
						page: 1
					},
					{
						name: "评论",
						id: "comment",
						page: 2
					},
				],
				commentlist: [],
				newslist: [{
						loadtext: "没有更多数据了",
						id: "Info",
						list: []
					},
					{
						loadtext: "没有更多数据了",
						id: "commentlist",
						list: []
					},
				],
			}
		},
		computed: {
			expertinfo() {
				return this.$store.state.expert_detail;
			},
			domain() {
				if (this.expertinfo.field)
					return this.expertinfo.field;
				if (this.expertinfo.domains)
					return this.expertinfo.domains.join('，');
				return '';
			},
			...mapState(['userInfo']),
		},
		methods: {
			async requestData() {
				const res = await api.post('evaluation/scholar', {
					id: this.expertinfo.id
				});
				this.commentlist = res.evaluation_list.map(o => ({
					time: o.created_at,
					text: o.description,
					userpic: o.icon,
					username: o.company_meta.name
				}));
				for (let item of this.commentlist) {
					const l = item.time.split("T");
					item.time = l[0];
				}
			},
			inputDialogToggle() {
				this.$refs.inputDialog.open()
			},
			async onrefresh() {
				if (this.refreshing) return;
				this.refreshing = true;
				await this.requestData()
				setTimeout(() => {
					this.refreshing = false;
					uni.showToast({
						title: '已更新',
						duration: 500
					})
				}, 200)
			},
			back() {
				uni.navigateBack()
			},
			tabtap(index) {
				this.tabIndex = index;
			},
			async dialogInputConfirm(val) {
				const id = this.expertinfo.id;
				const resp = await api.post('evaluation/create', {
					description: val,
					id
				});
				if (!resp) {
					setTimeout(() => {
						uni.showToast({
							title: '发布成功',
							icon: "success",
							duration: 1000
						});
						this.$refs.inputDialog.close()
					}, 100)
					this.requestData();
				}
				else {
					this.toast('发布失败');
				}				
			},
			async chat() {
				const uid = this.$store.state.userInfo.id;
				const eid = this.expertinfo.id;
				const demand_id = this.demandId;
				const res = await api.post('chat/create', {
					chatroom_name: "聊天", // TODO
					from_user_id: uid,
					to_user_id: eid,
					demand_id
				});
				uni.navigateTo({
					url: '../user-chat/user-chat?cid=' + res.id + '&fid=' + eid
				});
			},
			createOrder() {
				uni.navigateTo({
					url: '../create-order/create-order?rid=' + this.resolusionId
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

	.demo-uni-row {
		margin-bottom: 10px;
		display: block;
	}

	.demo-uni-col {
		height: 36px;
		border-radius: 5px;
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

	.expert-info-detail>view:first-child {
		color: #AAAAAA;
		font-size: 20upx;
		padding: 15upx 0;
	}

	.subBtnBox {
		width: 100%;
		position: fixed;
		bottom: 100upx;
	}

	.subBtn {
		width: 80%;
		height: 72rpx;
		background: linear-gradient(90deg, #ffff00 0%, #f0f000 100%);
		border-radius: 44rpx;
		text-align: center;
		line-height: 72rpx;
		font-size: 32rpx;
		font-weight: 600;
		color: #000000;
		margin: 46rpx auto;
	}

	.u-comment-list-child {
		padding: 20upx;
		background: #F4F4F4;
		border-bottom: 1upx solid #EEEEEE;
		box-sizing: border-box;
		margin: 0;
		margin-left: 70upx;
		width: auto;
	}

	.uni-comment-face image {
		width: 70upx;
		height: 70upx !important;
	}

	.uni-comment-top {
		display: flex;
	}

	.u-comment {
		padding: 0 20upx;
	}

	.u-comment-title {
		padding: 20upx;
		font-size: 30upx;
		font-weight: bold;
	}

	.example {
		width: 100%;
		bottom: 100upx;
		position: fixed;
		background-color: #fff;
	}
</style>
