<template class="box-body">
	<view class="box">
		<view class="father-box">
			<view class="content" @tap="gotoTopicInfo">
				<text style="font-weight: bold;font-size:small;">				
				{{cardinfo.content.slice(0,20)}}
				</text>
			</view>
			
			<view class="u-f-ac u-f-jsb">
				<view class="time" >
						{{cardinfo.createTime}}
				</view>
				<view class="active-comm">
					<tui-icon name="star" :color="''"></tui-icon>
					<text class="active-text">{{cardinfo.favor_num}}</text>
				</view>
				<view class="active-comm">
					<tui-icon name="agree" :color="''"></tui-icon>
					<text class="active-text">{{cardinfo.like_num}}</text>
				</view>
				
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
			userpic:Object,
			index:Number,
		},
		data() {
			return {

			};
		},
		methods:{
			gotoTopicInfo(){
				this.$emit("gotoTopic",this.index)
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
		height: 90upx;
		width: 90upx;
		border-radius: 90upx;
		border: 1px solid #007AFF;
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
		margin-left: 70upx;
		color: #808080;
	}



	.content {
		display: block;
		font-size: 14px;
		color: #24292E;
		font-style: italic;
		margin-left: 20upx;
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
