import { GOODS, GOODS_COLUMNS, PaperAll,UserAll } from "./api";
import { METHOD, request } from "@/utils/request";

export async function goodsList(params) {
  return request(GOODS, METHOD.GET, params);
}

export async function goodsColumns() {
  return request(GOODS_COLUMNS, METHOD.GET);
}

export const getkeywords = (params) => {
  const typeUrl = "Interpretation";
  const url = `/api/${typeUrl}/getkeywords`;
  return request(url, "get", params);
};

export const recommend = (params) => {
  const url = "/api/recommend";
  return request(url, "get", params);
};

export const getvis = (params) => {
  const typeUrl = "Interpretation";
  const url = `/api/${typeUrl}/getvis`;
  return request(url, "get", params);
};

export const gettags = (params) => {
  const typeUrl = "Interpretation";
  const url = `/api/${typeUrl}/gettags`;
  return request(url, "get", params);
};

export const getInterpretationComments = (method, params) => {
  const url = "/api/comment";
  return request(url, method, params);
};

export const getUserInfo = (id) => {
  const url = "/api/user/profile";
  if (id) {
    return request(url, "get", { user_id: id });
  } else {
    return request(url, "get");
  }
};

export const InterpretationIdReq = (id, type, method, params) => {
  const typeUrl = type === 1 ? "Interpretation" : "Note";
  const url = `/api/${typeUrl}/${id}`;
  return request(url, method, params);
};

export const getLocalTime = (utcTime) => {
  if (utcTime === null || utcTime === undefined) {
    return '无'
  } else {
    let date = new Date(utcTime)
    const second = date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds()
    const min = date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes()
    const hour = date.getHours() < 10 ? '0' + date.getHours() : date.getHours()
    // if (isHour) {
    //   return `${hour}:${min}:${second}`
    // }
    return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${hour}:${min}:${second}`
  }
}

export const getPaperAll = (id) => {
  if (id) {
    return request(PaperAll, "get", { user_id: id });
  } else {
    return request(PaperAll, "get");
  }
};

export const createProject = (params) => {
  const url = `/api/project/create`
  return request(url, 'post', params)
}

export const modifyProject = (params) => {
  const url = `/api/project/${params.id}`
  return request(url, 'post', params)
}

export const deleteProject = (params) => {
  const url = `/api/project/${params.id}`
  return request(url, 'delete', params)
}

export const addComment = (method, params) => {
  const url = '/api/comment/create'
  return request(url, method, params)
}

export const deleteComment = (method, params) => {
  const url = '/api/comment/delete'
  return request(url, method, params)
}

export const createDiscussionComment = (params) => {
  const url = `/api/discussion/create`
  return request(url, 'post', params)
}

export const deleteDiscussionComment = (method, params) => {
  const url = `/api/discussion/delete`
  return request(url, method, params)
}

export const getUserAll = (id) => {
  if (id) {
    return request(UserAll, "get", { user_id: id });
  } else {
    return request(UserAll, "get");
  }
};

export const UserDel = (params) => {
  const url = `/api/user/delete`
  return request(url,"post",params)
}

export const UserModify = (params) => {
  const url = `/api/user/changeinfo`
  return request(url, "post",params)
}

export const set_verified = (params) => {
  const url = `/api/verify/set-verified`
  return request(url, "post", params)
}

export const set_failed = (params) => {
  const url = `/api/verify/set-failed`
  return request(url, "post", params)
}

export default {
  goodsList,
  goodsColumns,
  getkeywords,
  recommend,
  getvis,
  getPaperAll,
  gettags,
  InterpretationIdReq,
  getUserInfo,
  getInterpretationComments,
  getLocalTime,
  createProject,
  modifyProject,
  deleteProject,
  addComment,
  createDiscussionComment,
  deleteComment,
  deleteDiscussionComment,
  UserDel,
  UserModify,
  set_verified,
  set_failed,
};
