<template class="box-body">
	<view class="box">
		<view class="father-box">
			<view class="demand-row">
				<view>
					{{title}}
				</view>
				<view style='color: #6c6c6c'>
					{{formatDate(demand.created_at)}}
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		name: 'demand-row',
		props: {
			demand: {
				title: String,
				description: String,
				created_at: String | Date
			},
			show_company: Boolean
		},
		computed: {
			title() {
				let res = this.demand.title;
				if (this.show_company) {
					const ent = this.demand.company_meta?.name;
					if (ent)
						res += ' (' + ent + ')';
				}
				return res;
			}
		},
		methods: {
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
		min-height: 70upx;
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

	.demand-row {
		display: block;
		font-size: 14px;
		color: #24292E;
		height: 120upx;
		text-indent: 1.5em;
		padding-top: 20upx;
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
