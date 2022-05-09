<template>
	<view>
		<template v-if="userInfo&&!userInfo.id">
			<!-- 未登录 -->
			<view class="u-f-ajc">登陆PaperDaily，体验更多功能</view>
			<!-- 第三方登陆 -->
			<view class="u-f-ajc" @tap="openLogin">账号密码登陆 <view class="icon iconfont icon-jinru"></view>
			</view>
		</template>
		<template v-else>
			<!-- 登陆 -->
			<home-info :homeinfo="homeinfo"></home-info>
		</template>
		<!-- 数据 -->
		<home-data @goToSpace="goToSpace"  :homedata="homedata"></home-data>
		<view style="position: relative;left:100;top:100">
		<view class="user-set-userinfo-list" v-on:click="goOrder()">
				订单管理
		</view>
		<view class="user-set-userinfo-list" v-on:click="goOrder()">
				订单查询
		</view>
		<view class="user-set-userinfo-list" v-on:click="goOrder()">
				订单沟通
		</view>
<!-- 		广告位 -->
<!-- 		<view class="home-adv u-f-ajc animated fadeIn fast">
			<image src="../../static/demo/demo20.jpg"  class="guanggao" lazy-load></image>
		</view> -->
		<!-- 功能列表
		<view class="home-list">
			<block v-for="(item,index) in list" :key="index">
				<home-list-item :userInfo="userInfo" :item="item" :index="index"></home-list-item>
			</block>
			<!-- <image src="../../static/images/tabbar/code_gra" mode=""></image> -->
		</view>


	</view>
</template>

<script>
	import homeListItem from "../../components/home/home-list-item.vue";
	import homeInfo from "../../components/home/home-info.vue";
	import otherLogin from "../../components/home/other-login.vue";
	import homeData from "../../components/home/home-data.vue";
	import {
		getUserProfile,
	} from "@/api/home.js";
	
	import {
		picUrl
	} from "@/api/common.js";
	
	import {
		webUrl
	} from '../../common/config.js'
	import {
		mapState
	} from 'vuex'
	export default {
		components: {
			homeListItem,
			homeInfo,
			otherLogin,
			homeData
		},
		computed: {
			...mapState(['userInfo'])
		},
		onShow() {
			if (this.userInfo.id) {
				this.homeinfo.userpic = this.userInfo.userpic
				this.homeinfo.username = this.userInfo.username
				this.homeinfo.email = this.userInfo.email
				if (!this.islogin) {
					this.initDat()
				}
			} else {
				this.homedata[0].num = 0
				this.homedata[1].num = 0
				this.homedata[2].num = 0
				this.islogin = false
			}

		},
		created() {

		},
		async mounted() {
			this.initDat()
			if (this.userInfo.id) {
				this.homeinfo.userpic = this.userInfo.userpic
				this.homeinfo.username = this.userInfo.username
				this.homeinfo.email = this.userInfo.email
				if (!this.islogin) {
					this.initDat()
				}
			} else {
				this.homedata[0].num = 0
				this.homedata[1].num = 0
				this.homedata[2].num = 0
				this.islogin = false
			}
		},
		data() {
			return {
				islogin: false,
				homeinfo: {
					userpic: this.userInfo ? this.userInfo.userpic : '',
					username: this.userInfo ? this.userInfo.username : "",
					totalnum: 0,
					todaynum: 0,
				},
				homedata: [
					// { name:"话题", num:0 },
					{
						name: "主页",
						num: 0
					},
					{
						name: "评论",
						num: 0
					},
					{
						name: "收藏",
						num: 0
					},
				],
			};
		},
		// 监听下拉刷新
		async onPullDownRefresh() {
			await this.initDat()
			uni.stopPullDownRefresh();
		},
		onNavigationBarButtonTap(e) {
			if (this.userInfo.id) {
				if (e.index == 0) {
					uni.navigateTo({
						url: '../user-set/user-set',
					});
				}
			} else {
					uni.navigateTo({
						url: '../login/login',
					});
			}

		},
		methods: {
			goOrder:function() {
				uni.navigateTo({
					url:'../Order/OrderManagement'
				})
			},
			openLogin() {
				uni.navigateTo({
					url: '../login/login'
				});
			},
			async initDat() {
				if (this.userInfo && this.userInfo.id) {
					let userProfile = await getUserProfile()
					console.log(userProfile)
					this.homeinfo.total_like = userProfile.total_like
					this.homeinfo.total_post = userProfile.total_post
					this.homeinfo.total_collect = userProfile.total_mycollect
					this.homeinfo.email = userProfile.email
					this.homedata[0].num = userProfile.total_post
					this.homedata[1].num = userProfile.total_comment
					this.homedata[2].num = userProfile.total_mycollect
					this.islogin = true
				}
			},
			
			goToSpace(index) {
				// if(this.userInfo.id){
				// 	this.$http.href('../login/login')
				// }
				switch (index) {

					case 0:
							this.$http.href('../../pages/user-space/user-space?uid=' + this.userInfo.id)
						break;
					case 1:
						// this.$http.href('../../pages/user-comment/user-comment?uid=' + this.userInfo.id)

						break;
					case 2:
						this.$http.href('../../pages/user-collect/user-collect?uid=' + this.userInfo.id)
						break;

				}

			}
		}
	}
</script>

<style>
	@import "../../common/form.css";
	.user-set-userinfo-list{
		padding: 40upx;
		border-bottom: 1upx solid #F4F4F4;
	}
	.home-list {
		padding: 20upx;
	}

	.home-adv {
		padding: 20upx;
	}

	.home-adv>image {
		border-radius: 20upx;
		height: 150upx;
	}
	.guanggao{
		width: 100%;
	}
	.tui-page-title {
		width: 100%;
		font-size: 48rpx;
		font-weight: bold;
		color: $uni-text-color;
		line-height: 42rpx;
		padding: 40rpx;
		box-sizing: border-box;
	}
</style>
