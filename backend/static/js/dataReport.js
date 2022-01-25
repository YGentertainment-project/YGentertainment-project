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
    if(typeof inputText === 'string' || inputText instanceof String){
        //it is string
        return true;    
    }else{
        //it is not string
        return false;
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
    refresh();
})
 

 $(document).on('click','input[name=day]',function(){
    const today = new Date();
    const next_day = addDays(today,0);
    var year = next_day.getFullYear();
    var month = ("0" + (1 + next_day.getMonth())).slice(-2);
    var day = ("0" + next_day.getDate()).slice(-2);
    $('input[name=start_date]').val(year+'-'+month+'-'+day);
    year = today.getFullYear();
    month = ("0" + (1 + today.getMonth())).slice(-2);
    day = ("0" + today.getDate()).slice(-2);
    $('input[name=end_date]').val(year+'-'+month+'-'+day);
 })
 
 $(document).on('click','input[name=week]',function(){
     const today = new Date();
     const next_day = addDays(today,-6);
     var year = next_day.getFullYear();
     var month = ("0" + (1 + next_day.getMonth())).slice(-2);
     var day = ("0" + next_day.getDate()).slice(-2);
     $('input[name=start_date]').val(year+'-'+month+'-'+day);
     year = today.getFullYear();
    month = ("0" + (1 + today.getMonth())).slice(-2);
    day = ("0" + today.getDate()).slice(-2);
    $('input[name=end_date]').val(year+'-'+month+'-'+day);
  })
 
 $(document).on('click','input[name=month]',function(){
     const today = new Date();
     const next_day = addDays(today,-30);
     var year = next_day.getFullYear();
     var month = ("0" + (1 + next_day.getMonth())).slice(-2);
     var day = ("0" + next_day.getDate()).slice(-2);
     $('input[name=start_date]').val(year+'-'+month+'-'+day);
     year = today.getFullYear();
     month = ("0" + (1 + today.getMonth())).slice(-2);
     day = ("0" + today.getDate()).slice(-2);
     $('input[name=end_date]').val(year+'-'+month+'-'+day); 
  })


//create Table header
const createTableHeader = (platform_header) => {
    const tableHeader = $('<tr></tr>');

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

    return tableHeader;
}


const createRow = (type,datas, platform_list,db_artist_list, crawling_artist_list) => {
    for(let i = 0; i< db_artist_list.length; i++){
        const tableRow = $('<tr></tr>')
        if(crawling_artist_list.includes(db_artist_list[i])){ //db 아티스트가 크롤링 된 아티스트 리스트 안에 있을 때
            let dataCol = $('<th></th>', {
                text:db_artist_list[i],
            })
            tableRow.append(dataCol)
            for(let j =0; j<platform_list.length; j++){
                let dataCol;
                if(type === '누적'){
                    if(datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]] || datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]]===0){
                        if(!isString(datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]])){
                            dataCol = $('<td><input class="data-input" type="text" value="'+numToString(datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]])+'" style="width:100%; text-align:end; background-color: #f8f9fa; border:0;"></input></td>')
                        } else{
                            dataCol = $('<td><input class="data-input" type="text" value="'+datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]]+'" style="width:100%; background-color: #f8f9fa; border:0;"></input></td>')
                        }
                    }
                    else{
                        dataCol = $('<td> <input class="data-input" type="text" value="" style="width:100%; background-color: #4B5563; border:0;" disabled></input></td>')
                    }
                } else{ //기간별일 때는 수정 불가능
                    if(datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]] || datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]]===0){
                        if(!isString(datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]])){
                            if(datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]] >0 ){
                                dataCol = $('<td style="color:#10B981; font-weight:bold;"><svg class="icon icon-xs me-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clip-rule="evenodd"></path></svg>'+numToString(datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]])+'</td>')
                            } else if(datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]] < 0 ){
                                dataCol = $('<td style="color:#E11D48; font-weight:bold;"><svg class="icon icon-xs me-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>'+numToString(datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]])+'</td>')
                            } else{
                                dataCol = $('<td>-</td>')
                            }
                        } else{
                            dataCol = $('<td></td>',{
                                text: datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]]
                            })
                        }
                    }
                    else{
                        dataCol = $('<td></td>')
                    } 
                }
                tableRow.append(dataCol)
            }
        } else{
            let dataCol = $('<th></th>', {
                text: db_artist_list[i],
            })
            tableRow.append(dataCol)
            for(let j =0; j<platform_list.length; j++){
                let dataCol = $('<td><input class="data-input" type="text" value="" style="width:100%; background-color: #4B5563; border:0;" disabled></input></td>')
                tableRow.append(dataCol)
            }
        }
        $('#board').append(tableRow);
    }
    
}

