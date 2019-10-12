import request from '@/utils/request'

const login_url = 'http://localhost:9527'
export function login(data) {
  return request({
//    baseURL: login_url,
    url: '/user/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    // baseURL: login_url,
    url: '/user/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    // baseURL: login_url,
    url: '/user/logout',
    method: 'post'
  })
}
