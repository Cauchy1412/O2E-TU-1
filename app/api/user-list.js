import axios from '@/config/requestConfig.js';

import {
	picUrl
} from './common.js'

export const getUserAttList = async (data) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let result = []
	console.log(data)
	axios.setLoading(false)
	let attData = await axios.get("follower/roll/"+data,{},headers)
	axios.setLoading(true)
	
	if(attData&&attData.length){
			result = attData.map((item)=>{
				return	{
						id:item.id,
						userpic:picUrl+item.userpic,
						username:item.username,
						isguanzhu:true
				}
			})
		
	}
	return result
}

export const getUserFansList = async (uid,eachData) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let result = []
	axios.setLoading(false)
	let fansData = await axios.get("fan/roll/"+uid,{},headers)
	axios.setLoading(true)
	
	if(fansData&&fansData.length){
		result = fansData.map((item)=>{
			let isguanzhu = false;
			if(eachData&&eachData.length){
				isguanzhu = eachData.some((eItem)=>{
					return item.id == eItem.id
				})
			}
			return	{
					id:item.id,
					userpic:picUrl+item.userpic,
					username:item.username,
					isguanzhu:item.isguanzhu
			}
		})
	}
	return result
}
export const getUserEachList = async (uid) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let result = []
	axios.setLoading(false)
	let eachData = await axios.get("friend/roll/"+uid,{},headers)
	axios.setLoading(true)
	if(eachData&&eachData.length){
		result = eachData.map((item)=>{
			return	{
					id:item.id,
					userpic:picUrl+item.userpic,
					username:item.username,
					isguanzhu:true
			}
		})
	}
	return result
}

function precessUserData(item){
	return {
		
	}
}