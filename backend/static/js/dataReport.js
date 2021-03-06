//number format
function numToString(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

//uncomma string number
function uncomma(str) {
    str = String(str);
    return str.replace(/[^\d]+/g, '');
}

//string check
function isString(inputText){
    return isNaN(Number(inputText));
}

function goTop(){
	$('#result-table').scrollTop(0);
}

function ajax(type,platform,start_date,end_date){
    if(!platform){
        return false;
    } 

    if(type == undefined){
        alert("누적/기간별 중 선택해주세요.");
        return;
    }else if(type=="누적" && start_date==""){
        alert("시작 일자를 선택해주세요.");
        return;
    } else if(type=="기간별" && start_date==""){
        alert("시작 일자를 선택해주세요.");
        return;
    } else if(type=="기간별" && end_date==""){
        return;
    }

    $.ajax({
        url: '/api/daily/?' + $.param({
            platform: platform,
            type: type,
            start_date: start_date,
            end_date: end_date,
        }),
        type: 'GET',
        datatype:'json',
        contentType: 'application/json; charset=utf-8',
        beforeSend: function(){ 
            $('#platform-title').text(platform+' 리포트');
            $('#overlay').fadeIn(300)
        },
        success: res => {
            let data_list = [];
            let artist_list = [];
            data_list = res.data //필터링 데이터
            artist_list = res.artists //DB 아티스트 리스트
            platform_header = res.platform //수집 항목


            console.log(data_list);


            let crawling_artist_list = [] //크롤링 된 아티스트 리스트
            crawling_artist_list = res.crawling_artist_list

            let db_artist_list = [] //DB 에 있는 아티스트 리스트
            for (let i = 0; i<artist_list.length; i++){
                db_artist_list.push(artist_list[i]);
            }

            console.log(platform_header);
            $('#overlay').fadeOut(300)

            $('#data-report-headers').eq(0).empty();
            $('#board').eq(0).empty();
            if(type === '누적'){
                $('#update-data').show();
            } else{
                $('#update-data').hide();
            }
            $('#platform-title').text(platform+' 리포트');
            if(res.data === 'no data'){
                showEmptyTable(platform_header,db_artist_list,crawling_artist_list)
            } else{
                showCrawledData(type,platform_header,data_list,db_artist_list,crawling_artist_list)
            }
        },
        error: e => {
            $('#overlay').fadeOut(300)
            console.log(e);
            if(type === '누적'){
                alert('데이터를 불러올 수 없습니다.')
            }
            if(type === '기간별'){
                var result = JSON.parse(e.responseText);
                alert(result.data+ ' 에 데이터가 없습니다. 날짜를 조정해주세요.');
                $('#data-report-headers').eq(0).empty();
                $('#board').eq(0).empty();
            }
        },
    })
}

function ajax_only(type,platform,start_date,end_date){
    $.ajax({
        url: '/api/daily/?' + $.param({
            platform: platform,
            type: type,
            start_date: start_date,
            end_date: end_date,
        }),
        type: 'GET',
        datatype:'json',
        contentType: 'application/json; charset=utf-8',
        beforeSend: function(){ 
            $('#platform-title').text(platform+' 리포트');
            $('#overlay').fadeIn(300)
        },
        success: res => {
            let data_list = [];
            let artist_list = [];
            data_list = res.data //필터링 데이터
            artist_list = res.artists //DB 아티스트 리스트
            platform_header = res.platform //수집 항목


            console.log(data_list);


            let crawling_artist_list = [] //크롤링 된 아티스트 리스트
            crawling_artist_list = res.crawling_artist_list

            let db_artist_list = [] //DB 에 있는 아티스트 리스트
            for (let i = 0; i<artist_list.length; i++){
                db_artist_list.push(artist_list[i]);
            }

            console.log(platform_header);
            $('#overlay').fadeOut(300)

            $('#data-report-headers').eq(0).empty();
            $('#board').eq(0).empty();
            if(type === '누적'){
                $('#update-data').show();
            } else{
                $('#update-data').hide();
            }
            $('#platform-title').text(platform+' 리포트');
            if(res.data === 'no data'){
                showEmptyTable(platform_header,db_artist_list,crawling_artist_list)
            } else{
                showCrawledData(type,platform_header,data_list,db_artist_list,crawling_artist_list)
            }
        },
        error: e => {
            $('#overlay').fadeOut(300)
            console.log(e);
            if(type === '누적'){
                alert('데이터를 불러올 수 없습니다.')
            }
            if(type === '기간별'){
                var result = JSON.parse(e.responseText);
                alert(result.data+ ' 에 데이터가 없습니다. 날짜를 조정해주세요.');
                $('#data-report-headers').eq(0).empty();
                $('#board').eq(0).empty();
            }
        },
    })
}


var Month = ['None','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
var MonthNum = ['None','1','2','3','4','5','6','7','8','9','10','11','12']
function parsingDate(date){
    var splited_list = date.split(' ')
    var index = Month.indexOf(splited_list[0])
    var result = ''
    if (index < 0){
        return splited_list[0] //YYYY-MM-DD 형태로 반환
    } else{
        result = splited_list[2] + '-' + MonthNum[index] + '-' + splited_list[1].slice(0, -3); 
        return result
    }
}

//date setting

function addDays(date, days) { 
    const clone = new Date(date); 
    clone.setDate(date.getDate() + days) 
    return clone; 
}

//refresh button
function refresh(){
    $('input[name=start_date]').val("");
    $('input[name=end_date]').val("");
}

$(document).on('click','input[name=refresh]',function(){
    $('input').not($(this)).removeClass("date-selected");  
    refresh();
})

//date input change button

  $(document).on('click','input[name=day]',function(){
    if($(this).hasClass("date-selected")){
        $(this).removeClass("date-selected");
    }else{
        $(this).addClass("date-selected");
        $('input').not($(this)).removeClass("date-selected");  
    }
    var today = new Date();
    var yesterday = new Date(today.setDate(today.getDate() -1 ));
    const next_day = addDays(yesterday,0);
    var year = next_day.getFullYear();
    var month = ("0" + (1 + next_day.getMonth())).slice(-2);
    var day = ("0" + next_day.getDate()).slice(-2);
    $('input[name=start_date]').val(year+'-'+month+'-'+day);
    year = yesterday.getFullYear();
    month = ("0" + (1 + yesterday.getMonth())).slice(-2);
    day = ("0" + yesterday.getDate()).slice(-2);
    $('input[name=end_date]').val(year+'-'+month+'-'+day);

    var platform = $(".contents-platforms").find('.platform-selected').val(); 
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();
    var type = $(':radio[name="view_days"]:checked').val();

    goTop()
    ajax(type,platform,start_date,end_date)
 })
 
 $(document).on('click','input[name=week]',function(){
    if($(this).hasClass("date-selected")){
        $(this).removeClass("date-selected");
    }else{
        $(this).addClass("date-selected");
        $('input').not($(this)).removeClass("date-selected");  
    }
     var today = new Date();
    var yesterday = new Date(today.setDate(today.getDate() -1 ));
     const next_day = addDays(yesterday,-6);
     var year = next_day.getFullYear();
     var month = ("0" + (1 + next_day.getMonth())).slice(-2);
     var day = ("0" + next_day.getDate()).slice(-2);
     $('input[name=start_date]').val(year+'-'+month+'-'+day);
     year = yesterday.getFullYear();
    month = ("0" + (1 + yesterday.getMonth())).slice(-2);
    day = ("0" + yesterday.getDate()).slice(-2);
    $('input[name=end_date]').val(year+'-'+month+'-'+day);

    var platform = $(".contents-platforms").find('.platform-selected').val(); 
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();
    var type = $(':radio[name="view_days"]:checked').val();

    goTop()
    ajax(type,platform,start_date,end_date)
  })
 
 $(document).on('click','input[name=month]',function(){
    if($(this).hasClass("date-selected")){
        $(this).removeClass("date-selected");
    }else{
        $(this).addClass("date-selected");
        $('input').not($(this)).removeClass("date-selected");  
    }
     var today = new Date();
     var yesterday = new Date(today.setDate(today.getDate() -1 ));
     const next_day = addDays(yesterday,-30);
     var year = next_day.getFullYear();
     var month = ("0" + (1 + next_day.getMonth())).slice(-2);
     var day = ("0" + next_day.getDate()).slice(-2);
     $('input[name=start_date]').val(year+'-'+month+'-'+day);
     year = yesterday.getFullYear();
     month = ("0" + (1 + yesterday.getMonth())).slice(-2);
     day = ("0" + yesterday.getDate()).slice(-2);
     $('input[name=end_date]').val(year+'-'+month+'-'+day); 


     var platform = $(".contents-platforms").find('.platform-selected').val(); 
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();
    var type = $(':radio[name="view_days"]:checked').val();

    goTop()
    ajax(type,platform,start_date,end_date)
  })


//create Table header
const createTableHeader = (type,platform_header) => {
    const tableHeader = $('<tr></tr>');
   if(type === '누적'){

        let c = $('<th></th>', {
            text:'artist',
            class:"border-0"
        })
        tableHeader.append(c)
        for(let i = 0; i< platform_header.length; i++){
            let col = $('<th></th>', {
                text: platform_header[i],
                class:"border-0"
            })
            tableHeader.append(col)
        }

   } else{
        let c = $('<th></th>', {
            text:'artist',
            class:"border-0"
        })
        tableHeader.append(c)
        for(let i = 0; i< platform_header.length; i++){
            if(platform_header[i] === 'user_created'){
                let col = $('<th></th>', {
                    text: platform_header[i],
                    class:"border-0"
                })
                tableHeader.append(col)
            } else{
                let col = $('<th></th>', {
                    text: platform_header[i],
                    class:"border-0"
                })
                tableHeader.append(col)
                col = $('<th></th>', {
                    text: platform_header[i] +' 의 증감 내역',
                    class:"border-0"
                })
                tableHeader.append(col)
            }
        }

   }
    return tableHeader;
}

const createRow = (type,datas, platform_list,db_artist_list, crawling_artist_list) => {
    var artist_has_value = [];
    for(var i = 0; i<datas.length; i++){
        artist_has_value.push(datas[i]['artist'])
    }

    for(var i = 0; i<db_artist_list.length; i++){
        const tableRow = $('<tr></tr>')
        if(artist_has_value.includes(db_artist_list[i])){
            let dataCol = $('<th></th>', {
                text:db_artist_list[i],
            })
            tableRow.append(dataCol)
            var jsonIdx = datas.findIndex(function(key) {return key["artist"] === db_artist_list[i]});
            for(let j =0; j<platform_list.length; j++){
                let dataCol;
                let dataCol_0 = ''
                if(type === '누적'){
                    if((datas[jsonIdx][platform_list[j]] || datas[jsonIdx][platform_list[j]]===0)){
                        if(!isString(datas[jsonIdx][platform_list[j]])){
                            dataCol = $('<td><input class="data-input" type="text" value="'+numToString(datas[jsonIdx][platform_list[j]])+'" style="width:100%; text-align:end; background-color: #f8f9fa; border:0;"></input></td>')
                        } else{ //string 인 경우
                            if(platform_list[j] === 'user_created'){
                                dataCol = $('<td><input class="data-input" type="text" value="'+parsingDate(datas[jsonIdx][platform_list[j]])+'" style="width:100%; text-align:center; background-color: #f8f9fa; border:0;"></input></td>')
                            } else{
                                dataCol = $('<td><input class="data-input" type="text" value="'+datas[jsonIdx][platform_list[j]]+'" style="width:100%; text-align:center; background-color: #f8f9fa; border:0;"></input></td>')
                            }
                        }
                    }
                    else{
                        dataCol = $('<td> <input class="data-input" type="text" value="" style="width:100%; background-color: #f8f9fa; border:0;"></input></td>')
                    }
                } else{ //기간별일 때는 수정 불가능
                    if(datas[jsonIdx][platform_list[j]] || datas[jsonIdx][platform_list[j]]===0){
                        if(!isString(datas[jsonIdx][platform_list[j]])){
                            if(datas[jsonIdx][platform_list[j]] >0 ){
                                if(datas[jsonIdx][platform_list[j]+'_end']){
                                    dataCol_0 = $('<td style="font-weight:bold;">'+numToString(datas[jsonIdx][platform_list[j]+'_end']) +'</td>')
                                    dataCol = $('<td style="font-weight:bold;">'+ ' <span style="color:#E11D48;"><i class="fas fa-caret-up"></i> '+numToString(datas[jsonIdx][platform_list[j]])+'</span></td>')
                                } else{
                                    dataCol_0 = $('<td style="font-weight:bold;">'+numToString(datas[jsonIdx][platform_list[j]]) +'</td>')
                                    dataCol = $('<td style="font-weight:bold;">'+' <span style="color:#E11D48;"><i class="fas fa-caret-up"></i> '+numToString(datas[jsonIdx][platform_list[j]])+'</span></td>')
                                }
                            } else if(datas[jsonIdx][platform_list[j]] < 0 ){ //음수
                                dataCol_0 = $('<td style="font-weight:bold;">'+numToString(datas[jsonIdx][platform_list[j]+'_end']) +'</td>')
                                dataCol = $('<td style="font-weight:bold;">'+' <span style="color:#2361ce; "><i class="fas fa-caret-down"></i> '+numToString(Math.abs(datas[jsonIdx][platform_list[j]]))+'</span></td>')
                            } else{
                                if(typeof(datas[jsonIdx][platform_list[j]+'_end']) == 'undefined'){
                                    dataCol_0 = $('<td style="font-weight:bold;">'+numToString(datas[jsonIdx][platform_list[j]]) +'</td>')
                                } else{
                                    dataCol_0 = $('<td style="font-weight:bold;">'+numToString(datas[jsonIdx][platform_list[j]+'_end']) +'</td>')
                                }
                                dataCol = $('<td>-</td>')
                            }
                        } else{
                            dataCol = $('<td></td>',{
                                text: parsingDate(datas[jsonIdx][platform_list[j]])
                            })
                        }
                    }
                    else{
                        dataCol = $('<td></td>')
                    } 
                }
                if(dataCol_0 == ''){
                    tableRow.append(dataCol)
                } else{
                    tableRow.append(dataCol_0)
                    tableRow.append(dataCol)
                }
            }

        } else if(crawling_artist_list.includes(db_artist_list[i])){
            let dataCol = $('<th></th>', {
                text:db_artist_list[i],
            })
            tableRow.append(dataCol)
            for(let j =0; j<platform_list.length; j++){
                //console.log(crawling_artist_list.indexOf(db_artist_list[i]));
                let dataCol;
                let dataCol_0 = '';
                if(type == '누적'){
                    dataCol = $('<td><input class="data-input" type="text" value="'+'" style="width:100%; background-color: #f8f9fa; border:0;"></input></td>')
                    tableRow.append(dataCol)
                } else{
                    if(platform_list[j] === 'user_created'){
                        dataCol = $('<td>-</td>')
                        tableRow.append(dataCol)
                    } else{
                        dataCol_0 = $('<td>-</td>')
                        tableRow.append(dataCol_0)
                        dataCol = $('<td>-</td>')
                        tableRow.append(dataCol)
                    }
                }
            }
        } else{
            let dataCol = $('<th></th>', {
                text: db_artist_list[i],
            })
            tableRow.append(dataCol)
            for(let j =0; j<platform_list.length; j++){
                if(type == '누적'){
                    let dataCol = $('<td><input class="data-input" type="text" value="" style="width:100%; background-color: #E5E7EB; border:0;" disabled></input></td>')
                    tableRow.append(dataCol)
                } else{
                    if(platform_list[j] === 'user_created'){
                        dataCol = $('<td><input class="data-input" type="text" value="" style="width:100%; background-color: #E5E7EB; border:0;" disabled></input></td>')
                        tableRow.append(dataCol)
                    } else{
                        dataCol_0 = $('<td><input class="data-input" type="text" value="" style="width:100%; background-color: #E5E7EB; border:0;" disabled></input></td>')
                        tableRow.append(dataCol_0)
                        dataCol = $('<td><input class="data-input" type="text" value="" style="width:100%; background-color: #E5E7EB; border:0;" disabled></input></td>')
                        tableRow.append(dataCol)
                    }
                }
            }
        }
        $('#board').append(tableRow);
    }
}


//create Rows for empty case (누적 일 때만)
const createEmptyRow = (platform_list,db_artist_list, crawling_artist_list) => {
    for(let i = 0; i< db_artist_list.length; i++){
        const tableRow = $('<tr></tr>')
        if(crawling_artist_list.includes(db_artist_list[i])){
            let dataCol = $('<th></th>', {
                text:db_artist_list[i],
            })
            tableRow.append(dataCol)
            for(let j =0; j<platform_list.length; j++){
                //console.log(crawling_artist_list.indexOf(db_artist_list[i]));
                let dataCol;
                dataCol = $('<td><input class="data-input" type="text" value="'+'" style="width:100%; background-color: #f8f9fa; border:0;"></input></td>')
                tableRow.append(dataCol)
            }
        } else{
            let dataCol = $('<th></th>', {
                text: db_artist_list[i],
            })
            tableRow.append(dataCol)
            for(let j =0; j<platform_list.length; j++){
                let dataCol = $('<td><input class="data-input" type="text" value="" style="width:100%; background-color: #E5E7EB; border:0;" disabled></input></td>')
                tableRow.append(dataCol)
            }
        }
        $('#board').append(tableRow);
    }
    
}


//show crawled data
const showCrawledData = (type,platform_list,datas,db_artist_list,crawling_artist_list) => {
    if(type === '누적'){
        $('#table').css('width','70%');
    } else{
        $('#table').css('width','95%');
    }
    $('#data-report-headers').append(createTableHeader(type,platform_list));
    createRow(type,datas,platform_list,db_artist_list,crawling_artist_list);
}


//show empty table (when data is none) (누적 일 때만 사용)
const showEmptyTable = (platform_list,db_artist_list,crawling_artist_list) => {
    var type = '누적' 
    $('#table').css('width','70%');
    $('#data-report-headers').append(createTableHeader(type,platform_list));
    createEmptyRow(platform_list,db_artist_list,crawling_artist_list);
}

//change color of button when clicking platform
$('option').click(function(){
    if($(this).hasClass("platform-selected")){
      $(this).removeClass("platform-selected");
    }else{
      $(this).addClass("platform-selected");
      $('option').not($(this)).removeClass("platform-selected");  
    }
});

//누적 일 때 다른 버튼 안보이게
//누적 & 기간별 ajax 작동
$(document).on('change','input[type=radio]',function(){
    goTop()
    var type = $(':radio[name="view_days"]:checked').val();
    if(type === '누적'){
        $('input[name=end_date]').hide()
        $('input[name=day]').hide()
        $('input[name=week]').hide()
        $('input[name=month]').hide()
    } else{
        $('input[name=end_date]').show()
        $('input[name=day]').show()
        $('input[name=week]').show()
        $('input[name=month]').show()
        $('input[name=start_date]').val("");
        $('input[name=end_date]').val("");
        $('input[name=day]').addClass('date-selected') //1일 default
        var today = new Date();
        var yesterday = new Date(today.setDate(today.getDate() -1 ));
        document.getElementById('start_date').valueAsDate = yesterday
        document.getElementById('end_date').valueAsDate = yesterday
    }
    changedDatas = [];
    var platform = $(".contents-platforms").find('.platform-selected').val(); 
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();
    ajax(type,platform,start_date,end_date)
})


//when change date(only platform button clicked)
$(document).on('change','#start_date',function(){
    goTop()
    var platform = $(".contents-platforms").find('.platform-selected').val(); 
    var type = $(':radio[name="view_days"]:checked').val();
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();
    
    changedDatas = [];

    if(!platform){
        return false;
    } 

    if(type == undefined){
        alert("누적/기간별 중 선택해주세요.");
        return;
    }else if(type=="누적" && start_date==""){
        alert("시작 일자를 선택해주세요.");
        return;
    } else if(type=="기간별" && start_date==""){
        alert("시작 일자를 선택해주세요.");
        return;
    } else if(type=="기간별" && end_date==""){
        return;
    }

    ajax_only(type,platform,start_date,end_date)
})

$(document).on('change','#end_date',function(){
    goTop()
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();
    var date1 = new Date(start_date);
    var date2 = new Date(end_date);
    var type = $(':radio[name="view_days"]:checked').val();
    if(type =="기간별" && date2 < date1){
        alert('시작 일자를 종료 일자보다 과거로 입력하세요.');
        return;
    }
    var platform = $(".contents-platforms").find('.platform-selected').val(); //platform name
    console.log(platform);
    if(!platform){
        return false;
    } 
    changedDatas = [];
    if(type == undefined){
        alert("누적/기간별 중 선택해주세요.");
        return;
    }else if(type=="누적" && start_date==""){
        alert("시작 일자를 선택해주세요.");
        return;
    } 

  ajax_only(type,platform,start_date,end_date)
})



//when clicking platform name
$(document).on('click','.platform-name',function(){

    goTop()
    var platform = $(this).val();
    var type = $(':radio[name="view_days"]:checked').val();
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();


    if(type == undefined){
        alert('누적/기간별을 설정하세요.')
        return;
    }else if(type=="누적" && start_date==""){
        alert('시작 일자를 설정하세요.')
        return;
    }else if(type=="기간별" && start_date==""){
        alert('시작 일자를 설정하세요.')
        return;
    }else if(type=="기간별" && start_date && end_date == ""){
        alert('종료 일자를 설정하세요.')
        return;
    }

    changedDatas = [];
    ajax_only(type,platform,start_date,end_date)
})


//input change detection
let changedDatas = [];
$(document).on('focus', '.data-input' ,function(){
    $(this).data('val', $(this).val());
});

$(document).on('change','.data-input' ,function(){
    var thisRow = $(this).closest('tr').find('th');  
    var colIdx = $(this).closest("td").index();
    var target = $(`th:eq(${colIdx})`).text();
    var artist = thisRow[0].innerHTML;
    var prev = $(this).data('val');
    var current = $(this).val();



    //최근 수정 항목만 살리기
    const itemToFind = changedDatas.find(function(item) {return item.artist === artist && item.target === target})
    const idx = changedDatas.indexOf(itemToFind)
    if (idx > -1){
        changedDatas.splice(idx, 1)
    }

    //최근 항목만 넣기
    changedDatas.push({
        'artist':artist,
        'target':target,
        'prev':prev,
        'current':uncomma(current), //콤마가 찍히지 않은 숫자 
        'comma_current': current, //콤마가 찍힌 숫자(view 용)
    })


});


//update crawled data(confirm button)
$('#update-data').click(function(){
    //modal find
    var modal = $('div').find('.modal')
    if(modal.hasClass('show')){
        modal.removeClass('show');
        modal.css('display','none');
    } else{
        modal.addClass('show');
        modal.css('display','block');
    }

    changedDatas.forEach(data => {
        const tableRow = $('<tr></tr>')
        for(key in data) {
            if(key === 'current'){
                continue;
            }
            let dataCol;

            dataCol = $('<td></td>', {
                text: data[key],
            })

            tableRow.append(dataCol)
        }
        $('#changed-data-list').append(tableRow);
    })



})

$('.btn-close').click(function(){
    var modal = $('div').find('.modal')
    if(modal.hasClass('show')){
        modal.removeClass('show');
        modal.css('display','none');
    } 
    changedDatas = [];
    $('#changed-data-list').eq(0).empty();
    var platform = $(".contents-platforms").find('.platform-selected').val(); 
    var type = $(':radio[name="view_days"]:checked').val();
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();

    goTop()
    ajax_only(type,platform,start_date,end_date)

})

$('.btn-close-2').click(function(){
    var modal = $('div').find('.modal')
    if(modal.hasClass('show')){
        modal.removeClass('show');
        modal.css('display','none');
    } 
    $('#changed-data-list').eq(0).empty();
    changedDatas = [];
    var platform = $(".contents-platforms").find('.platform-selected').val(); 
    var type = $(':radio[name="view_days"]:checked').val();
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();

    goTop()
   ajax_only(type,platform,start_date,end_date)
})

$('#update').click(function(){
    var type = $(':radio[name="view_days"]:checked').val(); //type (누적별)
    var platform_name = $(".contents-platforms").find('.platform-selected').val(); //platform name
    var start_date = $('input[name=start_date]').val(); //date to change data
    var allArtists= $('#board').find('th'); //all artist list
    var th = $('#data-report-headers').find('tr').children();
    var targets = [];

    for(var i = 1; i< th.length; i++){ //target 이름
        targets.push(th[i].innerHTML);
    } 

    var changedDatasArtists = []; //바뀐 값이 있는 아티스트
    changedDatas.forEach(data => {
        changedDatasArtists.push(data['artist'])
    })

    let jsonFieldDatas = []; //보낼 데이터
    for(var i = 0; i<allArtists.length; i++){
        if(changedDatasArtists.includes(allArtists[i].innerHTML)){
            var element = {};
            element['artist'] = allArtists[i].innerHTML;
            element['reserved_date'] = start_date;
            element['platform'] = platform_name;
            for (var j=0; j<targets.length; j++){
                if(targets[j] !== 'user_created'){
                    element[targets[j]] =  Number(uncomma($('#board').find(`tr:eq(${i})`).find(`td:eq(${j})`).find('input.data-input').val()))
                } else{
                    element[targets[j]] = $('#board').find(`tr:eq(${i})`).find(`td:eq(${j})`).find('input.data-input').val()
                }
            }
            jsonFieldDatas.push(element)
        }
    }

    jsonFieldDatas.push({
        'platform_name':platform_name,
        'start_date':start_date
    })

    console.log(jsonFieldDatas);


    //modal 닫기
    var modal = $('div').find('.modal')
    if(modal.hasClass('show')){
        modal.removeClass('show');
        modal.css('display','none');
    } 

    //update or create
    $.ajax({
        url: '/api/daily/',
        type: 'POST',
        datatype:'json',
        data: JSON.stringify(jsonFieldDatas),
        beforeSend: function(){
            $('#data-report-headers').eq(0).empty();
            $('#board').eq(0).empty();
            $('#overlay').fadeIn(300)
        },
        success: res => {
            alert("저장되었습니다.");
            $('#overlay').fadeOut(300);

            $('#changed-data-list').eq(0).empty();
            changedDatas = [];

            let data_list = [];
            let artist_list = [];
            data_list = res.data //필터링 데이터
            artist_list = res.artists //DB 아티스트 리스트
            platform_header = res.platform //수집 항목

            let crawling_artist_list = [] //크롤링 된 아티스트 리스트
            crawling_artist_list = res.crawling_artist_list

            console.log(crawling_artist_list);

            let db_artist_list = [] //DB 에 있는 아티스트 리스트
            for (let i = 0; i<artist_list.length; i++){
                db_artist_list.push(artist_list[i]);
            }

            console.log(platform_header);

            $('#data-report-headers').eq(0).empty();
            $('#board').eq(0).empty();
            if(type === '누적'){
                $('#update-data').show();
            } else{
                $('#update-data').hide();
            }
            $('#platform-title').text(platform_name+' 리포트');
            if(res.data === 'no data'){
                showEmptyTable(platform_header,db_artist_list,crawling_artist_list)
            } else{
                showCrawledData(type,platform_header,data_list,db_artist_list,crawling_artist_list)
            }
        },
        error: e => {
            $('#overlay').fadeOut(300)
            console.log(e);
            if(type === '누적'){
                alert('데이터를 저장하는데 실패했습니다.')
            }
            if(type === '기간별'){
                var result = JSON.parse(e.responseText);
                alert(result.data+ ' 에 데이터가 없습니다. 날짜를 조정해주세요.');
            }
        },
    })


    
   
   
})



//excel popup
$("#excel-form-open1").click(function(){
    document.getElementById("excel_form1").style.display = "flex";
    document.getElementById("excel_form2").style.display = "none";
    document.getElementById("excel_form3").style.display = "none";
    document.getElementById("excel_form4").style.display = "none";
    document.getElementById('excel_loading1').classList.add("hidden");
});
$("#excel-form-open2").click(function(){
    document.getElementById("excel_form1").style.display = "none";
    document.getElementById("excel_form2").style.display = "flex";
    document.getElementById("excel_form3").style.display = "none";
    document.getElementById("excel_form4").style.display = "none";
    document.getElementById('data_excel_download_form').style.display = "block";
    document.getElementById('data_excel_download_span').style.display = "none";
});
$("#excel-form-open3").click(function(){
    document.getElementById("excel_form1").style.display = "none";
    document.getElementById("excel_form2").style.display = "none";
    document.getElementById("excel_form3").style.display = "flex";
    document.getElementById("excel_form4").style.display = "none";
    document.getElementById('excel_loading3').classList.add("hidden");
});
$("#excel-form-open4").click(function(){
    document.getElementById("excel_form1").style.display = "none";
    document.getElementById("excel_form2").style.display = "none";
    document.getElementById("excel_form3").style.display = "none";
    document.getElementById("excel_form4").style.display = "flex";
    document.getElementById('excel_loading4').classList.add("hidden");
});

document.getElementById('close_button1').onclick = function(){
    document.getElementById("excel_form1").style.display = "none";
    document.getElementById('excel_loading1').classList.add("hidden");
}
document.getElementById('close_button2').onclick = function(){
    document.getElementById("excel_form2").style.display = "none";
}
document.getElementById('close_button3').onclick = function(){
    document.getElementById("excel_form3").style.display = "none";
    document.getElementById('excel_loading3').classList.add("hidden");
}
document.getElementById('close_button4').onclick = function(){
    document.getElementById("excel_form4").style.display = "none";
    document.getElementById('excel_loading4').classList.add("hidden");
}

document.getElementById('excel-btn1').onclick = function(){
    document.getElementById('excel_loading1').classList.remove("hidden");
}
document.getElementById('excel-btn2').onclick = function(){
    
}
document.getElementById('excel-btn3').onclick = function(){
    document.getElementById('excel_loading3').classList.remove("hidden");
}
document.getElementById('excel-btn4').onclick = function(){
    document.getElementById('excel_loading4').classList.remove("hidden");
}

// default 누적 & today 설정
var today = new Date();
var yesterday = new Date(today.setDate(today.getDate() -1 ));
document.getElementById('excel_import_date').valueAsDate = yesterday;
document.getElementById('excel_export_start_date').valueAsDate = yesterday;
document.getElementById('start_date').valueAsDate = yesterday;
document.getElementById('end_date').valueAsDate = yesterday;
document.getElementById('excel_export_date_text').style.display = "none";
document.getElementById('excel_export_end_date').style.display = "none";
document.getElementById('excel_export_days1').onclick = function(){
    //excel form - 누적 선택
    document.getElementById('excel_export_date_text').style.display = "none";
    document.getElementById('excel_export_end_date').style.display = "none";
}
document.getElementById('excel_export_days2').onclick = function(){
    //excel form - 기간별 선택
    document.getElementById('excel_export_end_date').valueAsDate = yesterday;
    document.getElementById('excel_export_date_text').style.display = "block";
    document.getElementById('excel_export_end_date').style.display = "block";
}
//default 누적 & end_date 안보이게
$('input[name=end_date]').hide()
$('input[name=day]').hide()
$('input[name=week]').hide()
$('input[name=month]').hide()

document.getElementById('excel-btn2').onclick = function(){
    document.getElementById('data_excel_download_form').style.display = "none";
    document.getElementById('data_excel_download_span').style.display = "block";
}