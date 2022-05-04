<template>
	<view class="user-space-userinfo">
		<view class="user-space-userinfo-item">
			<view>账号信息</view>
			<view>用户名：{{userinfo.username}}</view>
			<view>邮箱：{{userinfo.email}}</view>
			<!--<view>ID：{{userinfo.id}}</view>-->
		</view>
		<view class="user-space-userinfo-item" v-if="userinfo.user_type==0">
			<view>个人信息</view>
			<view>真实姓名：{{userinfo.truename}}</view>
			<view>性别：{{userinfo.gender}}</view>
			<view>职称：{{userinfo.professor}}</view>
			<view>研究领域：{{userinfo.domains}}</view>
		</view>
		<view class="user-space-userinfo-item" v-if="userinfo.user_type==2">
			<view>个人信息</view>
			<view>企业名：{{userinfo.truename}}</view>
			<view>公司类型：{{userinfo.business_type}}</view>
			<view>注册地：{{userinfo.place}}</view>
			<view>注册号：{{userinfo.regisnumber}}</view>
			<view>法定代表人：{{userinfo.legalperson}}</view>
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
