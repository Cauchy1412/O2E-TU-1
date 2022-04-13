import axios from '@/config/requestConfig.js';
import {
	picUrl
} from './common.js'
export const  getTopicDetail =async (id) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let detail = await axios.get('Interpretation/'+ id,{},headers)
	// if(detail.images==null||detail.images==''){
	// 	detail.images = []
	// }else{
	// 	detail.images = detail.images.split(",")
	// }
	detail.userpic=picUrl+detail.userpic
	return detail
}

export const  pushHistory = async (data) => {
	// let detail = await axios.post('Interpretation/browsingRecords',data,headers)
}

export const  getCommentList = async (uid,data) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let result = await axios.get('comment',data,headers)
	let temp=result.comment_list
	let comments = temp.map((x) => {
				return {
					id: x.id,
					username: x.username,
					created_at: x.created_at,
					user_id: uid,
					text: x.text,
					to: x.to_user ? x.to_user.username : 0,
					toId: x.to_user ? x.to_user.id : '',
					userpic: picUrl+x.userpic,
					parentId: x.parent_comment_id,
					children: []
				}
			})
	let father_comments_map = {}
	comments.filter(x => (x.parentId === undefined)).forEach(x => {
	   father_comments_map[x.id] = x
	})
	comments.forEach(x => {
	    if (x.parentId !== undefined) {
	          father_comments_map[x.parentId].children.push(x)
	    }
	})
	let ans=Object.values(father_comments_map)
	let length=comments.length
	return {"ans":ans,"length":length}
}
export const  delComment = async (id) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let result = await axios.post("comment/delete",{"id":id},headers)
	return result
}

export const  addComment = async (data) => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let result = await axios.post("comment/create",data,headers)
	return result
}
