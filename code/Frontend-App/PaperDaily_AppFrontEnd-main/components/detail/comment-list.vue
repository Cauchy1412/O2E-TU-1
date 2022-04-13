<template>
	<view class="">
		<view class="uni-comment-list" :class="{'u-comment-list-child':(item.parentId>0)}">
			<view class="uni-comment-face"><image :src="item.userpic" mode="widthFix"></image></view>
			<view class="uni-comment-body">
				<view class="uni-comment-top">
					<text>{{item.username}}</text>
					<text v-if="userInfo.id==item.user_id" @tap="deleteCom(item)">删除</text>
				</view>
				<view class="uni-comment-content" @tap="comment(item)">
				<!-- <rich-text v-html="item.text"></rich-text> -->
				<text style="word-break:break-all;">{{item.text}}</text>
				</view>
				<view class="uni-comment-date">
					<view>{{time}}</view>
				</view>
			</view>
		</view>
		<template v-if="item.children&&item.children.length>0">
		
		<view v-for="items in item.children" :key="items.id">
			<view class="uni-comment-list u-comment-list-child" >
				<view class="uni-comment-face">
					<image :src="items.userpic" mode="widthFix"></image></view>
				<view class="uni-comment-body">
					<view class="uni-comment-top">
						<text>{{items.username}}</text>
						<text v-if="userInfo.id==items.user_id" @tap="deleteCom(items)">删除</text>
					</view>
					<!-- @tap="comment(items)" -->
					<view class="uni-comment-content" @tap="comment(item)">
					<rich-text v-html="item.text"></rich-text>
					</view>
					<view class="uni-comment-date">
						<view>{{time}}</view>
					</view>
				</view>
			</view>
		</view>
		</template>
		
	</view>
	
</template>

<script>
	import time from "../../common/time.js";
	export default {
		props:{
			item:Object,
			index:Number,
			userInfo:Object
		},
		methods:{
			comment(item){
				console.log(item)
				if(!this.userInfo.id){
					this.$http.href('../../pages/login/login')
					return 
				}
				this.$emit("comSubimt",item)
			},
			deleteCom(item){
				this.$emit("comDelete",item)				
			}
		},
		computed:{
			time(){
				let date = new Date(this.item.created_at).getTime()
				return time.gettime.gettime(date);
		}
	},
	}
</script>

<style scoped>
.u-comment-list-child{
	padding: 20upx;
	background: #F4F4F4;
	border-bottom: 1upx solid #EEEEEE;
	box-sizing: border-box;
	margin: 0;
	margin-left: 70upx;
	width: auto;
}
.uni-comment-face image{
	width: 70upx;
	height: 70upx!important;
}
.uni-comment-top{
	display: flex;
}
</style>
