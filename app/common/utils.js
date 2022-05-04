import Vue from 'vue';

Vue.prototype.formatDate = date => {
  return new Date(date).toLocaleString('zh-CN');
}

Vue.prototype.navigateToPage = path => {
	uni.navigateTo({url: '/pages/' + path});
}
