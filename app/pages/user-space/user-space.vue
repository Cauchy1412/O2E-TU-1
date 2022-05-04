<template>
	<!-- 此页面对应个人空间页 -->
	<view>
		<!-- 背景图 + 用户基本信息 -->
		<user-space-head 
			@userActive="userActive"
			@refreshData="refreshData"
			:userinfo="info"></user-space-head>
		<!-- 统计 -->
		<view class="user-space-data">
			<home-data :homedata="spacedata"></home-data>
		</view>
		<view style="height: 20upx; background: #F4F4F4;"></view>
		<!-- tab导航 -->
		<swiper-tab-head 
		:tabBars="tabBars" 
		:tabIndex="tabIndex"
		@tabtap="tabtap"
		scrollItemStyle="width:33.33%;"
		scrollStyle="border-bottom:0;">
		</swiper-tab-head>
		<view style="margin-bottom: 5upx;"></view>
		
		<template v-if="tabIndex==0">
			<!-- 主页 -->
			<user-space-userinfo 
				:userinfo="info"
				:authInfo="userInfo"
				></user-space-userinfo>
		</template>
		
		<template v-if="tabIndex==1">
			<!-- 列表 -->
			<view class="topic-list">
			<block v-for="(list,listindex) in topicList" :key="listindex">
				<card @gotoTopic="gotoTopic" :cardinfo="list" :index="listindex"></card>
			</block>
			</view>
			<!-- 上拉加载 -->
		</template>

		<!-- 操作菜单 -->
		<user-space-popup :show="show" 
		@hide="togleShow"
		@lahei="lahei"
		@beizhu="beizhu"></user-space-popup>
		
	</view>
</template>

