let statusInterval;
let crawlCategory = 'youtube'
let dataCategory = 'youtube'

function getDateString(dateText) {
    var date = new Date(dateText)
    var year = date.getFullYear();
    var month = ('0' + (date.getMonth() + 1)).slice(-2);
    var day = ('0' + date.getDate()).slice(-2);
    var dateString = year + '-' + month + '-' + day;
    return dateString
}

function getTimeString(dateText) {
    var date = new Date(dateText)
    var hours = ('0' + date.getHours()).slice(-2);
    var minutes = ('0' + date.getMinutes()).slice(-2);
    var seconds = ('0' + date.getSeconds()).slice(-2);
    var timeString = hours + ':' + minutes + ':' + seconds;
    return timeString
}


headerList = {
    "youtube": ['artist', 'uploads', 'subscribers', 'views', 'User Created', 'Recorded Date', 'URL'],
    "tiktok": ['artist', 'uploads', 'followers', 'likes', 'Recorded Date', 'URL'],
    "twitter": ['artist', 'followers', 'twits', 'User Created', 'Recorded Date', 'URL'],
    "twitter2": ['artist', 'followers', 'twits', 'User Created', 'Recorded Date', 'URL'],
    "weverse": ['artist', 'weverses', 'Recorded Date', 'URL'],
    "facebook": ['artist', 'followers', 'Recorded Date', 'URL'],
    "instagram": ['artist', 'followers', 'Recorded Date', 'URL'],
    "vlive": ['artist', 'members', 'videos', 'likes', 'plays', 'Recorded Date', 'URL'],
    "melon": ['artist', 'listeners', 'streams', 'fans', 'Recorded Date', 'URL1', 'URL2'],
    "spotify": ['artist', 'monthly_listens', 'followers', 'Recorded Date', 'URL']
}


