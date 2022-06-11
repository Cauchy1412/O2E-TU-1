<template>
	<view class="index-icontainer">
		<!-- #ifdef MP-WEIXIN -->
		<!-- 		<view class="search-wrp">
			<view class="iconfont icon-icon_A font-x" @tap="checkIn"></view>
			<view class="iconfont icon-sousuo serach">
			</view>
			<input class="uni-input" type="text" placeholder="PaperDaily" @focus="searchInfo" />
			<view class="iconfont icon-fabiao font-x" @tap="publish"></view>
		</view> -->
		<!-- #endif -->
		<!--myNavBar @signIn="signIn"></myNavBar-->
		<!-- <tui-fab bgColor="#FFE933" :width="98" :height="98" :bottom="150" :right="50" @click="publish"></tui-fab> -->
		<swiper-tab-head :tabBars="tabBars" :tabIndex="tabIndex" @tabtap="tabtap">
		</swiper-tab-head>
		
		<view class="uni-tab-bar">
			<swiper class="swiper" style="height: 90vh;" :current="tabIndex" @change="tabChange">
				<swiper-item v-for="(items,index) in newslist" :key="index">
					<scroll-view
					@scroll="handleScroll"
					 scroll-y class="list" refresher-enabled :refresher-triggered="refreshing" refresher-background="#fafafa"
					 enable-back-to-top :refresher-threshold="100" @refresherrefresh="onrefresh" >
						<!-- 图文列表 -->
						<template v-if="items.list.length>0 && tabIndex == 0">
							<block v-for="(item,index1) in items.list" :key="index1">
								<index-list
								@likeOrTread="likeOrTread" @opendDetail="opendDetail" @share="share" :item="item" :userInfo="userInfo"
								 :index="index1"></index-list>
							</block>
							<load-more :loadtext="items.loadtext"></load-more>
						</template>

						<template v-if="items.list.length>0 && tabIndex == 1">
							<view class="topic-list">
								<block v-for="(list,index1) in items.list" :key="index1">
									<card @opendDetail="opendDetail" :cardinfo="list" :index="index1"></card>
								</block>
							</view>
						</template>

						<template v-if="items.list.length>0 && tabIndex == 2">
							<view class="topic-list">
								<view v-for="(list,index1) in items.list" :key="index1" @tap='() => openDemandDetail(list)'>
									<!--card @opendDetail="list.title" :cardinfo="list" :index="index1"></card-->
									<demand-row :demand="list" :show_company="true"></demand-row>
								</view>
							</view>
						</template>

						<template v-if="shoNo || !items.list.length">
							<!-- 无内容默认 -->
							<no-thing></no-thing>
						</template>
					</scroll-view>
				</swiper-item>
			</swiper>
		</view>
	</view>
</template>


