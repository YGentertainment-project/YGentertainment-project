//task info
function getTaskinfo(){
    $.ajax({
        url: '/crawler/api/taskinfos/',
        type: 'GET',
        datatype: 'json',
        contentType: 'application/json; charset=utf-8',
        success: res => {
          const taskinfos = res.taskinfos;
          return taskinfos
        },
        error: e => {
            console.log(e);
            const taskinfos = [];
            return taskinfos
        },
    })
}

//플랫폼별 스케줄러 시간 로딩 및 크롤러 상태 로딩
$(document).ready(function(){
    $.ajax({
        url: '/crawler/api/schedules/',
        type: 'GET',
        datatype: 'json',
        contentType: 'application/json; charset=utf-8',
        success: res => {
            const schedules = res.schedules;
            schedules.forEach(schedule => {
                var name = schedule.name
                var splitResult = name.split('_');

                var tr = $('#scheduler-body').find('tr')

                for(var r=0;r<tr.length;r++){
                    var cells = tr[r].getElementsByTagName("td");

                    if(splitResult[0] === cells[0].innerHTML){
                        cells[1].firstElementChild.value = schedule.hour;
                        cells[2].firstElementChild.value = schedule.minute;
                    } else if(splitResult[0] === 'crowdtangle' && cells[0].innerHTML === 'instagram' || splitResult[0] === 'crowdtangle' && cells[0].innerHTML === 'facebook'){
                        cells[1].firstElementChild.value = schedule.hour;
                        cells[2].firstElementChild.value = schedule.minute;
                    } 
                }
                
            })
        },
        error: e => {
            alert('Failed to listup schedules')
        },
    })


    //crawler status
    let success = 0;
    let error = 0;
    let running = 0;


    $('.state-description-success').text('정상 '+success+'건');
    $('.state-description-error').text('오류 '+error+'건');
    $('.state-description-running').text('실행 중 ' +running+'건');
})


$(document).on('click','#save-schedule',function(){
    var td = $(this).closest('tr').children();
    var platform = td.eq(0).text();
    var hour = td.eq(1).find('#hour-select option:selected').val();
    var minute = td.eq(2).find('#minute-select option:selected').val();

    if(platform === 'instagram' || platform === 'facebook'){
        platform = 'crowdtangle'
    }

    if (minute>= 0 && minute<= 59 && hour >= 0 && hour <= 23 && !isNaN(hour)) {
        // Schedule 생성 API request 보내기
        $.ajax({
            url: '/crawler/api/schedules/',
            type: 'POST',
            data: JSON.stringify({ "platform": platform, "hours": hour, "minutes": minute }),
            datatype: 'json',
            contentType: 'application/json; charset=utf-8',
            success: res => {
                alert('저장되었습니다.');
                location.reload(); // 데이터 불러오기
            },
            error: e => {
                alert('스케줄 생성에 실패했습니다.')
            },
        })
    }
    else {
        alert('스케줄 시간 입력이 잘못되었습니다.');
    }
})


//시간별 스케줄 테이블
var hourly_schedule_list = [];
function get_hourly_schedule(){
    $.ajax({
        url: '/dataprocess/api/schedule/?' + $.param({
            type: '시간별'
        }),
        type: 'GET',
        datatype:'json',
        contentType: 'application/json; charset=utf-8',
        success: res => {
            var datalist = res.data;
            console.log(datalist);
            $('#hourly-scheduler-body').eq(0).empty();
            hourly_schedule_list = datalist;
            console.log(hourly_schedule_list);
            var index = 0;
            datalist.forEach(data => {
                const tableRow = $('<tr></tr>');
                let dataCol = document.createElement('td');
                let platform = data['platform'];
                let tmp_index = index;
                dataCol.onclick = function(){
                    show_hourly_modal(platform, tmp_index);
                };
                dataCol.innerHTML = `
                <td>
                    <span class="input-btn">${data['platform']}</span>
                </td>
                `;
                tableRow.append(dataCol);

                let dataCol2 = document.createElement('td');
                let dataCol2Div = document.createElement('div');
                data['artists'].forEach(artist_name => {
                    let dataCol2DivBtn = document.createElement('span');
                    dataCol2DivBtn.innerHTML = `
                    <span style="margin-right:10px;">${artist_name}</span>
                    `;
                    dataCol2Div.append(dataCol2DivBtn);
                })
                dataCol2.append(dataCol2Div);
                tableRow.append(dataCol2);
                $('#hourly-scheduler-body').append(tableRow);
                index += 1;
            })
        },
        error: e => {
            console.log(e);
        },
    });
}

function update_platform_schedule(){
    var platform_name = document.getElementById('schedule-modal-title').innerHTML.replace(" 시간별 스케줄","");
    var platform_index = document.getElementById('schedule-platform-index').innerHTML;
    var data = {
        'platform': platform_name,
        'period': parseInt($('#schedule-hour-select option:selected').val()),
        'execute_time_minute':parseInt($('#schedule-minute-select option:selected').val())
    };
    $.ajax({
        url: '/dataprocess/api/schedule/',
        type: 'PUT',
        datatype:'json',
        data: JSON.stringify(data),
        success: res => {
            hourly_schedule_list[platform_index]['period'] = `${$('#schedule-hour-select option:selected').val()}:00:00`;
            hourly_schedule_list[platform_index]['execute_time'] = `00:${$('#schedule-minute-select option:selected').val()}:00`;
            alert('저장되었습니다.');
            close_hourly_modal();
        },
        error: e => {
            console.log(e);
        },
    })
}

function show_hourly_modal(platform_name, index){
    console.log(index);
    var period = hourly_schedule_list[index]['period'];
    var execute_time = hourly_schedule_list[index]['execute_time'];
    document.getElementById('schedule-modal-title').innerHTML = `${platform_name} 시간별 스케줄`;
    var period_time = period.split(':');
    $('#schedule-hour-select').val(parseInt(period_time[0])).prop('selected',true);
    execute_time = execute_time.split(':');
    $('#schedule-minute-select').val(parseInt(execute_time[1])).prop('selected',true);
    var modal = $('div').find('.modal');
    if(modal.hasClass('show')){
        modal.removeClass('show');
        modal.css('display','none');
    } else{
        modal.addClass('show');
        modal.css('display','block');
    }
}

function close_hourly_modal(){
    console.log("close");
    var modal = $('div').find('.modal')
    if(modal.hasClass('show')){
        modal.removeClass('show');
        modal.css('display','none');
    } 
}

get_hourly_schedule();
$(document).on('click','#schedule-close', close_hourly_modal);
$(document).on('click','#schedule-update', update_platform_schedule);