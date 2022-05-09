<template>
	<view>
		<tui-list-view title="个人信息" color="#777">
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
	</view>
</template>

<script>
	import {mapState, mapMutations} from 'vuex'
	export default {
		data() {
			return {
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
					{ name:"注册地",clicktype:"",datatype:"place"},
					{ name:"注册号",clicktype:"",datatype:"regisnumber"},
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
			clickevent(type){
				switch(type){
					case "edit_domain":
						uni.showToast({
							title: '芜湖！',
						});
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
			deepcopy(meta){		//深拷贝
				return JSON.parse(JSON.stringify(meta))
			}
		}
	}
</script>

<style>

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
