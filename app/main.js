import Vue from 'vue'
import App from './App'
import store from './store/store.js'
Vue.config.productionTip = false
//#ifdef H5 
// import './monitor/index.js'
//#endif
// 挂载全局方法
import $http from './config/requestConfig.js';
Vue.prototype.$http = $http;
import lib from "./common/lib.js"
Vue.prototype.lib=lib
Vue.prototype.$store = store
App.mpType = 'app'

import '@/common/utils.js';
Vue.prototype.toast = Vue.prototype.$http.toast;


const app = new Vue({
    ...App,
	store,
	lib,
})
app.$mount()
