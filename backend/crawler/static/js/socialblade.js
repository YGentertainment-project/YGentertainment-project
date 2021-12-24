let statusInterval;
let category = 'youtube'

function getDateString(dateText){
    var date = new Date(dateText)
    var year = date.getFullYear();
    var month = ('0' + (date.getMonth() + 1)).slice(-2);
    var day = ('0' + date.getDate()).slice(-2);
    var dateString = year + '-' + month  + '-' + day;
    return dateString
}

function getTimeString(dateText){
    var date = new Date(dateText)
    var hours = ('0' + date.getHours()).slice(-2);
    var minutes = ('0' + date.getMinutes()).slice(-2);
    var seconds = ('0' + date.getSeconds()).slice(-2);
    var timeString = hours + ':' + minutes  + ':' + seconds;
    return timeString
}

$(document).ready(function () {
    const api_domain = 'http://localhost:8000/crawler/api/'

    $('.crawler-loading').hide()
    $('.crawler-finish').hide()

    $('#site-select').change((e) => {
        category = e.target.value
        $('#board').html('')
    })

    const showCrawlSuccess = (data) => {
        const {status} = data;
        if(status === 'onprogress'){
            $('.crawler-loading').show()
            $('.crawler_finish').hide()
        }else{
            clearInterval(statusInterval);
            $('.crawler-loading').hide()
            $('.crawler_finish').show()
            $.ajax({
            url: api_domain + 'showdata/?' + $.param({
                platform: category
            }),
            type: 'GET',
            datatype:'json',
            contentType: 'application/json; charset=utf-8',
            success: res => {
                let table_html = ''
                const data_list = res.data
                showCrawledData(data_list) // Data들을 화면상에 표시
            },
            error: e => {
                alert('Failed to load data. Any crawled data is not saved.')
            },
        })
        }
    }

    const showCrawlFailure = (data) => {
        console.log(data);
    }

    const checkCrawlStatus = (taskId) => {
        $.ajax({
            url: api_domain + 'crawl/?task_id='+taskId,
            type: 'GET',
            success: showCrawlSuccess,
            error: showCrawlFailure,
        })
    }

    $('#start-crawl').click(() => {

        $('.crawler-loading').hide()
        $('.crawler_finish').hide()

        $('#board').html('')
        // 1. POST 요청 전송
        let task_id;
        $.ajax({
            url: api_domain + 'crawl/',
            type:'POST',
            data: JSON.stringify({"platform": category}),
            datatype:'json',
            contentType: 'application/json; charset=utf-8',
            success: res => {
                task_id = res['task_id'] // api 요청으로부터 task_id 받기
                // 2. 3초 간격으로 GET 요청을 보내서 상태 표시 갱신
                statusInterval = setInterval(() => checkCrawlStatus(task_id), 3000)
            },
            error: e => {
                alert('Failed to send request for scraping')
            },
        })
    })

    // Row를 만드는 함수
    const createTableRow = (data) => {
        const tableRow = $('<tr></tr>')
        // 해당 row에 대한 column 데이터들 넣기
        for(key in data){
            let dataCol;
            if(key === 'platform'){
                continue;
            }
            if (key === 'url') {
                let dataColUrl = $('<a></a>', {
                    href: data[key],
                    text: data[key],
                });
                dataCol = $('<td></td>');
                dataCol.append(dataColUrl);
            }
            else if(key === 'recorded_date'){
                dateString = getDateString(data[key]) + ' ' + getTimeString(data[key])
                dataCol = $('<td></td>', {
                    text: dateString,
                })
            }
            else{
                dataCol = $('<td></td>', {
                    text:data[key],
                })
            }
            tableRow.append(dataCol)
        }
        return tableRow
    }

    // crawl된 데이터를 표시하는 함수
    const showCrawledData = (datas) => {
        datas.forEach(data => {
            $('#board').append(createTableRow(data))
        })
    }

    // DB에 저장된 데이터 불러오기
    $('#show-data').click(() => {
        $.ajax({
            url: api_domain + 'showdata/?' + $.param({
                platform: category
            }),
            type: 'GET',
            datatype:'json',
            contentType: 'application/json; charset=utf-8',
            success: res => {
                let table_html = ''
                const data_list = res.data
                showCrawledData(data_list) // Data들을 화면상에 표시
            },
            error: e => {
                alert('Failed to load data. Any crawled data is not saved.')
            },
        })
    })
})