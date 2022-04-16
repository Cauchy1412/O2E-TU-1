import axios from '@/config/requestConfig.js';

import {
	picUrl
} from './common.js'

export const getTopicCollect = async (page=1,data) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let temp = await axios.get("favorites/page/"+page,data,headers)
	let result=temp.page
	if(result&&result.length){
		result.forEach((item)=>{
			item.userpic=picUrl+item.userpic
		})
	}
	// if (result && result.length) {
	// 	result.reverse()
	// } else {
	// 	result = []
	// }
	console.log(result)
	return result
}

export const deleteCollect = async (id) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	axios.setLoading(false);
	let result = await axios.delete('Interpretation/collect', {
		ids: [id]
	}, headers);
	axios.setLoading(true);
	return result
}

export const createCollect = async (data) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let result = await axios.delete('Interpretation/collect', data , headers);
	return result
}
