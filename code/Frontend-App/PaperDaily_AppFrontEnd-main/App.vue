<script>
    import {mapMutations,mapActions} from 'vuex'
	import {
		tokenRefresh
	} from "@/api/login.js";
	import{
		picUrl
	} from '@/api/common.js'
	export default {
		async onLaunch() {
			// 网路监听（用户目前断网，切换wifi）
			this.lib.NetWork.On();
			let data;
			let chatList;
			try{
				 chatList =JSON.parse(uni.getStorageSync('chatList'))
				 if(!uni.getStorageSync("fuid")){
					 uni.setStorageSync('fuid',Math.random()+"")
				 }
				 	this.setChatList(chatList||[])
			}catch(e){
			
			}
			
			// 更新检测
		},
		async onShow () {
			console.log('App Show')
			let res ={};
			if(uni.getStorageSync('refresh_token')){
				res = await tokenRefresh()
			}
			if(res && res.code==401){
				uni.clearStorageSync('token')
				uni.clearStorageSync('chatList')
				this.setChatList([])
				this.setUserInfo({})
				this.$http.href("pages/login/login")
			}else{
				if(res&&res.access_token){
					uni.setStorageSync('token',res.access_token)
					res.userInfo.userpic=picUrl+res.userInfo.userpic
					this.setUserInfo(res.userInfo)
					//this.$store.dispatch('setSocketV',res.userInfo.id)
					this.$http.href("pages/home/home")
				}else{
					this.$http.href("pages/login/login")
				}		
			}
		},
		onHide: function () {
			console.log('App Hide')
		},
		methods:{
			...mapMutations(['setUserInfo','setChatList'])
					
		}
	}
</script>

<style>
	/*每个页面公共css */
	/* 引入官方css库 */

	@import './common/uni.css';
	/* 引入自定义图标库 */
	@import './common/icon.css';
	/* 引入自定义图标库 */
	@import './common/ssk.css';
	/* 引入动画库 */
	@import './common/animate.css';
	/* 公共样式 */
	@import './common/common.css';
</style>
