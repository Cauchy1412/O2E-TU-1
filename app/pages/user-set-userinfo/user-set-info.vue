<template>
	<view class="body">
		<!--<tui-image-cropper
			v-if="cropper" @cropper="sucessCropper"
			 :imageUrl="headimg" :height="height" :width="height"></tui-image-cropper>-->
		<tui-list-view color="#777">
			<tui-list-cell :arrow="true">
				<view class="user-set-list-item" @tap="edit_icon">
					<view style="margin-top: 20upx;">头像</view>
					<view>
						<image class="user-set-head-img" :src="userInfo.userpic" mode="aspectFill" lazy-load></image>
					</view>
				</view>
			</tui-list-cell>
			<tui-list-cell :arrow="true" v-if="userInfo.user_type == 0">
				<view class="user-set-list-item" >
					<view style="margin-top: 20upx;">真实照片</view>
				</view>
			</tui-list-cell>
			<tui-list-cell :hover="!item.clicktype.length==0" :arrow="true" v-for="(item, index) in list" :key="index">
				<!--clicktype不为空则需要跳转-->
				<view class="user-set-list-item" @tap="clickevent(item.clicktype)">
					<view>{{item.name}}</view>
					<input class="user-set-list-item-info" :disabled="!item.clicktype.length==0" v-model="meta_info[item.datatype]"/> 
				</view>
			</tui-list-cell>
			<tui-list-cell :arrow="true">
				<view class="user-set-list-item" @tap="edit_brief">用户简介</view>
			</tui-list-cell>
		</tui-list-view>
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
				userpic:"",
				list:[],
				scholarlist:[
					// { icon:"",name:"账号与安全",clicktype:"navigateTo",url:"../../pages/user-set-repassword/user-set-repassword" },
					{ name:"真实姓名",clicktype:"",datatype:"name"},
					{ name:"性别",clicktype:"",datatype:"gender"},
					{ name:"职称",clicktype:"",datatype:"professor"},
					{ name:"研究领域",clicktype:"edit_domain",datatype:""},
				],
				companylist:[
					{ name:"企业名",clicktype:"",datatype:"name"},
					{ name:"企业类型",clicktype:"",datatype:"business_type"},
					// { name:"注册地",clicktype:"",datatype:"place"},
					// { name:"注册号",clicktype:"",datatype:"regisnumber"},
					{ name:"法定代表人",clicktype:"",datatype:"legalperson"},
				],
				meta_info:{
					name:"芜湖航空",			//default,显示这个说明没有按照正常流程进入页面
					gender:"",
					professor:"",
					domains:[],
					business_type:"",
					place:"",
					regisnumber:"",
					legalperson:""
				},
				// account_info:{},
			}
		},
		computed: {
			...mapState(['userInfo'])
		},
		mounted() {
			console.log(this.userInfo)
			if(this.userInfo.id){		//验证用户存在
				if(this.userInfo.user_type == 0) {	//区分用户类型，浅拷贝
					this.list = this.scholarlist	
				}else if(this.userInfo.user_type == 2) {
					this.list = this.companylist
				}
				this.meta_info = this.deepcopy(this.userInfo.meta)
			}
		},
		methods: {
			...mapMutations(['setUserInfo']),
			clickevent(type){
				switch(type){
					case "edit_domain":
						uni.navigateTo({
							url:"../user-set-domains/user-set-domains"
						})
						break;
					default:;	
				}
			},
			editname(){
				uni.showToast({
					title: '芜湖！',
				});
			},
			edit_brief(){
				uni.navigateTo({
					url:'../user-set-brief/user-set-brief'
				})
			},
			edit_icon(){
				uni.chooseImage({
					count:1,
					sizeType:['compressed'],
					success: (res) => {
						uni.navigateTo({	//复用原有组件
							url:'../user-face/user-face?tempFilePath='+res.tempFiles[0].path
						})
					}
				})	
			},
			async submit(){
				let new_user = this.deepcopy(this.userInfo)
				if(this.userInfo.user_type == 0) {	
					//此页面不修改domains
					new_user.meta['name'] = this.meta_info['name']
					new_user.meta['gender'] = this.meta_info['gender']
					new_user.meta['professor'] = this.meta_info['professor']
				}else if(this.userInfo.user_type == 2) {
					new_user.meta['name'] = this.meta_info['name']
					new_user.meta['business_type'] = this.meta_info['business_type']
					new_user.meta['legalperson'] = this.meta_info['legalperson']
				}
				let data = {meta: new_user.meta}
				console.log(data)
				let res = await updateUserInfo(data)
				if (!res.result) {
					this.$http.toast("修改失败");
				} else {
					this.setUserInfo(new_user)
					this.$http.toast("修改成功");
				}
			},
			deepcopy(meta){		//深拷贝
				return JSON.parse(JSON.stringify(meta))
			}
		}
	}
</script>

<style>
@import "../../common/form.css";	
.user-set-head-img{
	width: 90upx;
	height: 90upx;
	border-radius: 100%;
}
.user-set-list-item {
	display: flex;
	justify-content: space-between;
}

.user-set-list-item-info{
	text-align: right;
	margin-right: 30upx;
	color: #9B9B9B;
}
</style>
