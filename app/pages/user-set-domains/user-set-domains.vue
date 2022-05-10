<template>
	<view class="body">
		<tui-list-view backgroundColor="#777">
			<tui-list-cell :hover="false" v-for="(value, index) in cur_domains" :key="index">
				<!--clicktype不为空则需要跳转-->
				<view class="user-set-list-item">
					<text class="user-set-list-item-info">{{value}}</text> 
					<view>
						<text style="color: #007AFF;" @tap="delete_domain(index)">删除</text>
					</view>
				</view>
			</tui-list-cell>			
		</tui-list-view>
		<tui-list-cell>
			<view class="user-set-list-item" @tap="showsheet">
				<text style="color: #007AFF;">+ 添加研究领域</text>
			</view>
		</tui-list-cell>
		<button class="user-set-btn"
		type="primary" @tap="submit">保存</button>
		<view :hidden="sheethidden" class="popup_content">
			<view class="popup_title">添加新的研究领域</view>
			<view class="popup_text">
				<input placeholder='内容不超过10个字符' maxlength="10" v-model="new_domain"/>
				<view @click="add_domain">
					<button class="popup_button">确认</button>
				</view>
			</view>
		</view>
		<view class="popup_overlay" :hidden="sheethidden" @click="hidesheet"></view>
	</view>
</template>

<script>
	import {mapState, mapMutations} from 'vuex'
	import {updateUserInfo} from '@/api/user-set-userinfo.js'
	export default {
		data() {
			return {
				cur_domains:[],
				new_domain:"",
				sheethidden:true,
			}
		},
		computed: {
			...mapState(['userInfo'])
		},
		mounted() {
			this.cur_domains = JSON.parse(JSON.stringify(this.userInfo.meta))['domains']	//深拷贝
			console.log(this.cur_domains)
		},
		methods: {
			...mapMutations(['setUserInfo']),
			delete_domain(index){
				let value = this.cur_domains[index]
				this.cur_domains.splice(index,1)
				uni.showToast({
					title:"已删除：" + value,
					icon:'none',
				})
			},
			add_domain(){
				let domain = this.new_domain
				this.cur_domains.push(this.new_domain)
				this.new_domain = ""
				uni.showToast({
					title:"添加成功！",
				})
				this.sheethidden = true;
			},
			showsheet(){
				this.sheethidden = false;
			},
			hidesheet(){
				this.sheethidden = true;
			},
			async submit(){
				let new_user = JSON.parse(JSON.stringify(this.userInfo))
				new_user.meta['domains'] = this.cur_domains
				let data = {meta: new_user.meta}
				console.log(data)
				let res = await updateUserInfo(data)
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
.user-set-list-item {
	display: flex;
	justify-content: space-between;
}

.user-set-list-item-info{
	text-align: right;
	margin-right: 30upx;
	color: #9B9B9B;
}

.popup_overlay {
	position: fixed;
	top: 0%;
	left: 0%;
	width: 100%;
	height: 100%;
	background-color: black;
	z-index: 1001;
	-moz-opacity: 0.8;
	opacity: .80;
	filter: alpha(opacity=88);
}
.popup_content {
	position: fixed;
	left: 15%;
	width: auto;
	height: auto;
	align-items: center;
	
	border: 10px solid white;
	background-color: white;
	z-index: 1002;
	overflow: auto;
	border-radius: 20upx;	
}
.popup_title {
	padding-top: 20upx;
	width: 480upx;
	text-align: center;
	font-size: 32upx;
}
.popup_text {
	padding-top: 5upx;
	margin-top: 30upx;
	margin-left: 20upx;
}
.popup_button {
	color: white;
	background-color: #4399FC;
	border-radius: 20upx;
	margin-top: 200upx;
}
</style>
