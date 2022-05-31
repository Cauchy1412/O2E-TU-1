//跨域代理前缀
const API_PROXY_PREFIX='/api'
const BASE_URL = process.env.NODE_ENV === 'production' ?
    'http://114.116.221.131/api' :
    API_PROXY_PREFIX
const BASE_AXIOS_URL = 'http://114.116.221.131';

// const BASE_URL = process.env.VUE_APP_API_BASE_URL
module.exports = {
  BASE_URL,
  LOGIN: `${BASE_URL}/token-auth`,
  ROUTES: `${BASE_URL}/routes`,
  GOODS: `${BASE_URL}/goods`,
  GOODS_COLUMNS: `${BASE_URL}/columns`,
  PaperAll:`${BASE_URL}/Interpretation/getall`,
  UserAll:`${BASE_URL}/user/all`
}
