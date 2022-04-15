import axios from '@/config/requestConfig.js';
import time from '../common/time.js'
import {
	picUrl
} from './common.js'
export const saveUserAccess = async (data) => {
	//let result = await axios.post('user/access',data)
	return result
}

export const getUserInfo = async (data) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let result = await axios.get('user/profile',data,headers);
	return result
}

export const getTopicListByUid = async (id) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let result = []
	let topicList = await axios.get('post/'+id,{},headers);
	let ans=topicList.models
	if(ans&&ans.length){
		result = ans.map((item)=>{
			return{
				"createTime": time.gettime.gettime(item.created_at),
				"content": item.title,
				"id":item.id,
				"like_num":item.like_num,
				"favor_num":item.favor_num
			}
		})
	}
	console.log(result)
	return result
}

export const getTopicTitleByUid = async (id) => {
	let result = await axios.get('topic/title/user/'+id);
	return result
}