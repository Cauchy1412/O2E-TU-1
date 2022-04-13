import axios from '@/config/requestConfig.js';



export const userRegister = async (data) => {
	console.log("test");
	let result = await axios.put('user/create',data)
	return result
}

export const getCode = async (data) => {
	axios.setLoading(true);
	let result = await axios.post('user/create',data)
	axios.setLoading(false);
	return result
}
