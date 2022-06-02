<!-- This file is based on pages/index/index -->
<template>
	<view class="index-icontainer">
		<myNavBar @signIn="signIn"></myNavBar>

		<uni-fab horizontal="right" @fabClick='onFabClick'>
		</uni-fab>
		
		<scroll-view
		 scroll-y class="list" refresher-enabled :refresher-triggered="refreshing" refresher-background="#fafafa"
		 enable-back-to-top :refresher-threshold="100" @refresherrefresh="onrefresh"
		 style='height: 90vh; background-color: white;'
		 >
			<template v-if='sects.length'>
				<uni-section v-for='s in sects' :title='s.name' type="line">
					<uni-list>
						<uni-list-item
							v-for="o in s.items"
							:title='o.title'
							:note='formatDate(o.created_at)'
							:rightText='getStatus(o)'
							@click="openDetail(o)"
						></uni-list-item>
					</uni-list>
				</uni-section>
			</template>
			<view v-else>
				<no-thing></no-thing>
			</view>
		</scroll-view>
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
			uni.$on('ent-demands-update', this.requestData);
		},
		onShow() {
			this.requestData();
		},
		onBackPress() {
			this.requestData();
		},
		computed: {
			...mapState(['userInfo']),
			sects() {
				const r = ['未开始', '进行中', '已完成'].map(s => ({
					name: s,
					items: [],
				}));
				for (const o of this.demands) {
					const s = r[Number(o.state)];
					if (s)
						s.items.push(o);
				}
				return r.filter(s => s.items.length);
			}
		},
		methods: {
			getStatus(o) {
				const s = ['未开始', '进行中', '已完成'];
				return s[Number(o.state)];
			},
			async requestData() {
				/* this.demands =
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
				]; */

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
			openDetail(o) {
				this.$store.state.demand_detail = o;
				uni.navigateTo({
					url: '/pages/needs/needs?did=' + o.id,
				});
			},
			async signIn(){
				this.$http.href("/pages/check-in/check-in")
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
