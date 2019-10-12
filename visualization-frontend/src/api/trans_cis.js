import request from '@/utils/request'
const base_url = 'http://192.168.2.201:8080'
export function get_trans_cis(data) {
    return request({
        baseURL: base_url,
        url: '/api/trans/get_trans_cis/',
        method: 'POST',
        data: data
    })
}
export function validateHGVS(data) {
    return request({
        baseURL: base_url,
        url: '/api/trans/validateHGVS/',
        method: 'POST',
        data: data
    })
}
