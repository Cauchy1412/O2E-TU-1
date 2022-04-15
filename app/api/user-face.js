import axios from '@/config/requestConfig.js';
import {
	headers
} from './common.js'


export const  uploudFile = async (file) => {
	const h = { "Content-Type": "multipart/form-data"} 
	let url = await axios.post("user/icon",file)
	return url
}
