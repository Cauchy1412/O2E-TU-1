<template>
	<view>
		<textarea class="user-set-brief" 
				  :value="brief" 
				  placeholder="编辑您的简介信息"
				  type="text"
				  maxlength="120"
				  :auto-height="false"
				  @input="decrease"/>
		<view class="user-line"></view>		  
		<view>{{leftlength}}</view>
		
	</view>
</template>

<script>
	export default {
		data() {
			return {
				brief:"",
				maxlength:120,
				leftlength:120,
			}
		},
		methods: {
			decrease: function(e) {
				this.leftlength = this.maxlength - e.detail.value.length;
			}
		}
	}
</script>

<style>
.user-line{
	height: 1px;
	width: inherit;
	background-color: #000000;
}
.user-set-brief{
	font-size: 24upx;
	margin-left: 45upx;
	height: 300upx;
}
</style>
