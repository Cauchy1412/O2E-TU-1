import axios from '@/config/requestConfig.js';

//const API_HOST = '114.116.221.131:10516';
const API_HOST = 'localhost:8000';

// export const baseUrl=process.env.NODE_ENV === 'development'?"http://localhost:8000/api/":"http://api.hfb.xquery.cn/api/";
// export const socketBaseUrl=process.env.NODE_ENV === 'development'?"ws://localhost:8000/api/":"ws://api.hfb.xquery.cn/api/";

export const baseUrl = `http://${API_HOST}/api/`;
export const socketBaseUrl = `ws://${API_HOST}/api/`;
export const picUrl = baseUrl;

//可以new多个request来支持多个域名请求
//点赞功能
export const  giveLike = async (id) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let result = await axios.post('Interpretation/'+id+'/like',{},headers);
	return result
}