//create Rows for empty case
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
                let dataCol = $('<td><input class="data-input" type="text" value="" style="width:100%; background-color: #4B5563; border:0;" disabled></input></td>')
                tableRow.append(dataCol)
            }
        }
        $('#board').append(tableRow);
    }
    
}


//show crawled data
const showCrawledData = (type,platform_list,datas,db_artist_list,crawling_artist_list) => {
    $('#data-report-headers').append(createTableHeader(platform_list));
    createRow(type,datas,platform_list,db_artist_list,crawling_artist_list);
}


//show empty table (when data is none)
const showEmptyTable = (platform_list,db_artist_list,crawling_artist_list) => {
    $('#data-report-headers').append(createTableHeader(platform_list));
    createEmptyRow(platform_list,db_artist_list,crawling_artist_list);
}

//change color of button when clicking platform
$('option').click(function(){
    if($(this).hasClass("btn-gray-800")){
      $(this).removeClass("btn-gray-800");
    }else{
      $(this).addClass("btn-gray-800");  
      $('option').not($(this)).removeClass("btn-gray-800");  
    }
});

//누적 일 때 다른 버튼 안보이게
$(document).on('change','input[type=radio]',function(){
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
    }
})

$(document).on('change','input[name=view_days]',function(){
    var type = $(':radio[name="view_days"]:checked').val();
    if(type === '누적'){
        refresh();
    }
})


//when change date(only platform button clicked)
$(document).on('change','#start_date',function(){
    var platform = $(".contents-platforms").find('.btn-gray-800').val(); 
    var type = $(':radio[name="view_days"]:checked').val();
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();
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

    changedDatas = [];


    $.ajax({
        url: '/dataprocess/api/daily/?' + $.param({
            platform: platform,
            type: type,
            start_date: start_date,
            end_date: end_date,
        }),
        type: 'GET',
        datatype:'json',
        contentType: 'application/json; charset=utf-8',
        success: res => {
            let data_list = [];
            let artist_list = [];
            let platform_list = [];
            data_list = res.data //필터링 데이터
            artist_list = res.artists //DB 아티스트 리스트
            platform_header = res.platform //수집 항목


            console.log(data_list);


            let crawling_artist_list = [] //크롤링 된 아티스트 리스트
            if(res.data === 'no data'){
                crawling_artist_list = res.crawling_artist_list
            } else{
                for (let i = 0; i<data_list.length; i++){
                    crawling_artist_list.push(data_list[i]['artist']);
                }
            }

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
            $('#platform-title').text(platform+' 리포트');
            if(res.data === 'no data'){
                showEmptyTable(platform_header,db_artist_list,crawling_artist_list)
            } else{
                showCrawledData(type,platform_header,data_list,db_artist_list,crawling_artist_list)
            }
        },
        error: e => {
            console.log(e);
            if(type === '기간별'){
                var result = JSON.parse(e.responseText);
                alert(result.data+ ' 에 데이터가 없습니다. 날짜를 조정해주세요.');
            }
            location.reload();
        },
    })
})

$(document).on('change','#end_date',function(){
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();
    var date1 = new Date(start_date);
    var date2 = new Date(end_date);
    var type = $(':radio[name="view_days"]:checked').val();
    if(type =="기간별" && date2 < date1){
        alert('시작 일자를 종료 일자보다 과거로 입력하세요.');
        refresh();
        return;
    }
    var platform = $(".contents-platforms").find('.btn-gray-800').val(); //platform name
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

    $.ajax({
        url: '/dataprocess/api/daily/?' + $.param({
            platform: platform,
            type: type,
            start_date: start_date,
            end_date: end_date,
        }),
        type: 'GET',
        datatype:'json',
        contentType: 'application/json; charset=utf-8',
        success: res => {
            let data_list = [];
            let artist_list = [];
            let platform_list = [];
            data_list = res.data //필터링 데이터
            artist_list = res.artists //DB 아티스트 리스트
            platform_list = res.platform //수집 항목


            console.log(data_list);

            let crawling_artist_list = [] //크롤링 된 아티스트 리스트
            if(res.data === 'no data'){
                crawling_artist_list = res.crawling_artist_list
            } else{
                for (let i = 0; i<data_list.length; i++){
                    crawling_artist_list.push(data_list[i]['artist']);
                }
            }

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
            $('#platform-title').text(platform+' 리포트');
            showCrawledData(type,platform_header,data_list,db_artist_list,crawling_artist_list)
        },
        error: e => {
            console.log(e);
            if(type === '기간별'){
                var result = JSON.parse(e.responseText);
                alert(result.data+ ' 에 데이터가 없습니다. 날짜를 조정해주세요.');
            }
            location.reload();
        },
    })
})



