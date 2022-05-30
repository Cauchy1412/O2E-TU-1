import Vue from 'vue';

Vue.prototype.formatDate = d => {
	function pad(x) {
		if (x < 10)
			return '0' + x;
		return x;
	}
	const date = new Date(d);
	// return date.toLocaleString('zh-CN');
	var seperator1 = "/";
	var seperator2 = ":";
	var month = date.getMonth() + 1;    
	var strDate = date.getDate();
	var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate + "  " +
		pad(date.getHours()) + seperator2 + pad(date.getMinutes()) + seperator2 + pad(date.getSeconds());    
	return currentdate;
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
