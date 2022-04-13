import axios from '@/config/requestConfig.js';
export const  getUserProfile =async () => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let data = await axios.get('user/profile',{},headers)
	return data
}

// export const  giveLike = async (data) => {
// 	let result = await axios.post('topic/active',data);
// 	return result
// }
