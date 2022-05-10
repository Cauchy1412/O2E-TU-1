import axios from '@/config/requestConfig.js';


export const updateUserInfo = async (data) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let result = await axios.post("user/update-user-info",data,headers)
	//console.log(result)
	return result
}
export const getUserInfo = async () => {
	let result = await axios.get("user/info")
	return result
}
