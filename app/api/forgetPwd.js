import axios from '@/config/requestConfig.js';
import {
	headerForm
} from './common.js'
export const sendForgetCode = async (data) => {
	let result = await axios.post('user/forget-password',data)
	return result
}

export const forgetPwd = async (data) => {
	let result = await axios.put('user/forget-password',data);
	return result
}
