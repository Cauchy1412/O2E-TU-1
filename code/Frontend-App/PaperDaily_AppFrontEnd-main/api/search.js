import axios from '@/config/requestConfig.js';
import time from '../common/time.js';
import {
	picUrl
} from './common.js'



export const searchTopicList = async (page=1,key='',author='') => {
	let headers = {
		"Authorization":'Bearer ' + uni.getStorageSync('token')
	}
	let result = await axios.get('Interpretation/page/'+1+'?author='+author+'&keywords='+key,{},headers)
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
