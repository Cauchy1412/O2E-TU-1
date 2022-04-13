<template>
	<view class="container">
		<view class="tui-status-bar"></view>
		<view class="tui-header">
			<!-- <view>ThorUI组件库</view> -->
			<tui-icon name="shut" :size="52" @click="back"></tui-icon>
		</view>
		<view class="tui-page-title">注册</view>
		<view class="tui-form">
			<view class="tui-view-input">
				<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
					<view class="tui-cell-input">
						<tui-icon name="people" color="#6d7a87" :size="40"></tui-icon>
						<input :value="username" placeholder="请输入用户名" placeholder-class="tui-phcolor" type="text" maxlength="36" @input="inputUserName" />
						<view class="tui-icon-close" v-show="username" @tap="clearInput(1)">
							<tui-icon name="close-fill" :size="32" color="#bfbfbf"></tui-icon>
						</view>
					</view>
				</tui-list-cell>
				<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
					<view class="tui-cell-input">
						<tui-icon name="pwd" color="#6d7a87" :size="40"></tui-icon>
						<input :value="password" placeholder="请输入密码" :password="true" placeholder-class="tui-phcolor" type="text"
						 maxlength="36" @input="inputPwd" />
						<view class="tui-icon-close" v-show="password" @tap="clearInput(2)">
							<tui-icon name="close-fill" :size="32" color="#bfbfbf"></tui-icon>
						</view>
					</view>
				</tui-list-cell>
				<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
					<view class="tui-cell-input">
						<tui-icon name="mail" color="#6d7a87" :size="40"></tui-icon>
						<input :value="email" placeholder="邮箱" placeholder-class="tui-phcolor" type="text"
						 maxlength="36" @input="inputEmail" />
						<view class="tui-icon-close" v-show="email" @tap="clearInput(3)">
							<tui-icon name="close-fill" :size="32" color="#bfbfbf"></tui-icon>
						</view>
					</view>
				</tui-list-cell>
				<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
					<view class="tui-cell-input">
						<tui-icon name="shield" color="#6d7a87" :size="40"></tui-icon>
						<input placeholder="请输入验证码" placeholder-class="tui-phcolor" type="text" maxlength="6" @input="inputCode" />
						<view @tap="getCheckNum" class="tui-btn-send" :class="{ 'tui-gray': isSend }" :hover-class="isSend ? '' : 'tui-opcity'"
						 :hover-stay-time="150">{{ btnSendText }}</view>
					</view>
				</tui-list-cell>
			</view>
			<view class="tui-btn-box">
				<tui-button @tap="toRegister" :disabledGray="true" :disabled="disabled" :shadow="true" shape="circle">注册</tui-button>
			</view>
			<view class="tui-cell-text">
				注册代表同意
				<view class="tui-color-primary" hover-class="tui-opcity" :hover-stay-time="150" @tap="protocol">PaperDaily用户服务协议、隐私政策</view>
			</view>
		</view>
	</view>
</template>

<script>
	import {
		userRegister,
		getCode,
	} from '@/api/register.js'
	import {
		mapMutations
	} from 'vuex';
	export default {
		computed: {
			disabled: function() {
				let bool = true;
				if (this.username && this.code && this.password) {
					bool = false;
				}
				return bool;
			}
		},
		data() {
			return {
				username: '',
				password: '',
				code: '',
				email:'',
				isSend: false,
				btnSendText: '获取验证码' //倒计时格式：(60秒)
			};
		},
		methods: {
			//验证手机号码
			isEmail(email) {
				let mPattern=/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;
				return mPattern.test(email);
			},
			back() {
				uni.navigateBack();
			},
			inputCode(e) {
				this.code = e.detail.value;
			},
			inputUserName: function(e) {
				this.username = e.detail.value;
			},
			inputPwd: function(e) {
				this.password = e.detail.value;
			},
			inputEmail: function(e) {
				this.email= e.detail.value;
			},
			clearInput(type) {
				if (type == 1) {
					this.username = '';
				} else if(type==2){
					this.password = '';
				}else{
					this.email='';
				}
			},
			protocol() {
				this.tui.href("/pages/doc/protocol/protocol")
			},
			async getCheckNum() {
				if (this.btnSendText > 0) {
					return;
				}
				// 验证邮箱合法性
				if (!this.isEmail(this.email)) {
					uni.showToast({
						title: '请输入正确的邮箱',
						icon: "none"
					});
					return;
				}
				// 请求服务器，发送验证码
				
				let code = await getCode({"email":this.email})
				if(code){
					this.$http.toast("验证码已发送");
				}
				this.isSend = true,
				// 发送成功，开启倒计时
				this.btnSendText = 60;
				let timer = setInterval(() => {
					this.btnSendText--;
					if (this.btnSendText < 1) {
						clearInterval(timer);
						this.btnSendText = '获取验证码';
						this.isSend = true
					}
				}, 1000);
			},
			async toRegister() {
				if (!this.isEmail(this.email)) {
					this.$http.toast("请输入正确的邮箱");
					return
				}
				console.log("begin");
				let data = await userRegister({
					username: this.username,
					code: this.code,
					password: this.password,
					email:this.email,
				})
				if (!data || (data && !("id" in data))) {
					let msg = data.error_msg
					if(msg && data.code===409){
						this.$http.toast("用户名或邮箱已存在");
					}else if(msg &&data.code===400){
						this.$http.toast("请填写完整信息");
					}else if(msg &&data.code===402){
						this.$http.toast("验证码输入错误");
					}
					return
				}
				uni.redirectTo({
					url: '../login/login'
				})
				return;
			},
		}
	};
</script>

<style lang="scss" scoped>
	.container {
		.tui-page-title {
			width: 100%;
			font-size: 48rpx;
			font-weight: bold;
			color: $uni-text-color;
			line-height: 42rpx;
			padding: 110rpx 40rpx 40rpx 40rpx;
			box-sizing: border-box;
		}
		.tui-header {
			width: 100%;
			padding: 40rpx;
			display: flex;
			align-items: center;
			justify-content: space-between;
			box-sizing: border-box;
		}
		.tui-form {
			padding-top: 50rpx;

			.tui-view-input {
				width: 100%;
				box-sizing: border-box;
				padding: 0 40rpx;

				.tui-cell-input {
					width: 100%;
					display: flex;
					align-items: center;
					padding-top: 48rpx;
					padding-bottom: $uni-spacing-col-base;

					input {
						flex: 1;
						padding-left: $uni-spacing-row-base;
					}

					.tui-icon-close {
						margin-left: auto;
					}

					.tui-btn-send {
						width: 156rpx;
						text-align: right;
						flex-shrink: 0;
						font-size: $uni-font-size-base;
						color: $uni-color-primary;
					}

					.tui-gray {
						color: $uni-text-color-placeholder;
					}
				}
			}

			.tui-cell-text {
				width: 100%;
				padding: 40rpx $uni-spacing-row-lg;
				box-sizing: border-box;
				font-size: $uni-font-size-sm;
				color: $uni-text-color-grey;
				display: flex;
				align-items: center;

				.tui-color-primary {
					color: $uni-color-primary;
					padding-left: $uni-spacing-row-sm;
				}
			}

			.tui-btn-box {
				width: 100%;
				padding: 0 $uni-spacing-row-lg;
				box-sizing: border-box;
				margin-top: 80rpx;
			}
		}
	}
</style>
