<template>
	<view class="index-icontainer">
		<myNavBar @signIn="signIn"></myNavBar>

		<swiper-tab-head :tabBars="tabBars" :tabIndex="0">
		</swiper-tab-head>

		<uni-fab horizontal="right" @fabClick='onFabClick'>

		</uni-fab>

		<view class="uni-tab-bar">
			<swiper class="swiper-box" :style="{height:swiperheight+'px'}">
				<swiper-item>
					<scroll-view
					 scroll-y class="list" refresher-enabled :refresher-triggered="refreshing" refresher-background="#fafafa"
					 enable-back-to-top :refresher-threshold="100" @refresherrefresh="onrefresh" >

						<template v-if="demands.length">
							<view class="topic-list">
								<block v-for="(list,index1) in demands" :key="index1">
									<!--card @opendDetail="list.title" :cardinfo="list" :index="index1"></card-->
									<demand-row :demand="list"></demand-row>
								</block>
							</view>
						</template>
						<template v-else>
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
	import { api } from '@/api';
	import { mapState } from "vuex";
	
	export default {
		name: 'EntIndex',
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
				tabIndex: 1,
				start:0,
				remain:3,
				end: 5,
				size: 400,
				// list 偏移量
				offset: 0,
				refreshing: false,
				popupShow: false,
				demands: [],
				tabBars: [
					{
						name: "全部",
						id: "my",
						page: 1
					}
				],
			}
		},
		mounted() {
			uni.getSystemInfo({
				success: (res) => {
					let height = res.windowHeight - uni.upx2px(100)
					this.swiperheight = height;
				}
			});
			this.requestData();
		},
		computed: {
			...mapState(['userInfo']),
		},
		methods: {
			async requestData() {
				this.demands = 
					[
					{
						description: '我想做一个基于Vue的React框架',
						title: '基于Vue的React框架',
						created_at: new Date(Date.now()),
					},
					{
						description: 'QAQ',
						title: '基于React的OS内核',
						created_at: new Date(Date.now() - 2000),
					},
				];
				
				const res = await api.get('demand');
				this.demands = res.demand_list.map(o => ({
					...o,
					created_at: new Date(o.created_at)
				}));
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
			opendDetail(item) {
				uni.navigateTo({
					url: '../../pages/detail/detail?id=' + item.id,
				});
			},
			async signIn(){
				this.$http.href("../../pages/check-in/check-in")
			},
			onFabClick() {
				this.navigateToPage('demand/create');
			}
		},

	}
</script>

<style>
@import '/styles/index.css'
</style>