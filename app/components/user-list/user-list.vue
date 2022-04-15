<template>
	<view class="user-list u-f-ac animated fadeIn fast" @tap="navUserInfo">
		<image :src="item.userpic" mode="widthFix" lazy-load></image>
		<view>
			<view>{{item.username}}</view>
			<view style="display: inline-block;">
				{{item.institution}}
			</view>
		</view>
		<view class="icon iconfont u-f-ajc" 
			></view>
	</view>
</template>

<script>
	import tagSexAge from "../../components/common/tag-sex-age.vue";
	export default {
		components:{
			tagSexAge
		},
		props:{
			item:Object,
			index:Number
		},
		methods:{
			attActive(){
				this.$emit("attActive",this.index,this.item)
			},
			navUserInfo(){
				uni.navigateTo({
					url:'../../pages/user-space/user-space?uid='+this.item.id
				})
			}
		}
	}
</script>

<style scoped>
.user-list{
	margin: 0 20upx; 
	padding: 20upx 0;
	border-bottom: 1upx solid #EEEEEE;
}
.user-list>image{
	width: 100upx!important;
	height: 100upx!important;
	border-radius: 100%;
	margin-right: 20upx;
	flex-shrink: 0;
}
.user-list>view:first-of-type{
	flex: 1;
}
.user-list>view:first-of-type>view:first-child{
	font-size: 35upx;
}
.user-list>view:last-of-type{
	width: 80upx;
	color:#CCCCCC;
}
.icon-zengjia1{
	width: 100upx;
	color: #F8791B!important;
}
</style>
