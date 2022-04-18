import axios from '@/config/requestConfig.js';


export const updateUserInfo = async (data) => {
	let result = await axios.post("user/changeinfo",data)
	console.log(result)
	return result
}
export const getUserInfo = async () => {
	let result = await axios.get("user/info")
	return result
}
