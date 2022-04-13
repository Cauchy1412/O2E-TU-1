import request from "./request";
// let baseUrl=process.env.NODE_ENV === 'development'?"xxx":"xxx";
// let socketBaseUrl=process.env.NODE_ENV === 'development'?"xxx":"xxx";

//  let baseUrl=process.env.NODE_ENV === 'development'?"http://114.115.168.211:8000/api/":"http://114.115.168.211:8000/api/";
// let socketBaseUrl=process.env.NODE_ENV === 'development'?"ws://114.115.168.211:8000/api/":"ws://114.115.168.211:8000/api/";
 let baseUrl=process.env.NODE_ENV === 'development'?"http://127.0.0.1:8000/api/":"http://127.0.0.1:8000/api/";
let socketBaseUrl=process.env.NODE_ENV === 'development'?"ws://127.0.0.1:8000/api/":"ws://127.0.0.1:8000/api/";
//可以new多个request来支持多个域名请求
let $http = new request({
	//接口请求地址
	baseUrl: baseUrl,
	//服务器本地上传文件地址
	fileUrl: baseUrl,
	websocket: socketBaseUrl,
	//设置请求头（如果使用报错跨域问题，可能是content-type请求类型和后台那边设置的不一致）
	headers: {
		'content-type': 'application/json;charset=UTF-8'
	},
	// {
	// 	"content-type":"application/x-www-form-urlencoded"
	// }
	
})
export default $http;