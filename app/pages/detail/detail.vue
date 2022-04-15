<template>
	<view class="detail">
		<detail-info @goToUserInfo="goToUserInfo"
			@likeOrTread="likeOrTread"
		   :userInfo="userInfo" @comSubimt="comSubimt" :item="detail" :created_by="created_by"></detail-info>

		<view class="u-comment-title" :maskState="maskState">最新评论 {{comment.count}}</view>
		<view class="uni-comment u-comment">
			<block v-for="(item,index) in comment.list" :key="index">
				<comment-list @comSubimt="comSubimt" @comDelete="comDelete" :userInfo="userInfo" :item="item" :index="index"></comment-list>
			</block>
			<template v-if="comment.list.length==0">
				<view>还没有评论,快来说两句~</view>
			</template>
		</view>

		<view style="height: 120upx;"></view>

		<!-- 输入框 -->
		<!-- <user-chat-bottom @submit="submit"></user-chat-bottom> -->
		<!-- <t-rt-popup :itemList="itemList" ref="rtBubble" @click="itemClick"></t-rt-popup> -->
		<!-- 分享 -->
		<!-- <more-share :show="shareshow" @togle="togle"></more-share> -->
		<pl-comment ref="plComment" :maskState="maskState" @toggleState="toggleState" :placeholder="placeText" @pubComment="pubComment"></pl-comment>
	</view>
</template>

<script>
	import detailInfo from "../../components/detail/detail-info.vue";
	import plComment from "../../components/ygc-comment/ygc-comment.vue";
	import time from "../../common/time.js";
	import commentList from "../../components/detail/comment-list.vue";
	import userChatBottom from "../../components/user-chat/user-chat-bottom.vue";
	import moreShare from "../../components/common/more-share.vue";
	import tRtPopup from '@/components/views/t-rt-popup/t-rt-popup';
	import {
		getTopicDetail,
		pushHistory,
		delComment,
		addComment,
		getCommentList
	} from "@/api/detail.js";
	import {
		giveLike
	} from '@/api/common.js'
	import {
		mapState,
		mapMutations
	} from "vuex"
	
	var graceRichText = require("../../components/common/richText.js");
	export default {
		components: {
			tRtPopup,
			detailInfo,
			commentList,
			userChatBottom,
			moreShare,
			plComment
		},
		data() {
			return {
				shareshow: false,
				currentComm: {},
				placeText: "请输入评论",
				comment: {
					count: 0,
					list: []
				},
				itemList: [{
						title: '首页',
						icon: 'home'
					},
					{
						title: '收藏',
						icon: 'star'
					},
					{
						title: '分享',
						icon: 'partake'
					}
				],
				detail: {},
				created_by:{
					
				},
				maskState: false

			}
		},
		onLoad(data) {
			
			try {
				this.initData(data.id)
			} catch (e) {

			}
		},
		onShow(){
			try {
				this.initData(this.detail.id)
			} catch (e) {
			
			}
		},
		// 监听导航右边按钮
		onNavigationBarButtonTap(e) {
			// this.rtBubble()
			// if (e.index == 0) {
			// 	this.togle();
			// }
			// let pages = getCurrentPages(); // 当前页面
			// let beforePage = pages[pages.length - 2]; // 前一个页面
			// uni.navigateBack({
			// 	success: function() {
			// 		beforePage.onshow(); // 执行前一个页面的onLoad方法
			// 	},
			// });
		},
		computed: {
			...mapState(['userInfo'])
		},
		methods: {
			// 初始化数据
			async initData(id) {
				// 修改窗口标题
				uni.setNavigationBarTitle({
					title: "详情"
				});
				let detail = await getTopicDetail(id)
				this.detail = detail
				this.comment.count = detail.commentNum
				this.created_by = detail.created_by
				this.detail.content= graceRichText.format(this.detail.content)
				this.getcomment(detail.uid);
				
				this.$nextTick(()=>{
					this.detail = detail
				})
			},
			togle() {
				this.shareshow = !this.shareshow
			},
			itemClick(e) {
				switch(e.index){
					case 0: 
						uni.switchTab({
							url:'../index/index'
						})
					break;
					case 1:
						
					break;
					case 2:
					
					break;
				}
				let text = ["首页", "收藏", "分享"][e.index];
				this.$http.toast(`您点击了：${text}`);
			},
			onClick(){
				if(!this.userInfo || !this.userInfo.id){
					uni.showToast({
						title:"你还未登录！或登录过有效期!",
						icon:'none'
					})
					return
				}
				this.$http.post('topic/collect',{
					...this.topicActive,
					title:this.item.title,
					username:this.item.username,
					userpic:this.item.userpic
				})
				this.collect = !this.collect
			},
			rtBubble() {
				this.$refs.rtBubble.toggle();
			},
			comSubimt(item) {
				this.currentComm = item
				this.placeText = `回复  ${item.created_by.username}:`
				this.maskState = true
			},
			async comDelete(item) {
				await delComment(item.id)
				await this.getcomment();
			},
			async pubComment(text) {
				if (text == "") {
					return
				}
				if(this.currentComm.title){
					await addComment({
						interpretation_id:this.detail.id,
						parent_comment_id: null,
						to_user_id: null,
						content: text
					})
				}else{
					await addComment({
						interpretation_id:this.detail.id,
						parent_comment_id: this.currentComm.id,
						to_user_id: this.currentComm.user_id,
						content: text
					})
				}
				await this.getcomment()
				this.maskState = !this.maskState
			},
			toggleState() {
				this.maskState = !this.maskState
			},
			
			goToUserInfo(item) {
				
				uni.navigateTo({
					url: '../../pages/user-space/user-space?uid=' + item.uid
				})
			},
			async likeOrTread(data) {
				giveLike(data)
				if(this.detail.is_like){
					this.$http.toast("你已取消点赞!")
				}else{
					this.$http.toast("点赞成功!")
					
				}
			},
			// 获取评论
			async getcomment(id) {
				let items = await getCommentList(id,{"interpretation_id":this.detail.id})
				this.comment.list = items.ans;
				this.comment.count = items.length;
				this.detail.commentNum = items.length
			},
			formatRichText (html) {
							// 去掉img标签里的style、width、height属性
							let newContent= html.replace(/<img[^>]*>/gi,function(match,capture){
								match = match.replace(/style="[^"]+"/gi, '').replace(/style='[^']+'/gi, '');
								match = match.replace(/width="[^"]+"/gi, '').replace(/width='[^']+'/gi, '');
								match = match.replace(/height="[^"]+"/gi, '').replace(/height='[^']+'/gi, '');
								return match;
							});
							// 修改所有style里的width属性为max-width:100%
							newContent = newContent.replace(/style="[^"]+"/gi,function(match,capture){
								match = match.replace(/width:[^;]+;/gi, 'max-width:100%;').replace(/width:[^;]+;/gi, 'max-width:100%;');
								return match;
							});
							// 去掉<br/>标签
							newContent = newContent.replace(/<br[^>]*\/>/gi, '');
							// img标签添加style属性：max-width:100%;height:auto
							newContent = newContent.replace(/\<img/gi, '<img style="max-width:100%;height:auto;display:block;margin:0px auto;"');
							return newContent;
			},
		}
	}
</script>

<style>
	/* 评论 */
	.u-comment {
		padding: 0 20upx;
	}

	.u-comment-title {
		padding: 20upx;
		font-size: 30upx;
		font-weight: bold;
	}
</style>
