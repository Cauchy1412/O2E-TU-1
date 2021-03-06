import { request, METHOD } from "@/utils/request";

export async function get_demand_all() {
    const url = `/api/demand/all`
    return request(url, METHOD.GET);
}

export async function get_resolution_all() {
    const url = '/api/resolution/all'
    return request(url, METHOD.GET);
}

export const del_demand = (params) => {
    const url = '/api/demand/delete'
    return request(url, METHOD.POST, params);
}

export default {
    get_demand_all,
    get_resolution_all,
    del_demand,
}