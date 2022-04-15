<template>
	<view class="common-list u-f animated fadeIn fast">
		<view class="common-list-r">
			<view class="topic-title">
				<text style="font-weight: bold;font-size:x-large;">{{item.title}}</text>
			</view>
			<view>
				<view class="u-f-ac u-f-jsb">
					<view class="common-list-l" @tap="goToUserInfo(item)">
						<image :src="item.userpic" class="com-img" lazy-load></image>
						<view class="u-f-ac dre">
							<text class="author-name">{{created_by.username}} </text>
						</view>
					</view>
<!-- 					<template v-if="!isme">
						<view v-if="!isguanzhu" @tap="guanzhu"
							class="icon iconfont icon-zengjia guanzhu">关注</view>
						<view v-else @tap="guanzhu"
							class="icon iconfont guanzhu">取消关注</view>
					</template> -->
				</view>
				<view class="common-list-r-time">{{createDate}}</view>
			</view>
			
			<view>
				<rich-text v-html="item.content"></rich-text>
				<!-- <rich-text :nodes="formatRichText(item.content)"></rich-text> -->
			</view>
			
			<view class="u-f-ac u-f-jsb">
				<view>{{item.path}}</view>
				<view class="u-f-ac">
				<view class="active-comm" @tap="onCollect">
					<tui-icon :name="item.is_favor?'star-fill':'star'" :color="item.is_favor?'#FFE933':''"  :size="size" unit="upx"></tui-icon>
					<text class="active-text">{{item.is_favor?"取消收藏": "收藏"}}</text>
				</view>

				<view class="active-comm" @tap="giveLike">
					<tui-icon :name="item.is_like?'agree-fill': 'agree'" :color="item.is_like?'#FFE933': ''" :size="size" unit="upx"></tui-icon>
					<text class="active-text">
						{{item.like_num==0?"点赞": item.like_num}}
					</text>
				</view>
				<view class="active-comm" @tap="showComInput">
					<tui-icon name="community" :size="size" unit="upx"></tui-icon>
					<text class="active-text">{{item.commentNum==0?"评论": item.commentNum}}</text>
				</view>
				</view>
			</view>
		</view>

	</view>
</template>

<script>
	import time from "../../common/time.js";
	export default {
		components:{
		},
		props:{
			item:Object,
			userInfo:Object,
			created_by:Object
		},
		data() {
			return {
				isguanzhu: this.item.isguanzhu,
				list: "list3",
				size: 48,
			}
		},
		computed:{
			createDate(){
				let data =this.item.created_at? new Date(this.item.created_at).getTime():+new Date;
				return time.gettime.sumAge(data)
			},
			isme(){
				return 	this.userInfo.id==this.created_by.id
			}
		},
		mounted(){
			console.log(this.item)
		},
		watch:{
			'item.id':function(){
				this.isguanzhu= this.item.isguanzhu
			}
		},
		methods:{
			goToUserInfo(item){
				this.$emit("goToUserInfo",item)
			},

			onCollect(){
				let headers = {
					"Authorization":'Bearer ' + uni.getStorageSync('token')
				}
				if(!this.userInfo.id){
					this.$http.href('../../pages/login/login')
					return 
				}
				if(this.item.is_favor){
					this.$http.post('Interpretation/'+this.item.id+'/unfavor',{},headers)
					this.$http.toast("取消收藏!")
				}else{
					this.$http.post('Interpretation/'+this.item.id+'/favor',{},headers)
					this.$http.toast("收藏成功!")
				}
				this.item.is_favor = !this.item.is_favor
			},
			guanzhu(){
				let headers = {
					"Authorization":'Bearer ' + uni.getStorageSync('token')
				}
				if(!this.userInfo.id){
					this.$http.href('../../pages/login/login')
					return 
				}
				if(this.isguanzhu){
					this.$http.post('user/'+this.created_by.id+'/unfollow',{},headers)
					this.isguanzhu=false;
					this.$http.toast("取消关注!")
				}else{
					this.$http.post('user/'+this.created_by.id+'/follow',{},headers)
					this.isguanzhu=true;
					this.$http.toast("关注成功!")

				}
				
			},
			showComInput(){
				if(!this.userInfo.id){
					this.$http.href('../../pages/login/login')
					return 
				}
				
				this.$emit("comSubimt",this.item)
			},
			async giveLike(){
				if(!this.userInfo.id){
					this.$http.href('../../pages/login/login')
					return 
				}
				if(this.item.is_like){
					this.item.like_num--
					await this.$emit("likeOrTread",this.item.id)
				}else{
					this.item.like_num++
					await this.$emit("likeOrTread",this.item.id)
				
				}
				this.item.is_like = !this.item.is_like
			},
		}
	}
</script>

<style scoped>
@import "../../common/list.css";
	
.common-list-l{
	display:flex;
	
}
.common-list-l .com-img{
	width: 68upx!important;
	height: 68upx!important;
	margin-right: 20upx;
	border-radius: 50%;
}
 .author-name{
	 /* color: #000000; */
	font-weight: 700;
}
.active-comm{
	display: flex;
	align-items: center;
	margin-right: 20upx;
	color: #666666;
}
.active-text{
	margin-left: 10upx;
	font-weight: 500;
}
.dre{
	display: flex;
	flex-direction:row ;
	padding-left: 10upx;
}
.common-list-r{
	border-bottom: 0;
	
}
.common-list{
	border-bottom: 1upx solid #EEEEEE;
}
.common-list-r-time{
	padding: 20upx 0 0 10upx;
	color: #CCCCCC!important;
	font-size: 25upx;
	background: #FFFFFF!important;
}
.common-list-r>view:nth-child(1)>view:nth-child(1)>view:first-child{
	color: #999999;
	font-size: 32upx;
}

.common-list-r>view:nth-child(1)>view:nth-child(1)>view:last-child{
	background-color: #FFFFFF;
	padding: 0 10upx;
	font-size: 26upx;
}
.common-list-r .list3{
	display: flex;
	flex-direction: row;
	padding-top: 15upx;
	justify-content: space-between;
	flex-wrap: wrap;
	}
.common-list-r .list3 .img-n>image{
	width: 230upx;
	height: 230upx;
	margin-bottom: 10upx;
	border-radius: 20upx;
	margin-right: 7upx;
}
.img-1{
	width: 100%;
}
.img-1>image{
	width: 100%;
	margin-bottom: 10upx;
	border-radius: 20upx;
}
.common-list-r .list4>image{
	margin-bottom: 10upx;
	border-radius: 20upx;
}

.container1 {
        padding: 10px;
}

</style>
