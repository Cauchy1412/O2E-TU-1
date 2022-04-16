<template>
	<view class="user-space-userinfo">
		<view class="user-space-userinfo-item">
			<view>账号信息</view>
			<view>用户名：{{userinfo.username}}</view>
			<view>邮箱：{{userinfo.email}}</view>
			<view>ID：{{userinfo.id}}</view>
		</view>
		<view class="user-space-userinfo-item">
			<view>个人信息</view>
			<view>机构：{{userinfo.institution}}</view>
<!-- 			<view>故乡：{{userinfo.path}}</view> -->
		</view>
	</view>
</template>

<script>
	import t from "../../common/time.js";
	export default {
		props:{
			userinfo:Object
		},
		computed:{
			getRegAge(){
				return t.gettime.sumAge(this.userinfo.regtime)
			},
			getXingZuo(){
				return t.gettime.getHoroscope(this.userinfo.birthday)
			}
		}
	}
</script>

<style scoped>
.user-space-userinfo{
	padding: 0 30upx;
}
.user-space-userinfo-item{
	padding: 20upx 0;
	border-bottom: 1upx solid #EEEEEE;
}
.user-space-userinfo-item>view{
	color: #AAAAAA;
}
.user-space-userinfo-item>view:first-child{
	color: #333333;
	font-size: 35upx;
	padding: 15upx 0;
}
</style>
