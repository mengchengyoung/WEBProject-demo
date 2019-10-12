function isEmpty(obj) {
    if (typeof obj === 'undefined' || obj == null || obj == '') {
        return true
    } else {
        return false
    }
}
Date.prototype.Format = function(fmt) {
    var o = {
        'M+': this.getMonth() + 1, // 月份
        'd+': this.getDate(), // 日
        'H+': this.getHours(), // 小时
        'm+': this.getMinutes(), // 分
        's+': this.getSeconds(), // 秒
        'q+': Math.floor((this.getMonth() + 3) / 3), // 季度
        'S': this.getMilliseconds() // 毫秒
    }
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + '').substr(4 - RegExp.$1.length))
    for (var k in o) { if (new RegExp('(' + k + ')').test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (('00' + o[k]).substr(('' + o[k]).length))) }
    return fmt
}

function GetDateDiff(startTime, endTime, diffType) {
    // 将xxxx-xx-xx的时间格式，转换为 xxxx/xx/xx的格式
    if (isEmpty(startTime) || isEmpty(endTime)) {
        return 0
    }
    startTime = startTime.replace(/\-/g, '/')
    endTime = endTime.replace(/\-/g, '/')

    // 将计算间隔类性字符转换为小写
    diffType = diffType.toLowerCase()
    var sTime = new Date(startTime) // 开始时间
    var eTime = new Date(endTime) // 结束时间
    // 作为除数的数字
    var timeType = 1
    switch (diffType) {
        case 'second':
            timeType = 1000
        break
        case 'minute':
            timeType = 1000 * 60
        break
        case 'hour':
            timeType = 1000 * 3600
        break
        case 'day':
            timeType = 1000 * 3600 * 24
        break
        default:
        break
    }
    return ((eTime.getTime() - sTime.getTime()) / parseInt(timeType)).toFixed(2)
}
function getNowFormatDate() {
    var date = new Date()
    var seperator1 = '-'
    var seperator2 = ':'
    var month = date.getMonth() + 1
    var strDate = date.getDate()
    if (month >= 1 && month <= 9) {
        month = '0' + month
    }
    if (strDate >= 0 && strDate <= 9) {
        strDate = '0' + strDate
    }
    var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate +
            ' ' + date.getHours() + seperator2 + date.getMinutes() +
            seperator2 + date.getSeconds()
    return currentdate
}

function isToday(item) {
        const today = new Date().Format('yyyy-MM-dd')
        const sample_date = new Date(item['submitted']).Format('yyyy-MM-dd')
        return today === sample_date
}

export function convert_Monitordata(data) {
    var state = { '05': 'done', '04': 'failed', '03': 'hold', '02': 'running', '01': 'qsub' }
    var total_time = 0
    var today_sample = 0
    var sample_done = 0
    var sample_err = 0
    var sample_running = 0
    for (const i in data) {
        let time_cost = GetDateDiff(data[i]['running'], data[i]['finished'], 'hour')
        total_time += time_cost

        if (time_cost == 0) {
            time_cost = GetDateDiff(data[i]['running'], getNowFormatDate(), 'hour')
            data[i]['cost_time'] = time_cost + ' (h)'
        } else {
            data[i]['cost_time'] = time_cost + ' (h)'
        }
        if (isToday(data[i])) today_sample++
        switch (data[i]['status']) {
            case '05': sample_done++
            break
            case '02': sample_running++
            break
            case '04': sample_err++
            default:
                break
        }
        data[i]['status'] = state[data[i]['status']]
    }
    var sample_counts = Object.keys(data).length
    var runtime_average = total_time / sample_counts
    return { 'tableData': data, 'today_sample': today_sample, 'sample_done': sample_done, 'sample_err': sample_err, 'sample_running': sample_running }
}

