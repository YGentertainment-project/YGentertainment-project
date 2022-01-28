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

                // let dataCol2 = document.createElement('td');
                // let dataCol2Div = document.createElement('div');
                // data['artists'].forEach(artist_name => {
                //     let dataCol2DivBtn = document.createElement('span');
                //     dataCol2DivBtn.innerHTML = `
                //     <span style="margin-right:10px;">${artist_name}</span>
                //     `;
                //     dataCol2Div.append(dataCol2DivBtn);
                // })
                // dataCol2.append(dataCol2Div);
                // tableRow.append(dataCol2);
                let dataCol2 = document.createElement('td');
                dataCol2.innerHTML = `<td style="width: 100px;">
                    <select id="schedule-hour-select${tmp_index}" class="form-select">
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
                dataCol4.onclick = function(){
                    update_platform_schedule(platform, tmp_index);
                };
                dataCol4.innerHTML = `
                <label class="btn btn-primary btn-shadow border-0" style="margin: 10px; font-weight: bold;">
                    저장
                </label>`;
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

function update_platform_schedule(platform, platform_index){
    var data = {
        'platform': platform,
        'period': parseInt($(`#schedule-hour-select${platform_index} option:selected`).val()),
        'execute_time_minute': parseInt($(`#schedule-minute-select${platform_index} option:selected`).val())
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