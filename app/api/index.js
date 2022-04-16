import axios from '@/config/requestConfig.js';
import time from '../common/time.js';

import {
	picUrl
} from './common.js'
export const  getTopicList =async () => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let result = await axios.get('recommend',{},headers)
	let index = 0
	if(result&&result.length){
		result = result.map((item)=>{
			index = index + 1
			return{
				"createTime": time.gettime.gettime(item.created_at),
				"content": item.title,
				"id":item.id,
				"userpic": picUrl+item.userpic,
				"username" : item.created_by.username,
				"index": index
			}
		})
	}
	return result
}

export const  getRecommendList =async () => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let result = await axios.get('Interpretation/popup',{},headers)
	if(result&&result.length){
		result = result.map((item)=>{
			return{
				"created_at": time.gettime.gettime(item.created_at),
				"content": item.content,
				"title":item.title,
				"isguanzhu":item.isguanzhu,
				"is_like":item.is_like,
				"is_favor":item.is_favor,
				"commentNum": item.commentNum,
				"like_num": item.like_num,
				"favor_num": item.favor_num,
				"id":item.id,
				"userpic": picUrl+item.userpic,
				"username" : item.created_by.username,
				"uid":item.uid,
				"tags":item.tags
			}
		})
	}
	return result
}

function getHeaders() {
	const token = uni.getStorageSync('token');
	if (!token)
		return {};
	return {
		"Authorization":'Bearer ' + token
	};
}

export const api = {
	get(path) {
		return axios.get(path, {}, getHeaders());
	},
	
	post(path, data) {
		return axios.post(path, data, getHeaders());
	}
};