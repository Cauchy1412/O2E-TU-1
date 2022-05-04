<template>
	<view class="container">
		<tui-navigation-bar backgroundColor="255,255,255" :isFixed="false" :isOpcity="false">
			<view class="tui-content-box">
				<view class="tui-avatar-box" @tap="back">
					<tui-icon name="back" color="#FFE933" :size="64"></tui-icon>
				</view>
				<view class="tui-search-box">
					<view class="tui-search-text">专家列表</view>
				</view>
				<view class="tui-notice-box">
				</view>
			</view>
		</tui-navigation-bar>
		<uni-card :is-shadow="false" @tap="goDetail(item)" v-for="(item,index) in expertsList" :key="index">
			<view class="demand-info">
				<view class="demand-info-item">
					<view class="text-cut"> {{item.name}}</view>
					<view>性别: {{item.sex}}</view>
					<view>职称: {{item.title}}</view>
					<view>研究领域: {{item.field}}</view>
				</view>
			</view>
		</uni-card>
	</view>
</template>

<script>
	import { api } from '@/api';
	export default {
		onLoad(data) {
			this.demandId = data.id
		},
		mounted() {
			this.requestData()
		},
		data() {
			return {
				demandId: '',
				expertsList: [{
						id: '111',
						img: 'https://img-blog.csdnimg.cn/2020062923175961.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NnMTI5MDU0MDM2,size_16,color_FFFFFF,t_70',
						name: 'Sebastian Thrun',
						sex: '男',
						title: '谷歌无人车之父',
						field: '人工智能，无人驾驶',
						info: '我是计算机科学教授，领导着自主视觉小组(AVG)。我的小组是Tübingen大学和位于德国网络谷中心Tübingen的智能系统MPI的一部分。我是Tübingen大学计算机科学系的副系主任，是卓越集群“ML in science”和CRC“Robust Vision”的PI。我也是ELLIS的研究员、董事会成员和ELLIS博士项目的协调员。我的研究小组正在开发用于计算机视觉、自然语言和机器人的机器学习模型，应用于自动驾驶、VR/AR和科学文献分析。'
					},
					{
						id: '112',
						img: 'http://www.cvlibs.net/site/andreas_geiger.jpg',
						name: 'Andreas Geiger',
						sex: '男',
						title: 'KITTI数据集作者之一',
						field: '人工智能，无人驾驶',
						info: '我领导着一个由专业计算机科学家组成的团队，他们的唯一目标是通过人工智能技术显著地帮助社会，并一直在寻找具有重大影响的项目。我们致力于机器人、自动驾驶汽车、自动化家庭、医疗保健、无人机和其他一些应用。我们目前专注于三个领域:用于医疗保健的人工智能、用于人类预测的人工智能和智能家居。'
					},
				],

			}
		},
		methods: {
			back() {
				uni.navigateBack()
			},
			goDetail(item) {
				uni.navigateTo({
					url: '/pages/expert-info/expert-info?id=' + item.id + '&demandId=' + this.demandId + '&img=' + item.img + '&name=' + item.name + '&sex=' + item.sex + '&title=' + item.title + '&field=' + item.field + '&info=' + item.info
				})
			},
			async requestData() {
				const res = await api.get('resovle/recommend?id=' + this.demandId);
				this.expertsList = res.datalist.map(o => ({
					...o,
				}));
			},
		}
	}
</script>

<style>
	.container {
		padding: 0upx 0 120upx 0;
		box-sizing: border-box;
		position: relative;
	}

	.header {
		padding: 80upx 90upx 60upx 90upx;
		box-sizing: border-box;
	}

	.box {
		margin: 20upx 0;
		width: 100%;
		position: fixed;
		bottom: -16px;

		.margin-bottom-xl {
			margin-bottom: 20rpx;
		}
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
	}

	.tui-search-box {
		height: 55upx;
		align-items: center;
		font-weight: 700;
		color: #000000;
	}

	.tui-notice-box {
		width: 60upx;
	}

	.demand-info {
		padding: 0 30upx;
	}

	.demand-info-item {
		padding: 20upx 0;
		border-bottom: 1upx solid #EEEEEE;
	}

	.demand-info-item>view {
		color: #AAAAAA;
		font-size: 16upx;
	}

	.demand-info-item>view:first-child {
		color: #333333;
		font-size: 20upx;
		padding: 15upx 0;
	}
</style>