//when clicking platform name
$(document).on('click','.platform-name',function(){
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

    $.ajax({
        url: '/dataprocess/api/daily/?' + $.param({
            platform: platform,
            type: type,
            start_date: start_date,
            end_date: end_date,
        }),
        type: 'GET',
        datatype:'json',
        contentType: 'application/json; charset=utf-8',
        success: res => {
            let data_list = [];
            let artist_list = [];
            let platform_list = [];
            data_list = res.data //필터링 데이터
            artist_list = res.artists //DB 아티스트 리스트
            platform_header = res.platform //수집 항목


            console.log(data_list);

            let crawling_artist_list = [] //크롤링 된 아티스트 리스트
            if(res.data === 'no data'){
                crawling_artist_list = res.crawling_artist_list
            } else{
                for (let i = 0; i<data_list.length; i++){
                    crawling_artist_list.push(data_list[i]['artist']);
                }
            }

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
            $('#platform-title').text(platform+' 리포트');
            if(res.data === 'no data'){
                showEmptyTable(platform_header,db_artist_list,crawling_artist_list)
            } else{
                showCrawledData(type,platform_header,data_list,db_artist_list,crawling_artist_list)
            }
        },
        error: e => {
            console.log(e);
            if(type === '기간별'){
                var result = JSON.parse(e.responseText);
                alert(result.data+ ' 에 데이터가 없습니다. 날짜를 조정해주세요.');
            }
            location.reload();
        },
    })


    
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
    var platform = $(".contents-platforms").find('.btn-gray-800').val(); 
    var type = $(':radio[name="view_days"]:checked').val();
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();


    $.ajax({
        url: '/dataprocess/api/daily/?' + $.param({
            platform: platform,
            type: type,
            start_date: start_date,
            end_date: end_date,
        }),
        type: 'GET',
        datatype:'json',
        contentType: 'application/json; charset=utf-8',
        success: res => {
            let data_list = [];
            let artist_list = [];
            let platform_list = [];
            data_list = res.data //필터링 데이터
            artist_list = res.artists //DB 아티스트 리스트
            platform_header = res.platform //수집 항목


            console.log(data_list);

            let crawling_artist_list = [] //크롤링 된 아티스트 리스트
            if(res.data === 'no data'){
                crawling_artist_list = res.crawling_artist_list
            } else{
                for (let i = 0; i<data_list.length; i++){
                    crawling_artist_list.push(data_list[i]['artist']);
                }
            }

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
            $('#platform-title').text(platform+' 리포트');
            if(res.data === 'no data'){
                showEmptyTable(platform_header,db_artist_list,crawling_artist_list)
            } else{
                showCrawledData(type,platform_header,data_list,db_artist_list,crawling_artist_list)
            }
        },
        error: e => {
            console.log(e);
            if(type === '기간별'){
                var result = JSON.parse(e.responseText);
                alert(result.data+ ' 에 데이터가 없습니다. 날짜를 조정해주세요.');
            }
            location.reload();
        },
    })

})

$('.btn-close-2').click(function(){
    var modal = $('div').find('.modal')
    if(modal.hasClass('show')){
        modal.removeClass('show');
        modal.css('display','none');
    } 
    $('#changed-data-list').eq(0).empty();
    changedDatas = [];
    var platform = $(".contents-platforms").find('.btn-gray-800').val(); 
    var type = $(':radio[name="view_days"]:checked').val();
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();

    $.ajax({
        url: '/dataprocess/api/daily/?' + $.param({
            platform: platform,
            type: type,
            start_date: start_date,
            end_date: end_date,
        }),
        type: 'GET',
        datatype:'json',
        contentType: 'application/json; charset=utf-8',
        success: res => {
            let data_list = [];
            let artist_list = [];
            let platform_list = [];
            data_list = res.data //필터링 데이터
            artist_list = res.artists //DB 아티스트 리스트
            platform_header = res.platform //수집 항목


            console.log(data_list);

            let crawling_artist_list = [] //크롤링 된 아티스트 리스트
            if(res.data === 'no data'){
                crawling_artist_list = res.crawling_artist_list
            } else{
                for (let i = 0; i<data_list.length; i++){
                    crawling_artist_list.push(data_list[i]['artist']);
                }
            }

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
            $('#platform-title').text(platform+' 리포트');
            if(res.data === 'no data'){
                showEmptyTable(platform_header,db_artist_list,crawling_artist_list)
            } else{
                showCrawledData(type,platform_header,data_list,db_artist_list,crawling_artist_list)
            }
        },
        error: e => {
            console.log(e);
            if(type === '기간별'){
                var result = JSON.parse(e.responseText);
                alert(result.data+ ' 에 데이터가 없습니다. 날짜를 조정해주세요.');
            }
            location.reload();
        },
    })

})

