
import { request, METHOD} from '@/utils/request'
 
export const followerList = (id, params) => {
  const url = `/api/follower/${id}`
  return request(url, 'get', params)
}


export async function api_get_test(url) {
  return request(url, METHOD.GET)
}
export default {
  api_get_test
}
