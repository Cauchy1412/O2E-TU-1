<template class="box-body">
	<view class="box">
		<view class="father-box">
			<view class="content" @tap="openDetail">
				<text style="font-weight: bolder;font-size:x-large;color: #3F536E;">
				{{cardinfo.index+"		"}}
				</text>
				<text style="font-weight: 650;font-size:medium;">				
				{{cardinfo.content.slice(0,20)}}
				</text>
			</view>
			
			<view class="header" @tap="openDetail">
				<image class="img" :src="cardinfo.userpic"></image>
				<view class="auth">
				<text style="font-weight: 300;font-size:small;">{{cardinfo.username}}</text>
				</view>
				<view class="time">{{cardinfo.createTime}}</view>
			</view>
			
		</view>
	</view>
</template>

<script>
	export default {
		name: 'card',
		props: {
			cardinfo: {
				type: Object
			},
			index:Number
		},
		data() {
			return {

			};
		},
		methods:{
			openDetail(){
				this.$emit("opendDetail",this.cardinfo)
			}
		}
	}
</script>

<style>
	
	.low{
		margin-left: 0upx;
	}

	.father-box {
		background-color: #FFFFFF;
		box-shadow: #C8C7CC;
		min-height: 150upx;
		margin: 20upx 0;
		border-radius: 20upx;
	}

	.img {
		margin: 20upx 0px 20upx 50upx;
		height: 70upx;
		width: 70upx;
		border-radius: 70upx;
		border: 1px solid #ffffff;
		display: inline-flex;
	}

	.auth {
		font-weight: bolder;
		font-family: Arial, Helvetica, sans-serif;
		font-size: 15px;
		margin-top: -100upx;
		margin-left: 170upx;
	}

	.time {
		font-family: Arial, Helvetica, sans-serif;
		font-size: 12px;
		display: inline-flex;
		margin-left: 170upx;
		margin-top: -20upx;
		color: #808080;
	}



	.content {
		display: block;
		font-size: 14px;
		color: #24292E;
		font-style: italic;
		margin-left: 0upx;
		margin-right: 60upx;
		margin-top: 20upx;
		height: 70upx;
		text-indent: 1.5em;
	}

	.nbsp {
		margin-left: 25upx;
	}

	.icon-like {
		height: 32upx;
		width: 32upx;
	}



	.good view {
		font-size: 12px;
		margin-left: 20upx;
		color: #6D6D72;
		margin-top: -2upx;
		text-align: center;
	}



	.show {
		color: #0081FF;
		margin-top: 12upx;
	}
	
	.active-comm{
		display: flex;
		align-items: center;
		margin-right: 20upx;
		color: #666666;
	}
</style>
