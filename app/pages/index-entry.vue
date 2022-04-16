<template>
	<view>
		<template v-if='type'>
			<EntIndex></EntIndex>
		</template>
		<template v-else>
			<NaiveIndex></NaiveIndex>
		</template>
	</view>
</template>

<script>
	import { mapState } from 'vuex'
	import NaiveIndex from '@/pages/index/index';
	import EntIndex from '@/pages/ent/index';
	export default {
		components: {
			NaiveIndex, EntIndex
		},
		mounted() {
			if (this.type)
				uni.setTabBarItem({index: 0, text: '需求'})
		},
		computed: {
			...mapState(['userInfo']),
			type() {
				const user = this.userInfo;
				if (user) {
					const type = user.user_type || 0;
					return type;
				}
				return 0;
			}
		}
	}
</script>
