//플랫폼별 스케줄러 시간 로딩 및 크롤러 상태 로딩
$(document).ready(function(){
    $.ajax({
        url: '/crawler/api/schedules/?' + $.param({
            schedule_type: 'daily'
        }),
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

    var today = new Date();

    var year = today.getFullYear();
    var month = ('0' + (today.getMonth() + 1)).slice(-2);
    var day = ('0' + today.getDate()).slice(-2);

    var dateString = year + '-' + month  + '-' + day;
   

    const fromDate = dateString
    const toDate = dateString
    $.ajax({
        url:  '/crawler/api/monitors/?' + $.param({
            fromdate: fromDate,
            todate: toDate,
        }),
        type: 'GET',
        datatype: 'json',
        contentType: 'application/json; charset=utf-8',
        success: res => {
            const {normals, execs, errors, details} = res

            console.log(details);
            
            $('.state-description-success').text('정상 '+normals+'건');
            $('.state-description-error').text('오류 '+errors+'건');
            $('.state-description-running').text('실행 중 ' +execs+'건');

            var no_page = 0
            var no_login = 0
            var ect = 0

            details.forEach(detail => {
              if(detail['type'] == '400'){
                  no_page = no_page + 1
              } else if(detail['type'] == '401'){
                  no_login = no_login +1
              } else{
                  ect = ect +1
              }
            })

          $('#no-page').text(no_page)
          $('#no-login').text(no_login)
          $('#ect').text(ect)
           
        },
        error: e => {
            console.log(e)
            $('.state-description-success').text('정상 '+'None'+'건');
            $('.state-description-error').text('오류 '+'None'+'건');
            $('.state-description-running').text('실행 중 ' +'None'+'건');
        },
    })
})


$(document).on('click','#save-schedule',function(){
    var td = $(this).closest('tr').children();
    var platform = td.eq(0).text();
    var hour = td.eq(1).find('#hour-select option:selected').val();
    var minute = td.eq(2).find('#minute-select option:selected').val();

    if(platform === 'instagram' || platform === 'facebook'){
        platform = 'crowdtangle'
    }

    // schedule table에 저장
    $.ajax({
        url: '/dataprocess/api/schedule/',
        type: 'PUT',
        data: JSON.stringify({ "platform": platform, "execute_time_hour": hour, "execute_time_minute": minute, 'schedule_type':'daily' }),
        datatype: 'json',
        contentType: 'application/json; charset=utf-8',
        success: res => {
            console.log(res);
        },
        error: e => {
            console.log(e);
        },
    })


    if (minute>= 0 && minute<= 59 && hour >= 0 && hour <= 23 && !isNaN(hour)) {
        // Schedule 생성 API request 보내기
        $.ajax({
            url: '/crawler/api/schedules/',
            type: 'POST',
            data: JSON.stringify({ "platform": platform, "hours": hour, "minutes": minute, 'schedule_type': 'daily' }),
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
        url: '/dataprocess/api/schedule/?type=시간별',
        type: 'GET',
        datatype:'json',
        contentType: 'application/json; charset=utf-8',
        success: res => {
            var datalist = res.data;
            $('#hourly-scheduler-body').eq(0).empty();
            hourly_schedule_list = datalist;
            var index = 0;
            datalist.forEach(data => {
                const tableRow = $('<tr></tr>');
                let dataCol = document.createElement('td');
                let platform = data['platform'];
                let artists = data['artists'];
                let tmp_index = index;
                dataCol.onclick = function(){
                    show_hourly_modal(platform, artists, tmp_index);
                };
                dataCol.innerHTML = `
                <td>
                    <span class="input-btn">${data['platform']}</span>
                </td>
                `;
                tableRow.append(dataCol);

                let dataCol2 = document.createElement('td');
                dataCol2.innerHTML = `<td style="width: 100px;">
                    <select id="schedule-hour-select${tmp_index}" class="form-select">
                        <option value="1">01</option>
                        <option value="2">02</option>
                        <option value="3">03</option>
                        <option value="4">04</option>
                        <option value="5">05</option>
                        <option value="6">06</option>
                        <option value="7">07</option>
                        <option value="8">08</option>
                        <option value="9">09</option>
                        <option value="10">10</option>
                        <option value="11">11</option>
                        <option value="12">12</option>
                        <option value="13">13</option>
                        <option value="14">14</option>
                        <option value="15">15</option>
                        <option value="16">16</option>
                        <option value="17">17</option>
                        <option value="18">18</option>
                        <option value="19">19</option>
                        <option value="20">20</option>
                        <option value="21">21</option>
                        <option value="22">22</option>
                        <option value="23">23</option>
                    </select>
                </td>`;
                tableRow.append(dataCol2);
                let dataCol3 = document.createElement('td');
                dataCol3.innerHTML = `
                <td style="width: 100px;">
                            <select style="margin:2px;" name="minute" id="schedule-minute-select${tmp_index}" class="form-select">
                                <option value="0">00</option>
                                <option value="1">01</option>
                                <option value="2">02</option>
                                <option value="3">03</option>
                                <option value="4">04</option>
                                <option value="5">05</option>
                                <option value="6">06</option>
                                <option value="7">07</option>
                                <option value="8">08</option>
                                <option value="9">09</option>
                                <option value="10">10</option>
                                <option value="11">11</option>
                                <option value="12">12</option>
                                <option value="13">13</option>
                                <option value="14">14</option>
                                <option value="15">15</option>
                                <option value="16">16</option>
                                <option value="17">17</option>
                                <option value="18">18</option>
                                <option value="19">19</option>
                                <option value="20">20</option>
                                <option value="21">21</option>
                                <option value="22">22</option>
                                <option value="23">23</option>
                                <option value="24">24</option>
                                <option value="25">25</option>
                                <option value="26">26</option>
                                <option value="27">27</option>
                                <option value="28">28</option>
                                <option value="29">29</option>
                                <option value="30">30</option>
                                <option value="31">31</option>
                                <option value="32">32</option>
                                <option value="33">33</option>
                                <option value="34">34</option>
                                <option value="35">35</option>
                                <option value="36">36</option>
                                <option value="37">37</option>
                                <option value="38">38</option>
                                <option value="39">39</option>
                                <option value="40">40</option>
                                <option value="41">41</option>
                                <option value="42">42</option>
                                <option value="43">43</option>
                                <option value="44">44</option>
                                <option value="45">45</option>
                                <option value="46">46</option>
                                <option value="47">47</option>
                                <option value="48">48</option>
                                <option value="49">49</option>
                                <option value="50">50</option>
                                <option value="51">51</option>
                                <option value="52">52</option>
                                <option value="53">53</option>
                                <option value="54">54</option>
                                <option value="55">55</option>
                                <option value="56">56</option>
                                <option value="57">57</option>
                                <option value="58">58</option>
                                <option value="59">59</option>
                            </select>
                        </td>`;
                        // dataCol3.options["4"].selected = true;
                // dataCol3.val("3").prop('selected',true);
                tableRow.append(dataCol3);
                let dataCol4 = document.createElement('td');

                if (artists.length <= 0){
                    dataCol4.onclick = function(){
                        alert('시간별로 수집할 아티스트를 먼저 선정하세요.')
                    }
                    dataCol4.innerHTML = `
                    <label class="btn btn-primary btn-shadow border-0 disabled" style="margin: 5px; font-weight: bold;font-size: 10px !important; width: 50px;">
                        저장
                    </label>`;
                }else{
                    dataCol4.onclick = function(){
                        update_hourly_platform_schedule(platform, tmp_index);
                    };
                    dataCol4.innerHTML = `
                    <label class="btn btn-primary btn-shadow border-0" style="margin: 5px; font-weight: bold;font-size: 10px !important; width: 50px;">
                        저장
                    </label>`;
                }

                tableRow.append(dataCol4);
                index += 1;

                $('#hourly-scheduler-body').append(tableRow);


                var period_time = data['period'].split(':');
                $(`#schedule-hour-select${tmp_index}`).val(parseInt(period_time[0])).prop('selected',true);
                var execute_time = data['execute_time'].split(':');
                $(`#schedule-minute-select${tmp_index}`).val(parseInt(execute_time[1])).prop('selected',true);
            })
        },
        error: e => {
            console.log(e);
        },
    });
}

function update_hourly_platform_schedule(platform, platform_index){
    var data = {
        'platform': platform,
        'period': parseInt($(`#schedule-hour-select${platform_index} option:selected`).val()),
        'execute_time_minute': parseInt($(`#schedule-minute-select${platform_index} option:selected`).val()),
        'schedule_type': 'hour'
    };

    // 플랫폼이 일정주기 크롤링 하도록 설정
    $.ajax({
        url: '/crawler/api/schedules/',
        type: 'POST',
        data: JSON.stringify(data),
        datatype:'json',
        contentType: 'application/json; charset=utf-8',
        success: res => {
            console.log(res)
        },
        error: e => {
            console.log(e)
        },
    })
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

function show_hourly_modal(platform_name, artists, index){
    document.getElementById('schedule-modal-title').innerHTML = `${platform_name} 시간별 아티스트`;

    $('#hourly-artist').eq(0).empty();
    artists.forEach(data=>{
        const artist = document.createElement('span');
        artist.innerHTML = `<span style="margin-right: 8px;">${data}</span>`
        $('#hourly-artist').append(artist);
    })
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
    var modal = $('div').find('.modal')
    if(modal.hasClass('show')){
        modal.removeClass('show');
        modal.css('display','none');
    } 
}

get_hourly_schedule();
$(document).on('click','#schedule-close', close_hourly_modal);