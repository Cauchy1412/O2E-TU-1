<template>
	<view class="home-info u-f-ac animated fadeIn fast" @tap="ToUserSpace">
		<image :src="homeinfo.userpic" mode="widthFix" lazy-load></image>
		<view class="u-f1">
			<view>{{homeinfo.username}}</view>
			<view>邮箱: {{homeinfo.email}} </view>
		</view>
		<view class="icon iconfont icon-jinru"></view>
	</view>
</template>

<script>
	export default {
		props:{
			homeinfo:Object
		},
		methods:{
			ToUserSpace(){
				uni.navigateTo({
					url: '../../pages/user-set-userinfo/user-set-info',
				});
			}
		}
	}
</script>

<style scoped>
.home-info{
	padding: 20upx 40upx;
}
.home-info>image{
	flex-shrink: 0;
	width: 100upx!important;
	height: 100upx !important;
	border-radius: 100%;
	margin-right: 15upx;
}
.home-info>view:first-of-type>view:first-child{
	font-size: 32upx;
}
.home-info>view:first-of-type>view:last-child{
	color: #BBBBBB;
}
.home-info>view:last-of-type{
	height: 100%;
}

</style>
