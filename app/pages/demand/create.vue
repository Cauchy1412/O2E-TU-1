<!-- This file is based on pages/add-input -->
<template>
	<view class="container">
		<tui-navigation-bar backgroundColor="255,255,255" :isFixed="false" :isOpcity="false">
			<view class="tui-content-box">
				<view class="tui-avatar-box" @tap="back">
					<tui-icon name="back" color="#FFE933" :size="64"></tui-icon>
				</view>
				<view class="tui-search-box">
					<view class="tui-search-text">发布需求</view>
				</view>
				<view class="tui-notice-box" @tap="submit">
					<text class="tui-add-text">发布</text>
				</view>
			</view>
		</tui-navigation-bar>

		<view class="select-topic-class">
			<view class="select-title" style='width: 100%'>
				<input
					placeholder='需求标题'
					v-model="demandData.title"
				>
				</input>
			</view>
			<view class="select-desc" @tap='demandData.title = ""'>
				<tui-icon name="shut"  :size="48"></tui-icon>
			</view>
		</view>

		<view v-if="selTitle.title" class="topic-tilte">
			#{{selTitle.title}}#
		</view>
		<view class="add-topic-text" style='height: 250px'>
			<textarea
				v-model='demandData.description'
				focus
				placeholder="需求描述"
				spellcheck="false"
			/>
		</view>
		
		<view class="example">
			<uni-forms :modelValue="formData">
				<uni-forms-item label='研发经费'>
					<uni-easyinput v-model="formData.fund" placeholder='可选' />
				</uni-forms-item>
				<uni-forms-item label='研发周期'>
					<uni-easyinput v-model="formData.period" placeholder='可选' />
				</uni-forms-item>
				<uni-forms-item label='研发地点'>
					<uni-easyinput v-model="formData.place" placeholder='可选' />
				</uni-forms-item>
			</uni-forms>
		</view>
	</view>
</template>

<script>
	import {mapState,mapMutations} from 'vuex'
	import {api} from '@/api'
	export default {
		data() {
			return {
				baseFormData: {},
				formData: {
					fund: '',
					period: '',
					place: ''
				},
				demandData: {
					title: '',
					description: ''
				},
				imageData: [],
				//上传地址
				text: '',
				top: 0, //标题图标距离顶部距离
				opcity: 0,
				scrollTop: 0.5,
				placeholder: 'sssxxx',
				titleClass:''
			}
		},
		computed:{
			...mapState(['userInfo', 'selTitle','category'])
		},
		methods: {
			...mapMutations(['delSelTitle','resetSelTitle', 'delCategory']),
			back() {
				uni.navigateBack();
			},
			async submit() {
				const { demandData, formData } = this;
				const title = demandData.title.trim();
				const description = demandData.description.trim();

				if (!title)
					return this.toast("请填写需求标题");

				if (!description)
					return this.toast("请填写需求描述");

				const resp = await api.post('demand/create', {
					title, description, meta: formData
				});
				if (!resp) {
					uni.navigateBack({
						complete() {
							setTimeout(() => {
								uni.showToast({
									title: '发布成功',
									icon: "success",
									duration: 1000
								});
							}, 100);
						}
					});
				}
				this.toast('发布失败');
			}
		}
	}
</script>

<style>
	page {
		background-color: #fff;

	}

	.container {
		padding: 0upx 0 120upx 0;
		box-sizing: border-box;
		position: relative;
	}

	.header {
		padding: 80upx 90upx 60upx 90upx;
		box-sizing: border-box;
	}

	.title {
		font-size: 34upx;
		color: #333;
		font-weight: 500;
	}

	.sub-title {
		font-size: 24upx;
		color: #7a7a7a;
		padding-top: 18upx;
	}

	.tui-box-upload {
		padding-left: 25upx;
		margin-bottom: 90upx;
		box-sizing: border-box;
	}

	.tui-title {
		width: 100%;
		padding: 50upx 30upx 30upx;
		box-sizing: border-box;
		font-weight: bold;
	}

	.tui-header-bg {
		width: 100%;
		margin: 0;
	}

	.tui-header-img {
		width: 100%;
		height: 440upx;
		display: block;
	}

	.tui-header-icon {
		width: 100%;
		position: fixed;
		top: 0;
		padding: 0 12upx;
		display: flex;
		align-items: center;
		height: 64upx;
		transform: translateZ(0);
		z-index: 99999;
		box-sizing: border-box;
	}

	.tui-content-box {
		width: 100%;
		height: 88upx;
		padding: 0 30upx;
		box-sizing: border-box;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.tui-avatar-box {
		width: 60upx;
		height: 60upx;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
	}

	.tui-avatar {
		width: 56upx;
		height: 56upx;
		border-radius: 50%;
	}

	.tui-search-box {
		height: 64upx;
		margin: 0 28upx;
		border-radius: 36upx;
		font-size: 36upx;
		padding: 0 24upx;
		box-sizing: border-box;
		color: #bfbfbf;
		display: flex;
		align-items: center;
		font-weight: 700;
		color: #000000;
	}

	.select-topic-class {
		height: 72upx;
		margin: 20upx 20upx;
		border-radius: 10upx;
		background-color: #f1f1f1;
		padding: 0 24upx;
		box-sizing:border-box;
		color: #bfbfbf;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.select-title {
		color: #000000;
		font-size: 34upx;
		font-weight: 700;
	}
	.select-desc {
		display: flex;
		align-items: center;
	}
	.add-topic-text{
		box-sizing: border-box;
		width: 100%;
		padding-top: 10upx;
		padding-left: 45upx;
	}
	.tui-bg-white {
		background-color: #ffffff !important;
	}

	.tui-search-text {
		padding-left: 10upx;
	}

	.tui-add-text {
		color: #000000;
		padding: 10upx 30upx;
		font-size: 28upx;
		box-sizing: border-box;
		font-weight: 700;
		border-radius: 40upx;
		background-color: #FFE933;
	}
	.topic-tilte{
		padding: 10upx 40upx;
		box-sizing: border-box;
		font-weight: 700;
		color:#5677fc;
	}
	.tui-notice-box {
		position: relative;
		flex-shrink: 0;
		font-size: 44upx;
		color: #fff;
	}
	
		.example {
			padding: 15px;
			background-color: #fff;
		}
	
		.segmented-control {
			margin-bottom: 15px;
		}
	
		.button-group {
			margin-top: 15px;
			display: flex;
			justify-content: space-around;
		}
	
		.form-item {
			display: flex;
			align-items: center;
		}
	
		.button {
			display: flex;
			align-items: center;
			height: 35px;
			margin-left: 10px;
		}
</style>
