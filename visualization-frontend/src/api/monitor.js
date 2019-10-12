import request from '@/utils/request'
const base_url = 'http://192.168.2.201:8080'
//
export function build_Project(data) {
    console.log(data)
    return request({
        // baseURL: base_url,
        url: 'api/monitor/build/',
        method: 'POST',
        data: data
    })
}

export function get_Project() {
    return request({
        // baseURL: base_url,
        url: 'api/monitor/show/monitorProject/',
        method: 'POST'
    })
}

export function delete_Project(projectID) {
    return request({
        // baseURL: base_url,
        url: 'api/monitor/modify/deleteProject/',
        method: 'POST',
        data: {
            'projectID': projectID,
            'operation': 'delete'
        }
    })
}

export function stop_Project(projectID, operation) {
    return request({
        // url: 'api/monitor/modify/stopProject/',
        // baseURL: base_url,
        method: 'POST',
        data: {
            'projectID': projectID,
            'operation': operation
        }
    })
}

export function get_Monitordata(projectID) {
    return request({
        // baseURL: base_url,
        url: 'api/monitor/data/',
        method: 'POST',
        data: {
           'projectID': projectID
        }
    })
}

export function get_subprocessData(sample_id) {
    return request({
        // baseURL: base_url,
        url: 'api/monitor/subprocess/data/',
        method: 'POST',
        data: {
            'sample_id': sample_id
        }
    })
}
