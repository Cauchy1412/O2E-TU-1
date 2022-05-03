<template>
	<view class="container">
		<view class="tui-status-bar"></view>
		<view class="tui-header">
			<!-- <view>ThorUI组件库</view> -->
			<tui-icon name="shut" :size="52" @click="back"></tui-icon>
		</view>
		<!--<view class="tui-page-title">注册</view>-->
		<swiper-tab-head :tabBars="tabBars" :tabIndex="tabIndex" @tabtap="tabtap">
		</swiper-tab-head>
		<view class="tui-form">
			<view class="tui-view-input">
				<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
					<view class="tui-cell-input">
						<tui-icon name="people" color="#6d7a87" :size="40"></tui-icon>
						<input :value="username" placeholder="请输入用户名" placeholder-class="tui-phcolor" type="text" maxlength="15" @input="inputUserName" />
						<view class="tui-icon-close" v-show="username" @tap="clearInput(0, 'username')">
							<tui-icon name="close-fill" :size="32" color="#bfbfbf"></tui-icon>
						</view>
					</view>
				</tui-list-cell>
				<!--仅专家注册可见-->	
				<view class="tui-view-input-expert" v-if="(tabIndex===0)">
					<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
						<view class="tui-cell-input">
							<tui-icon name="people" color="#6d7a87" :size="40"></tui-icon>
							<input :value="expertData.name" placeholder="真实姓名" placeholder-class="tui-phcolor" type="text" maxlength="15" @input="inputName" />
							<view class="tui-icon-close" v-show="expertData.name" @tap="clearInput(1, 'name')">
								<tui-icon name="close-fill" :size="32" color="#bfbfbf"></tui-icon>
							</view>
						</view>
					</tui-list-cell>
					<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
						<view class="tui-cell-input">
							<tui-icon name="people" color="#6d7a87" :size="40"></tui-icon>
							<input :value="expertData.gender" placeholder="性别" placeholder-class="tui-phcolor" type="text" maxlength="15" @input="inputGender" />
							<view class="tui-icon-close" v-show="expertData.gender" @tap="clearInput(1, 'gender')">
								<tui-icon name="close-fill" :size="32" color="#bfbfbf"></tui-icon>
							</view>
						</view>
					</tui-list-cell>
					<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
						<view class="tui-cell-input">
							<tui-icon name="listview" color="#6d7a87" :size="40"></tui-icon>
							<input :value="expertData.professor" placeholder="职称" placeholder-class="tui-phcolor" type="text" maxlength="15" @input="inputProfessor" />
							<view class="tui-icon-close" v-show="expertData.professor" @tap="clearInput(1, 'professor')">
								<tui-icon name="close-fill" :size="32" color="#bfbfbf"></tui-icon>
							</view>
						</view>
					</tui-list-cell>
					<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
						<view class="tui-cell-input">
							<tui-icon name="histogram" color="#6d7a87" :size="40"></tui-icon>
							<input :value="domain_str" placeholder="研究领域,多个研究领域用中文逗号分隔" placeholder-class="tui-phcolor" type="text" maxlength="36" @input="inputField" />
							<view class="tui-icon-close" v-show="domain_str" @tap="clearInput(0, 'filed_str')">
								<tui-icon name="close-fill" :size="32" color="#bfbfbf"></tui-icon>
							</view>
						</view>
					</tui-list-cell>
				</view>
				<!--仅企业注册可见-->				
				<view class="tui-view-input-enterprise" v-if="(tabIndex===1)">
					<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
						<view class="tui-cell-input">
							<tui-icon name="home" color="#6d7a87" :size="40"></tui-icon>
							<input :value="businessData.name" placeholder="企业名" placeholder-class="tui-phcolor" type="text" maxlength="36" @input="inputBusinessName" />
							<view class="tui-icon-close" v-show="businessData.name" @tap="clearInput(2, 'name')">
								<tui-icon name="close-fill" :size="32" color="#bfbfbf"></tui-icon>
							</view>
						</view>
					</tui-list-cell>
					<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
						<view class="tui-cell-input">
							<tui-icon name="home" color="#6d7a87" :size="40"></tui-icon>
							<input :value="businessData.business_type" placeholder="公司类型" placeholder-class="tui-phcolor" type="text" maxlength="15" @input="inputBusinessType" />
							<view class="tui-icon-close" v-show="businessData.business_type" @tap="clearInput(2, 'business_type')">
								<tui-icon name="close-fill" :size="32" color="#bfbfbf"></tui-icon>
							</view>
						</view>
					</tui-list-cell>
					<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
						<view class="tui-cell-input">
							<tui-icon name="location" color="#6d7a87" :size="40"></tui-icon>
							<input :value="businessData.place" placeholder="注册地" placeholder-class="tui-phcolor" type="text" maxlength="36" @input="inputRegisPlace" />
							<view class="tui-icon-close" v-show="businessData.place" @tap="clearInput(2, 'place')">
								<tui-icon name="close-fill" :size="32" color="#bfbfbf"></tui-icon>
							</view>
						</view>
					</tui-list-cell>
					<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
						<view class="tui-cell-input">
							<tui-icon name="house" color="#6d7a87" :size="40"></tui-icon>
							<input :value="businessData.regisnumber" placeholder="注册号" placeholder-class="tui-phcolor" type="text" maxlength="36" @input="inputRegisNumber" />
							<view class="tui-icon-close" v-show="businessData.regisnumber" @tap="clearInput(2, 'regisnumber')">
								<tui-icon name="close-fill" :size="32" color="#bfbfbf"></tui-icon>
							</view>
						</view>
					</tui-list-cell>
					<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
						<view class="tui-cell-input">
							<tui-icon name="people" color="#6d7a87" :size="40"></tui-icon>
							<input :value="businessData.legalperson" placeholder="法定代表人" placeholder-class="tui-phcolor" type="text" maxlength="15" @input="inputLegalPerson" />
							<view class="tui-icon-close" v-show="businessData.legalperson" @tap="clearInput(2, 'legalperson')">
								<tui-icon name="close-fill" :size="32" color="#bfbfbf"></tui-icon>
							</view>
						</view>
					</tui-list-cell>
				</view>
				
				<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
					<view class="tui-cell-input">
						<tui-icon name="pwd" color="#6d7a87" :size="40"></tui-icon>
						<input :value="password" placeholder="请输入密码" :password="true" placeholder-class="tui-phcolor" type="text"
						 maxlength="15" @input="inputPwd" />
						<view class="tui-icon-close" v-show="password" @tap="clearInput(0,'password')">
							<tui-icon name="close-fill" :size="32" color="#bfbfbf"></tui-icon>
						</view>
					</view>
				</tui-list-cell>
				<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
					<view class="tui-cell-input">
						<tui-icon name="mail" color="#6d7a87" :size="40"></tui-icon>
						<input :value="email" placeholder="邮箱" placeholder-class="tui-phcolor" type="text"
						 maxlength="36" @input="inputEmail" />
						<view class="tui-icon-close" v-show="email" @tap="clearInput(2,'email')">
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
	import swiperTabHead from "../../components/index/swiper-tab-head.vue";
	
	export default {
		components: {
			swiperTabHead,
		},
		computed: {
			disabled: function() {
				let bool = true;
				if (this.username && this.code && this.password) {
					bool = false;
				}
				return bool;
			},
			jobValue: function() {
				if (this.tabIndex === 0) {
					return 0;
				} else if (this.tabIndex === 1) {
					return 2;
				}
				return -1;
			}
		},
		data() {
			return {
				username: '',
				password: '',
				code: '',
				email:'',
				isSend: false,
				btnSendText: '获取验证码' ,//倒计时格式：(60秒)
				domain_str:'',
				expertData: {
					name:'',				//真实姓名
					gender:'',				
					professor:'',			//职称
					domains:[],
				},
				businessData: {
					name:'',
					business_type:'',		//公司类型
					place:'',				//注册地
					regisnumber:'',			//注册号
					legalperson:'',			//法定代表人
				},
				tabIndex: 0,
				tabBars: [{
						name: "专家注册",
						id: "experiment",
						page: 1
					},
					{
						name: "企业注册",
						id: "enterprise",
						page: 1
					},
				],
			};
		},
		methods: {
			// tabbar点击事件
			tabtap(index) {
				this.tabIndex = index;
			},
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
			inputName: function(e) {
				this.expertData.name = e.detail.value;
			},
			inputGender: function(e) {
				this.expertData.gender = e.detail.value;
			},
			inputProfessor: function(e) {
				this.expertData.professor = e.detail.value;
			},
			inputField: function(e) {
				this.domain_str = e.detail.value;
			},
			inputBusinessName: function(e) {
				this.businessData.name = e.detail.value;
			},
			inputBusinessType: function(e) {
				this.businessData.business_type = e.detail.value;
			},
			inputRegisPlace: function(e) {
				this.businessData.place = e.detail.value;
			},
			inputRegisNumber: function(e) {
				this.businessData.regisnumber = e.detail.value;
			},
			inputLegalPerson: function(e) {
				this.businessData.legalperson = e.detail.value;
			},
			clearInput(type, ele) {
				if (type == 1) {
					this.expertData[ele] = '';
				} else if(type == 2){
					this.businessData[ele] = '';
				}else{
					this[ele]='';
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
				if (this.tabIndex == 0) {
					this.expertData.domains = this.domain_str.split('，')
					
					console.log("domain: " + this.expertData.domains)
				}
				let formData = (this.tabIndex == 0)?this.expertData:this.businessData;
				let data = await userRegister({
					username: this.username,
					code: this.code,
					password: this.password,
					email: this.email,
					user_type: this.jobValue,
					verified_type: 0,		//默认为0，未认证状态
					meta: formData,
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
					padding-top: 36rpx;
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
