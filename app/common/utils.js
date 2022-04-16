import Vue from 'vue';

Vue.prototype.formatDate = date => {
  return date.toLocaleString();
}

Vue.prototype.navigateToPage = path => {
	uni.navigateTo({url: '/pages/' + path});
}