<script>
	import indexList from "../../components/index/index-list.vue";
	import swiperTabHead from "../../components/index/swiper-tab-head.vue";
	import loadMore from "../../components/common/load-more.vue";
	import noThing from "../../components/common/no-thing.vue";
	import myNavBar from "../../components/common/my-nav-bar.vue";
	import uniCalendar from '@/components/uni-calendar/uni-calendar.vue'
	import card from '../../components/list-card/list-card-1.vue'
	import demandRow from '@/components/demand-row.vue';
	import {
		getTopicList,
		getRecommendList, api
	} from '@/api/index.js'
	import {
		giveLike
	} from '@/api/common.js'
	import {
		mapState,
		mapMutations
	} from "vuex"
	export default {
		name: 'NaiveIndex',
		components: {
			indexList,
			swiperTabHead,
			loadMore,
			noThing,
			uniCalendar,
			myNavBar,
			card,
			demandRow
		},
		data() {
			return {
				swiperheight: 500,
				tabIndex: 2,
				start:0,
				remain:3,
				end: 5,
				size: 400,
				// list 偏移量
				offset: 0,
				refreshing: false,
				shoNo: false,
				popupShow: false,
				shareList: [{
					share: [{
						name: "QQ",
						icon: "qq",
						color: "#07BDFD",
						size: 68
					}, {
						name: "微信",
						icon: "wechat",
						color: "#80D640",
						size: 68
					}, {
						name: "朋友圈",
						icon: "moments",
						color: "#80D640",
						size: 68,
					}]
				}, {
					operate: [{
						name: "刷新",
						icon: "refresh",
						size: 56
					}, {
						name: "搜索内容",
						icon: "search-2",
						size: 56
					}]
				}],
				tabBars: [{
						name: "推荐",
						id: "tuijian",
						page: 1
					},
					{
						name: "热榜",
						id: "hanfu",
						page: 2
					},
					{
						name: "需求广场",
						id: "demands",
						page: 3
					},
				],
				newslist: [{
						loadtext: "没有更多数据了",
						id: "recommend",
						list: []
					},
					{
						loadtext: "没有更多数据了",
						id: "hotList",
						list: []
					},
					{
						loadtext: "没有更多数据了",
						id: "demandlist",
						list: []
					},
				],


			}
		},
		onLoad() {
			uni.getSystemInfo({
				success: (res) => {
					let height = res.windowHeight - uni.upx2px(100)
					this.swiperheight = height;
				}
			});
			this.requestData()
		},
		onShow() {
			this.requestData()
		},
		onTabItemTap() {
			this.requestData()
		},
		onBackPress() {
			this.requestData();
		},
		mounted() {
			this.requestData();
			uni.$on('user_change', this.requestData);
		},
		computed: {
			...mapState(['userInfo']),
			// 预留项
			preCount() {
				return this.newslist.map(item=>{
					return Math.min(this.start, this.remain);
				})
			},
			nextCount() {
				return this.newslist.map(item=>{
					return Math.min(item.list.length - this.end, this.remain);
				})
			}
		},

		methods: {
			async requestData(GoPage, Gotype) {
				// let currentPage = GoPage || this.tabBars[this.tabIndex].page;
				let type = this.tabBars[this.tabIndex].id;
				let items;
				try {
					if(this.tabIndex==1){
						items = await getTopicList()
					}else if (this.tabIndex == 0){
						items = await getRecommendList()
					} else {
						const resp = await api.get('demand/all');
						items = resp.demand_list;
					}
				} catch (e) {
					items = [];
				}
				// this.tabBars[this.tabIndex].page = page
				// if(this.tabIndex === 1){
				// 	this.newslist[this.tabIndex].list = items
				// }else{
				// 	this.newslist[this.tabIndex].list = this.newslist[this.tabIndex].list.concat(items)
				// }
				if (items && items.length > 0) {
					this.newslist[this.tabIndex].list = items
					this.newslist[this.tabIndex].loadtext = "上拉加载更多";
				}else{
					this.newslist[this.tabIndex].list = []
					this.newslist[this.tabIndex].loadtext = "没有更多数据了";
				}
			},
			publish() {
				// 打开发布页面
				this.$http.href("../add-input/add-input")
			},
			searchInfo() {
				// uni.navigateTo({
				// 	url: '../search/search',
				// });
			},
			share() {
				this.popupShow = !this.popupShow
			},
			popup: function() {
				this.popupShow = !this.popupShow
				this.$http.toast("敬请期待~")
			},
			async onrefresh() {
				if (this.refreshing) return;
				this.refreshing = true;
				await this.requestData()
				setTimeout(() => {
					this.refreshing = false;
					uni.showToast({title:'已更新',duration:500})
				}, 200)
			},
			loadmore(index) {
				// if (this.newslist[index].loadtext != "上拉加载更多") {
				// 	return;
				// }
				// // 修改状态
				// this.newslist[index].loadtext = "加载中...";
				// const scrollTop = ev.detail.scrollTop;
				// // 开始位置
				// const start = Math.floor(scrollTop / this.size)
				// this.start = start < 0 ? 0 : start;
				// // 结束位置
				// this.end = this.start + this.remain;
				// // 计算偏移
				// const offset = scrollTop - (scrollTop % this.size) - this.preCount * this.size
				// this.offset = offset < 0 ? 0 : offset;
				// 获取数据
				// this.requestData(this.tabBars[this.tabIndex].page + 1)

			},
			handleScroll(ev) {
				const scrollTop = ev.detail.scrollTop;
				// console.log(scrollTop)
				// console.log(this.newslist[this.tabIndex])
				// 开始位置
				const start = Math.floor(scrollTop / this.size)
				this.start = start < 0 ? 0 : start;
				// 结束位置
				this.end = this.start + this.remain;
				// 计算偏移
				const offset = scrollTop - (scrollTop % this.size) - this.preCount[this.tabIndex] * this.size
				this.offset = offset < 0 ? 0 : offset;
			},
			// tabbar点击事件
			tabtap(index) {
				this.tabIndex = index;
			},
			// 滑动事件
			tabChange(e) {
				console.log('tabchange', e);
				this.tabIndex = e.detail.current;
				this.requestData(this.tabBars[this.tabIndex].page, this.tabBars[this.tabIndex].id)
			},
			async likeOrTread(data) {
				giveLike(data.id)
				console.log(data)
				if(data.is_like){
					this.$http.toast("你已取消点赞!")
				}else{
					this.$http.toast("点赞成功!")
				}
			},
			opendDetail(item) {
				uni.navigateTo({
					url: '../../pages/detail/detail?id=' + item.id,
				});
			},
			initNavigation(e) {
				this.opcity = e.opcity;
				this.top = e.top;
			},
			signIn() {
				this.$http.href("../../pages/check-in/check-in")
			},
			openDemandDetail(o) {
				this.$store.state.demand_detail = o;
				uni.navigateTo({
					url: '/pages/needs/needs?did=' + o.id,
				});
			},
		},

	}
</script>

<style>
@import '/styles/index.css'
</style>
