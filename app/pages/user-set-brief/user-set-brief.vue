<template>
	<view class="body">
		<textarea class="user-set-brief" 
				  :value="brief" 
				  placeholder="编辑您的简介信息,不超过120个字符"
				  type="text"
				  maxlength="120"
				  :auto-height="false"
				  @input="decrease"/>
		<view class="user-line"></view>		  
		<view class="user-set-brief-count">{{leftlength}}</view>
		
		<button class="user-set-btn"
		type="primary" @tap="submit">保存</button>
		
	</view>
</template>

<script>
	import {mapState, mapMutations} from 'vuex'
	import {updateUserInfo} from '@/api/user-set-userinfo.js'
	export default {
		data() {
			return {
				brief:"",
				maxlength:120,
				leftlength:120,
			}
		},
		computed: {
			...mapState(['userInfo'])
		},
		mounted() {
			this.brief = this.userInfo.meta['info']
		},
		methods: {
			...mapMutations(['setUserInfo']),
			decrease(e) {
				this.leftlength = this.maxlength - e.detail.value.length;
				this.brief = e.detail.value
			},
			async submit() {
				if (this.brief == "") {
					this.$http.toast("简介信息为空");
					return;
				}
				let new_user = JSON.parse(JSON.stringify(this.userInfo))
				new_user.meta['info'] = this.brief
				console.log(new_user)
				let res = await updateUserInfo(new_user)
				if (!res || !res.result) {
					this.$http.toast("修改失败");
				} else {
					this.setUserInfo(new_user)
					uni.navigateBack({
						complete() {
							setTimeout(() => {
								uni.showToast({
									title: '修改成功',
									icon: "success",
									duration: 1000
								});
							}, 100);
						}
					});
				}
			}
		}
	}
</script>

<style>
@import "../../common/form.css";
.user-set-brief{
	font-size: 24upx;
	margin-top: 20upx;
	margin-left: 35upx;
	height: 300upx;
}
.user-line{
	height: 1px;
	width: inherit;
	background-color: #000000;
}
.user-set-brief-count{
	text-align: right;
	margin-right: 20upx;
}
</style>