$('#update').click(function(){
    var type = $(':radio[name="view_days"]:checked').val(); //type (누적별)
    var platform_name = $(".contents-platforms").find('.btn-gray-800').val(); //platform name
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
                    element[targets[j]] =  uncomma($('#board').find(`tr:eq(${i})`).find(`td:eq(${j})`).find('input.data-input').val())
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
        url: '/dataprocess/api/daily/',
        type: 'POST',
        datatype:'json',
        data: JSON.stringify(jsonFieldDatas),
        success: res => {
            alert("저장되었습니다.");
            $('#changed-data-list').eq(0).empty();
            changedDatas = [];

            let data_list = [];
            let artist_list = [];
            data_list = res.data //필터링 데이터
            artist_list = res.artists //DB 아티스트 리스트
            platform_header = res.platform //수집 항목

            console.log(data_list);

            let crawling_artist_list = [] //크롤링 된 아티스트 리스트
            if(res.data === 'no data'){
                crawling_artist_list = res.crawling_artist_list
            } else{
                for (let i = 0; i<data_list.length; i++){
                    crawling_artist_list.push(data_list[i]['artist']);
                }
            }

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
            console.log(e);
            if(type === '기간별'){
                var result = JSON.parse(e.responseText);
                alert(result.data+ ' 에 데이터가 없습니다. 날짜를 조정해주세요.');
            }
            location.reload();
        },
    })
   
   
})



//excel popup
$("#excel-form-open1").click(function(){
    document.getElementById("excel_form1").style.display = "flex";
    document.getElementById("excel_form2").style.display = "none";
    document.getElementById("excel_form3").style.display = "none";
});
$("#excel-form-open2").click(function(){
    document.getElementById("excel_form1").style.display = "none";
    document.getElementById("excel_form2").style.display = "flex";
    document.getElementById("excel_form3").style.display = "none";
});
$("#excel-form-open3").click(function(){
    document.getElementById("excel_form1").style.display = "none";
    document.getElementById("excel_form2").style.display = "none";
    document.getElementById("excel_form3").style.display = "flex";
});

document.getElementById('close_button1').onclick = function(){
    document.getElementById("excel_form1").style.display = "none";
}
document.getElementById('close_button2').onclick = function(){
    document.getElementById("excel_form2").style.display = "none";
}
document.getElementById('close_button3').onclick = function(){
    document.getElementById("excel_form3").style.display = "none";
}

document.getElementById('excel-btn1').onclick = function(){
    document.getElementById('progress-bar__bar1').classList.add('active');
}
document.getElementById('excel-btn2').onclick = function(){
    document.getElementById('progress-bar__bar2').classList.add('active');
}
document.getElementById('excel-btn3').onclick = function(){
    document.getElementById('progress-bar__bar3').classList.add('active');
}

// default 누적 & today 설정
document.getElementById('excel_import_date').valueAsDate = new Date();
document.getElementById('excel_export_start_date').valueAsDate = new Date();
document.getElementById('start_date').valueAsDate = new Date();
document.getElementById('end_date').valueAsDate = new Date();
document.getElementById('excel_export_date_text').style.display = "none";
document.getElementById('excel_export_end_date').style.display = "none";
document.getElementById('excel_export_days1').onclick = function(){
    //excel form - 누적 선택
    document.getElementById('excel_export_date_text').style.display = "none";
    document.getElementById('excel_export_end_date').style.display = "none";
}
document.getElementById('excel_export_days2').onclick = function(){
    //excel form - 기간별 선택
    document.getElementById('excel_export_end_date').valueAsDate = new Date();
    document.getElementById('excel_export_date_text').style.display = "block";
    document.getElementById('excel_export_end_date').style.display = "block";
}
//default 누적 & end_date 안보이게
$('input[name=end_date]').hide()
$('input[name=day]').hide()
$('input[name=week]').hide()
$('input[name=month]').hide()

if(document.getElementById('alert') != null){
    alert(ocument.getElementById('alert').innerHTML);
}