<script>
	import userSpaceHead from "../../components/user-space/user-space-head.vue";
	import homeData from "../../components/home/home-data.vue";
	import swiperTabHead from "../../components/index/swiper-tab-head.vue";
	import userSpaceUserinfo from "../../components/user-space/user-space-userinfo.vue";
	import commonList from "../../components/common/common-list.vue";
	import card from '../../components/list-card/list-card.vue'
	import loadMore from "../../components/common/load-more.vue";
	import userSpacePopup from "../../components/user-space/user-space-popup.vue";
	import {mapMutations, mapState} from 'vuex'
	import topicList from "../../components/news/topic-list.vue";
	import time from '../../common/time.js'
	import {saveUserAccess,get_user_info,getTopicListByUid,getTopicTitleByUid} from '@/api/user-space.js'
	import {
		picUrl
	} from "@/api/common.js";
	export default {
		components:{
			userSpaceHead,
			homeData,
			swiperTabHead,
			userSpaceUserinfo,
			commonList,
			loadMore,
			userSpacePopup,
			card,
			topicList		
		},
		computed:{
			...mapState(['userInfo'])
		},
		onLoad(data) {
			this.info.id = data.uid
			this.initData(data.uid)
			console.log("onLoad")
			// if(data.uid!=this.userInfo.id){
			// 	saveUserAccess({
			// 		fromId:this.userInfo.id?this.userInfo.id:(+new Date+"").slice(5),
			// 		toId: data.uid
			// 	})
			// }
		},
		onHide() {
		    uni.hideLoading(); 
		    this.ifOnShow = true;
		},
		onShow() {
		    if (this.ifOnShow == true) {
			console.log("onShow")
			this.initData(this.info.id)
		      window.location.reload();//返回当前页面强制书哈辛
		    } 
		},
		provide () {
		    return {
		      reload: this.initData(this.info.id)
		    }
		},
		data() {
			return {
				ifOnShow: false,//首先设置ifOnShow不然会一直循环刷新
				show:false,
				info:{
					currentId: -1,		//app使用者的id
					id:0,				//主页对应用户的id
					bgimg:1,
					userpic:"",
					username:"",
					email:"",
					user_type:-1,
					verified_type:-1,
					truename:"",
					gender:"",
					professor:"",
					domains:"",
					business_type:"",
					place:"",
					regisnumber:"",
					legalperson:"",
					isguanzhu:0,
				},
				topicList:[],
				titleList:[],
				spacedata:[
					{ name:"获赞数", num:0 },
					{ name:"关注", num:0 },
					{ name:"粉丝", num:0 },
				],
				tabIndex:0,
				tabBars:[
					{ name:"主页",id:"zhuye" },
				],
				tablist:[ {},
					{
						loadtext:"",
						list:[
						]
					},
					{
						loadtext:"",
						// 上拉加载更多
						list:[
						]
					},
				],
			}
		},
		// 上拉触底事件
		onReachBottom() {
			// 上拉加载
			this.loadmore();
		},
		onNavigationBarButtonTap(e) {
			if(e.index==0){ this.togleShow(); }
		},
		methods: {
			async initData(id){
				let data = await get_user_info({"id":id});
				let topicList = await getTopicListByUid(id);
				this.topicList = topicList
				// console.log(data)
				if("id" in data){
					this.spacedata[0].num = data.total_like>=1000?(data.total_like/1000)+"k":data.total_like
					this.spacedata[1].num = data.total_fan
					this.spacedata[2].num = data.total_fan
					let currentId = this.userInfo.id
					this.info.currentId = currentId
					this.info.id = data.id
					this.info.userpic = picUrl+data.userpic
					this.info.username = data.username
					this.info.email = data.email
					this.info.user_type = data.user_type
					if (this.info.user_type == 0) {
						this.tabBars.push({ name:"论文解读",id:"lunwenjiedu" })
					}
					this.initmeta(this.info.user_type, data.meta)
					this.info.isguanzhu = data.is_following
				}
			},
			initmeta(type, meta) {
				let domain_str = ""
				if(type == 0) {
					for (let i = 0; i < meta['domains'].length; i++) {
						domain_str = domain_str + meta['domains'][i] + " "
					}
					this.info.truename = meta['name']
					this.info.gender = meta['gender']
					this.info.professor = meta['professor']
					this.info.domains = domain_str
				} else if (type == 2) {
					this.info.truename = meta['name']
					this.info.business_type = meta['business_type']
					this.info.place = meta['place']
					this.info.regisnumber = meta['regisnumber']
					this.info.legalperson = meta['legalperson']
				}
			},
			userActive(){
				this.info.isguanzhu = !this.info.isguanzhu
			},
			async refreshData(){
				let data = await getUserInfo({"user_id":this.info.id});			
				if("id" in data){
					this.spacedata[0].num = data.total_like>=1000?(data.total_like/1000)+"k":data.total_like
					this.spacedata[1].num = data.total_fan
					this.spacedata[2].num = data.total_fan
					let currentId = this.userInfo.id
					this.info.currentId = currentId;
					this.info.userpic = picUrl+data.userpic;
					this.info.username = data.username;
					this.info.email = data.email
					this.info.institution=data.institution
					this.info.isguanzhu = data.is_following;
					this.info.id = data.id;
				}
			},
			gotoTopic(index){
				let topicDetail = this.topicList[index];
				uni.navigateTo({
					url: '../../pages/detail/detail?id='+topicDetail.id,
				});
			},
			// 操作菜单显示隐藏
			togleShow(){
				this.show=!this.show;
			},
			// 私信
			lahei(){
				if(this.info.id==this.userInfo.id){
					this.$http.toast("无法向自己发送私信！")
					return
				}
				this.togleShow();
				uni.navigateTo({
					url: '../../pages/user-chat/user-chat?fid='+this.info.id
				});
			},
			// 备注
			beizhu(){
				console.log("备注")
				this.togleShow()
			},
			// 上拉加载更多
			loadmore(){
				if(this.tablist[this.tabIndex].loadtext!="上拉加载更多"){ return; }
				// 修改状态
				this.tablist[this.tabIndex].loadtext="加载中...";
				// 获取数据
				// this.tablist[this.tabIndex].loadtext="没有更多数据了";
			},
			tabtap(index){
				this.tabIndex=index;
			},
		}
	}
</script>

<style>
.user-space-margin{
	margin: 10upx 10upx 0  10upx;
}
.topic-view{
	padding: 20upx;
}
.topic-list{
	box-sizing: border-box;
	background-color: #F9F9F9;
	padding: 5upx 20upx 0 30upx;
}
.user-space-data{
	background: #FFFFFF;
	position: relative;
	z-index: 10;
	border-top-left-radius: 20upx;
	border-top-right-radius: 20upx;
	margin-top: -15upx;
}

</style>