$(document).ready(function () {
    const api_domain = '/crawler/api/'

    $('.crawler-loading').hide()
    $('.crawler-finish').hide()

    $('#crawl-select').change((e) => {
        crawlCategory = e.target.value
    })

    $('#data-select').change((e) => {
        dataCategory = e.target.value
        $('#board').html('')
        $('#table-header tr').html('')
        const headerRows = headerList[dataCategory].map((header) =>
            $('<th></th>', {
                scope: "slope",
                text: header,
            })
        )
        headerRows.forEach((headerRow) => {
            $('#table-header tr').append(headerRow)
        })
    })




    const showCrawlSuccess = (data) => {
        const { status } = data;
        // PENDING, FINISHED, or something.
        if (status === 'PENDING') {
            $('.crawler-loading').show()
            $('.crawler_finish').hide()
        } else {
            clearInterval(statusInterval);
            $('.crawler-loading').hide()
            $('.crawler_finish').show()
            $.ajax({
            url: api_domain + 'showdata/?' + $.param({
                platform: crawlCategory
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
            url: api_domain + 'crawl/?task_id=' + taskId,
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
            data: JSON.stringify({"platform": crawlCategory}),
            datatype:'json',
            contentType: 'application/json; charset=utf-8',
            success: res => {
                task_id = res['task_id'] // api 요청으로부터 task_id 받기
                alert(`Task ${task_id} 에서 크롤링을 진행 하고 있습니다!`)
                console.log(task_id)
            },
            error: e => {
                alert('Failed to send request for scraping')
            },
        })
    })

    // Row를 만드는 함수
    const createTableRow = (data, type = 'data') => {
        const tableRow = $('<tr></tr>')
        // 해당 row에 대한 column 데이터들 넣기
        for (key in data) {
            console.log('key : ', key)
            let dataCol;
            if (key === 'id') {
                tableRow.attr("id", data[key])
                continue;
            }
            else if (key === 'url') {
                let dataColUrl = $('<a></a>', {
                    href: data[key],
                    text: data[key],
                });
                dataCol = $('<td></td>');
                dataCol.append(dataColUrl);
            }
            else if (key === 'recorded_date' || key === 'last_run') {
                let dateString = '';
                if (!data[key]) {
                    dateString = '없음'
                }
                else {
                    dateString = getDateString(data[key]) + ' ' + getTimeString(data[key])
                }
                dataCol = $('<td></td>', {
                    text: dateString,
                })
            }
            else if(key === 'started'){
                dataCol = $('<td></td>', {
                    text: data[key],
                })
            }
            else if(key === 'runtime'){
                dataCol = $('<td></td>', {
                    text: `${Number(data[key]).toFixed(2)}초`,
                })
            }
            else {
                dataCol = $('<td></td>', {
                    text: data[key],
                })
            }
            tableRow.append(dataCol)
        }
        if (type === 'schedule') {
            const deleteBtn = $('<button></button>', {
                type: 'button',
                class: 'btn btn-danger',
                text: '삭제'
            })
            deleteBtn.click(deleteSchedule)
            const dataCol = $('<td></td>')
            dataCol.append(deleteBtn);
            tableRow.append(dataCol);
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
                platform: dataCategory
            }),
            type: 'GET',
            datatype: 'json',
            contentType: 'application/json; charset=utf-8',
            success: res => {
                $('#board').html('')
                const data_list = res.data
                showCrawledData(data_list) // Data들을 화면상에 표시
            },
            error: e => {
                alert('Failed to load data. Any crawled data is not saved.')
            },
        })
    })

    // 스케줄 생성 AJAX 요청
    $('#create-schedule').click(() => {
        const scheduleSpider = $('#spiderSelect').val();
        const scheduleHours = $('#hoursControlInput').val() === '' ? '' : Number($('#hoursControlInput').val());
        const scheduleMinutes = Number($('#minutesControlInput').val());
        $('#hoursControlInput').val('');
        $('#minutesControlInput').val('');
        if (scheduleMinutes >= 0 && scheduleMinutes <= 59 && scheduleHours >= 0 && scheduleHours <= 23 && !isNaN(scheduleHours)) {
            // Schedule 생성 API request 보내기
            $.ajax({
                url: api_domain + 'schedules/',
                type: 'POST',
                data: JSON.stringify({ "platform": scheduleSpider, "hours": scheduleHours, "minutes": scheduleMinutes }),
                datatype: 'json',
                contentType: 'application/json; charset=utf-8',
                success: res => {
                    $('#close-schedulemodal').click()
                },
                error: e => {
                    alert('Failed to create task')
                },
            })
        }
        else {
            alert('스케줄 시간 입력이 잘못되었습니다.');
        }
    })

    const deleteSchedule = (e) => {
        const parentCol = e.target.parentNode;
        const parentRow = parentCol.parentNode;
        console.log(parentRow)
        const scheduleId = parentRow.id;
        $.ajax({
            url: api_domain + 'schedules/',
            type: 'DELETE',
            data: JSON.stringify({ "id": scheduleId }),
            datatype: 'json',
            contentType: 'application/json; charset=utf-8',
            success: res => {
                const schedules = res.schedules;
                $('#schedule-board').html('')
                schedules.forEach(schedule => {
                    $('#schedule-board').append(createTableRow(schedule, 'schedule'));
                })
            },
            error: e => {
                alert('Failed to delete schedule')
            },
        })
    }


    // schedule 들의 리스트들을 불러옴
    $('#listup-schedule').click(() => {
        $.ajax({
            url: api_domain + 'schedules/',
            type: 'GET',
            datatype: 'json',
            contentType: 'application/json; charset=utf-8',
            success: res => {
                $('#schedule-board').html('');
                const schedules = res.schedules;
                schedules.forEach(schedule => {
                    console.log(schedule.last_run)
                    $('#schedule-board').append(createTableRow(schedule, 'schedule'));
                })
            },
            error: e => {
                alert('Failed to listup schedules')
            },
        })
    })

    $('#listup-tasks').click(() => {
        $.ajax({
            url: api_domain + 'taskinfos/',
            type: 'GET',
            datatype: 'json',
            contentType: 'application/json; charset=utf-8',
            success: res => {
              $('#task-board').html('');
              const taskinfos = res.taskinfos;
              console.log(taskinfos)
              taskinfos.forEach(taskinfo => {
                  $('#task-board').append(createTableRow(taskinfo, 'task'));
              })
            },
            error: e => {
                alert('Failed to listup executed tasks')
            },
        })
    })

    $('#get-monitor').click((e) => {
        e.preventDefault();
        const fromDate = $('#InputFromDate').val()
        const toDate = $('#InputToDate').val()
        $.ajax({
            url: api_domain + 'monitors/?' + $.param({
                fromdate: fromDate,
                todate: toDate,
            }),
            type: 'GET',
            datatype: 'json',
            contentType: 'application/json; charset=utf-8',
            success: res => {
                const {normals, execs, errors, details} = res
                $('#stats-board').append(createTableRow({'normals': normals, 'errors': errors, 'execs': execs}))
                details.forEach(detail => {
                    tableRow = $('#monitor-board').append(createTableRow(detail) )
                })
            },
            error: e => {
                console.log(e)
                alert(e.responseJSON.error)
            },
        })
    })
})
