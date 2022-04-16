import axios from '@/config/requestConfig.js';
import time from '../common/time.js'
import {
	picUrl
} from './common.js'



export const pushMessage = async (data) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	axios.setLoading(false);
	console.log(data)
	let result = await axios.post("chat/push",data,headers)
	axios.setLoading(true);
	return result
}

export const createChat = async (data) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let result = await axios.post('chat/create',data,headers)
	return result
}


export const getChat = async (id,userInfo) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let item = await axios.get('chat/'+id,{},headers)
	let result= {}
	if (item) {
			let fid = userInfo.id == item.from_user_id ? item.to_user_id : item.from_user_id
			let sendTime = time.gettime.gettime(new Date())
			let message = ''
			let msgList = item.message_list
			result = {
				id: item.chatroom_id,
				fid: fid,
				fromId: item.from_user_id,
				toId: item.to_user_id,
				afterTime: +new Date(item.afterTime),
				userpic: item.from_user_id==userInfo.id?picUrl+item.to_user_pic:picUrl+item.from_user_pic,
				username: item.from_user_id==userInfo.id?item.to_user_name:item.from_user_name,
				time: sendTime,
				message: message,
				noreadnum: 0,
				messages: msgList
			}
	}
	return result
}
