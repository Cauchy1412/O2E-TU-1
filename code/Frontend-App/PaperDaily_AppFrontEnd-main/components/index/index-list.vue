<template>
	<view class="container"> 
		<view class="item-list">
			<view class="topic-title" @tap="opendetail">
				<text style="font-weight: bold;font-size:larger;">{{item.title}}</text>
			</view>
			<view class="author-wrap" @tap="opendetail">
				<image class="anthor-pic" :src="item.userpic" lazy-load mode="aspectFill"></image>
				<text class="author-name">{{item.username}}</text>
			</view> 
			<view span="7" class="container1" @tap="opendetail">
			    <editor v-html="item.content" read-only=true></editor>
			</view>
			<view style="color: #007AFF;" @tap="opendetail">
				<template v-for="tag in item.tags">
					#{{tag.name}}#
				</template>
			</view> 
		<!-- 	<template v-if="item.urlType=='img'">
				<view v-if="item.images&&item.images.length>2" class="image-view-n">
						<block v-for="(items,index1) in item.images" :key="index1">
							<image :src="items"
							lazy-load @tap="imgdetail(index1)"></image>
						</block>
				</view>
				<view v-else-if="item.images.length==2" class="image-view-2">
						<block v-for="(items,index1) in item.images" :key="index1">
							<image :src="items"
							lazy-load @tap="imgdetail(index1)"></image>
						</block>
				</view>
				<view v-else-if="item.images.length==1" class="image-view-1">
					<image :src="item.images[0]"
					lazy-load mode="aspectFit" @tap="imgdetail(0)"></image>
				</view>
			</template> -->

			
			<view class="topic-active">
				<view class="active-comm" @tap="onCollect">
					<tui-icon :name="item.is_favor?'star-fill':'star'" :color="item.is_favor?'#FFE933':''"  :size="size" unit="upx"></tui-icon>
					<text class="active-text">{{item.is_favor?"取消收藏": "收藏"}}</text>
				</view>
				<view class="active-comm" @tap="opendetail">
					<tui-icon name="community" :size="size" unit="upx"></tui-icon>
					<text class="active-text">{{item.commentNum==0?"评论": item.commentNum}}</text>
				</view>
				<view class="active-comm" @tap="giveLike">
					<tui-icon :name="item.is_like?'agree-fill': 'agree'" :color="item.is_like?'#FFE933': ''" :size="size" unit="upx"></tui-icon>
					<text class="active-text">
						{{item.like_num==0?"点赞": item.like_num}}
					</text>
				</view>
			</view>
		</view>

		</view>


	</view>
</template>

<script>
	import uniFav from '@/components/uni-fav/uni-fav.vue'
	import {
		picUrl
	} from "@/api/common.js";
	export default {
		components:{
			uniFav
		},
		props:{
			item:Object,
			index:Number,
			userInfo:Object
		},
		data() {
			return {
				isguanzhu: this.item.isguanzhu,
				collect: this.item.collect,
				size: 48,
				topicActive:{
					uid:this.userInfo.id,
					tid:this.item.id,
					tuid: this.item.uid,
					cid:this.item.cid
					
				}
			}
		},
		methods: {
			async giveLike(){
				if(!this.userInfo.id){
					this.$http.href("../../pages/login/login")
					return
				}
				if(this.item.is_like){
					this.item.like_num--
					await this.$emit("likeOrTread",this.item)
				}else{
					this.item.like_num++
					await this.$emit("likeOrTread",this.item)
				}
				this.item.is_like = !this.item.is_like
			},
			opendetail(){
				this.$emit("opendDetail",this.item)
			},
			imgdetail(index){
				uni.previewImage({
					current:index,
					urls:this.item.images
				})
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
		}
	}
</script>

<style scoped>
.container{
	display: flex;
	box-sizing: border-box;
	width: 100vw;
	align-items: center;
	flex-direction: column;
	background-color: #F9F9F9;
	padding: 0 20upx ;
}
.author-wrap{
	display: flex;
	height: 90upx;
	align-items: center;
	overflow: hidden;
}
.anthor-pic{
	width: 60upx;
	height: 60upx;
	margin-right: 20upx;
	border-radius: 50%;
	
}
.topic-text{
	margin-bottom: 10upx;
}
.topic-active{
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin: 0 20upx;
	height: 100upx;
	line-height: 100upx;
}
.active-comm{
	display: flex;
	align-items: center;
	color: #666666;
}
.active-text{
	margin-left: 10upx;
}
.author-wrap .author-name{
	font-weight: 700;
}

.item-list{
	background-color: #FFFFFF;
	box-sizing: border-box;
	width: 100%;
	min-height: 300upx;
	border-radius: 20upx;
	margin-bottom: 25upx;
	padding: 14upx;
}
.image-view-n{
	display: flex;
	flex-wrap: wrap;
	justify-content: space-between;
}
.image-view-n >image{
	width: 220upx;
	height: 220upx;
	border-radius: 10upx;
	/* margin-right: 10upx; */
	margin-bottom: 10upx;
}
.image-view-2{
	display: flex;
	flex-wrap: wrap;
	justify-content: start;
}
.image-view-2 >image{
	width: 220upx;
	height: 220upx;
	border-radius: 10upx;
	margin-right: 10upx;
	margin-bottom: 10upx;
}
.image-view-1{
	display: flex;
	justify-content: flex-start;
}

.container1 {
        padding: 10px;
}

#editor {
        width: 100%;
        height: 300px;
        background-color: #CCCCCC;
}
</style>
