import Vue from 'vue';

Vue.prototype.formatDate = date => {
  return new Date(date).toLocaleString('zh-CN');
}

Vue.prototype.navigateToPage = path => {
	uni.navigateTo({url: '/pages/' + path});
}

Vue.prototype.isEnterprise = function () {
	return this.$store.state.userInfo.user_type;
}

Vue.prototype.getCurrentUser = function() {
	return this.$store.state.userInfo;
}
