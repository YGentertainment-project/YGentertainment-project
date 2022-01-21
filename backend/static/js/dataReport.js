//default checked
$(document).ready(function(){
    var type = $("input:radio[name='view_days']:checked"). val( );
    if(type === "누적"){
        $('input[name=end_date]').hide()
        $('input[name=day]').hide()
        $('input[name=week]').hide()
        $('input[name=month]').hide()
    }
})

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
                                dataCol = $('<td><svg class="icon icon-xs me-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clip-rule="evenodd"></path></svg>'+numToString(datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]])+'</td>')
                            } else if(datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]] < 0 ){
                                dataCol = $('<td><svg class="icon icon-xs me-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>'+numToString(datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]])+'</td>')
                            } else{
                                dataCol = $('<td></td>',{
                                    text: numToString(datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]])
                                })
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
                dataCol = $('<td><input type="text" value="'+'" style="width:100%; background-color: #f8f9fa; border:0;"></input></td>')
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
    $('.thead-light').append(createTableHeader(platform_list));
    createRow(type,datas,platform_list,db_artist_list,crawling_artist_list);
}


//show empty table (when data is none)
const showEmptyTable = (platform_list,db_artist_list,crawling_artist_list) => {
    $('.thead-light').append(createTableHeader(platform_list));
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

            $('thead').eq(0).empty();
            $('tbody').eq(0).empty();
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
            alert(e.responseText);
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

            $('thead').eq(0).empty();
            $('tbody').eq(0).empty();
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
            alert(e.responseText);
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

            $('thead').eq(0).empty();
            $('tbody').eq(0).empty();
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
            var result = JSON.parse(e.responseText);
            alert(result.data+ ' 에 데이터가 없습니다. 날짜를 조정해주세요.');
            $('#result-table').eq(0).empty();
        },
    })


    
})


//update crawled data
$('#update-data').click(function(){
    var type = $(':radio[name="view_days"]:checked').val();
    var platform_name = $(".contents-platforms").find('.btn-gray-800').val(); //platform name
    var th = $('#board').find('th');
    var trs_value = $('input[type=text]');    
    trs_value = trs_value.slice(3)
    var type = $(':radio[name="view_days"]:checked').val();
    var start_date = $('input[name=start_date]').val();

    for(var i = 0; i<trs_value.length; i++){
        if(trs_value[i].value === ""){
            trs_value[i].value = 0; //안채워진 값들은 0 으로 간주
        }
    }

    //youtube
    if(platform_name === 'youtube'){
        var artists = [];
        var uploads = [];
        var subscribers = [];
        var views = [];
        var user_creation = [];
        for(var i = 5; i< th.length ; i++){
            artists.push(th[i].innerHTML);
        }
        for(var i = 0 ; i < trs_value.length ; i+=4){
            uploads.push(uncomma(trs_value[i].value))
        }
        for(var i = 1 ; i < trs_value.length ; i+=4){
            subscribers.push(uncomma(trs_value[i].value))
        }
        for(var i = 2 ; i < trs_value.length ; i+=4){
            views.push(uncomma(trs_value[i].value))
        }
        for(var i = 3 ; i < trs_value.length ; i+=4){
            user_creation.push(trs_value[i].value)
        }
        console.log({'platform_name':platform_name,
        'artists[]':artists,
        'uploads[]' : uploads, 
        'subscribers[]': subscribers, 
        'views[]': views, 
        'user_creation[]': user_creation, 
        'start_date':start_date
        })
        $.ajax({
            type: 'POST',
            data : {'platform_name':platform_name,
            'artists[]':artists,
            'uploads[]' : uploads, 
            'subscribers[]': subscribers, 
            'views[]': views, 
            'user_creation[]': user_creation, 
            'start_date':start_date
            },
            url: '/dataprocess/api/daily/',
            success: res => {
                alert("Successfully save!");
                let data_list = [];
                let artist_list = [];
                data_list = res.data //필터링 데이터
                artist_list = res.artists //DB 아티스트 리스트
                platform_header = res.platform //수집 항목


                console.log(platform_header);



            let crawling_artist_list = [] //크롤링 된 아티스트 리스트
            for (let i = 0; i<data_list.length; i++){
                crawling_artist_list.push(data_list[i]['artist']);
            }

            let db_artist_list = [] //DB 에 있는 아티스트 리스트
            for (let i = 0; i<artist_list.length; i++){
                db_artist_list.push(artist_list[i]);
            }
            $('thead').eq(0).empty();
            $('tbody').eq(0).empty();
            if(type === '누적'){
                $('#update-data').show();
            } else{
                $('#update-data').hide();
            }
            $('#platform-title').text(platform_name+' 리포트');
            showCrawledData(type,platform_header,data_list,db_artist_list,crawling_artist_list)
            },
            error : function (e){
                console.log(e);
                alert(e.responseText);
            }
          });
    }

    //spotify 
     if(platform_name === 'spotify'){
        var artists = [];
        var listens = [];
        var followers = [];
        for(var i = 3; i< th.length ; i++){
            artists.push(th[i].innerHTML);
        }
        for(var i = 0 ; i < trs_value.length ; i+=2){
            listens.push(uncomma(trs_value[i].value))
        }
        for(var i = 1 ; i < trs_value.length ; i+=2){
            followers.push(uncomma(trs_value[i].value))
        }

        $.ajax({
            type: 'POST',
            data : {'platform_name':platform_name,
            'artists[]':artists,
            'listens[]' : listens, 
            'followers[]': followers, 
            'start_date': start_date
            },
            url: '/dataprocess/api/daily/',
            success: res => {
                alert("저장되었습니다.");
                let data_list = [];
                let artist_list = [];
                let platform_list = [];
                data_list = res.data //필터링 데이터
                artist_list = res.artists //DB 아티스트 리스트
                platform_header = res.platform //수집 항목


                console.log(data_list);



            let crawling_artist_list = [] //크롤링 된 아티스트 리스트
            for (let i = 0; i<data_list.length; i++){
                crawling_artist_list.push(data_list[i]['artist']);
            }

            let db_artist_list = [] //DB 에 있는 아티스트 리스트
            for (let i = 0; i<artist_list.length; i++){
                db_artist_list.push(artist_list[i]);
            }

            $('thead').eq(0).empty();
            $('tbody').eq(0).empty();
            if(type === '누적'){
                $('#update-data').show();
            } else{
                $('#update-data').hide();
            }
            $('#platform-title').text(platform_name+' 리포트');
            showCrawledData(type,platform_header,data_list,db_artist_list,crawling_artist_list)
            },
            error : function (e){
                console.log(e);
                alert(e.responseText);
            }
          });
    }


     //melon
     if(platform_name === 'melon'){
        var artists = [];
        var listens = [];
        var streams = [];
        for(var i = 3; i< th.length ; i++){
            artists.push(th[i].innerHTML);
        }
        for(var i = 0 ; i < trs_value.length ; i+=2){
            listens.push(uncomma(trs_value[i].value))
        }
        for(var i = 1 ; i < trs_value.length ; i+=2){
            streams.push(uncomma(trs_value[i].value))
        }
        
        $.ajax({
            type: 'POST',
            data : {'platform_name':platform_name,
            'artists[]':artists,
            'listens[]' : listens, 
            'streams[]': streams, 
            'start_date': start_date
            },
            url: '/dataprocess/api/daily/',
            success: res => {
                alert("저장되었습니다.");
                let data_list = [];
                let artist_list = [];
                let platform_list = [];
                data_list = res.data //필터링 데이터
                artist_list = res.artists //DB 아티스트 리스트
                platform_header = res.platform //수집 항목


            let crawling_artist_list = [] //크롤링 된 아티스트 리스트
            for (let i = 0; i<data_list.length; i++){
                crawling_artist_list.push(data_list[i]['artist']);
            }

            let db_artist_list = [] //DB 에 있는 아티스트 리스트
            for (let i = 0; i<artist_list.length; i++){
                db_artist_list.push(artist_list[i]);
            }
            $('thead').eq(0).empty();
            $('tbody').eq(0).empty();
            if(type === '누적'){
                $('#update-data').show();
            } else{
                $('#update-data').hide();
            }
            $('#platform-title').text(platform_name+' 리포트');
            showCrawledData(type,platform_header,data_list,db_artist_list,crawling_artist_list)
            },
            error : function (e){
                console.log(e);
                alert(e.responseText);
            }
          });
    }

    //vlive
    if(platform_name === 'vlive'){
        var artists = [];
        var members = [];
        var videos = [];
        var likes = [];
        var plays = [];
        for(var i = 5; i< th.length ; i++){
            artists.push(th[i].innerHTML);
        }
        for(var i = 0 ; i < trs_value.length ; i+=4){
            members.push(uncomma(trs_value[i].value))
        }
        for(var i = 1 ; i < trs_value.length ; i+=4){
            videos.push(uncomma(trs_value[i].value))
        }
        for(var i = 2 ; i < trs_value.length ; i+=4){
            likes.push(uncomma(trs_value[i].value))
        }
        for(var i = 3 ; i < trs_value.length ; i+=4){
            plays.push(uncomma(trs_value[i].value))
        }

        $.ajax({
            type: 'POST',
            data : {'platform_name':platform_name,
            'artists[]':artists,
            'members[]' : members, 
            'videos[]': videos, 
            'likes[]': likes,
            'plays[]':plays, 
            'start_date':start_date
            },
            url: '/dataprocess/api/daily/',
            success: res => {
                alert("저장되었습니다.");
                let data_list = [];
                let artist_list = [];
                let platform_list = [];
                data_list = res.data //필터링 데이터
                artist_list = res.artists //DB 아티스트 리스트
                platform_header= res.platform //수집 항목
    
                let crawling_artist_list = [] //크롤링 된 아티스트 리스트
                for (let i = 0; i<data_list.length; i++){
                    crawling_artist_list.push(data_list[i]['artist']);
                }
    
                let db_artist_list = [] //DB 에 있는 아티스트 리스트
                for (let i = 0; i<artist_list.length; i++){
                    db_artist_list.push(artist_list[i]);
                }

                $('thead').eq(0).empty();
                $('tbody').eq(0).empty();
                if(type === '누적'){
                    $('#update-data').show();
                } else{
                    $('#update-data').hide();
                }
                $('#platform-title').text(platform_name+' 리포트');
                showCrawledData(type,platform_header,data_list,db_artist_list,crawling_artist_list)
            },
            error : function (){
            }
          });
    }

    //instagram & facebook
    if(platform_name === 'instagram' || platform_name==='facebook'){
        var artists = [];
        var followers = [];
        for(var i = 2; i< th.length ; i++){
            artists.push(th[i].innerHTML);
        }
        for(var i = 0 ; i < trs_value.length ; i+=1){
            followers.push(uncomma(trs_value[i].value))
        }

        $.ajax({
            type: 'POST',
            data : {'platform_name':platform_name,
            'artists[]':artists,
            'followers[]' : followers,  
            'start_date':start_date
            },
            url: '/dataprocess/api/daily/',
            success: res => {
                alert("저장되었습니다.");
                let data_list = [];
                let artist_list = [];
                let platform_list = [];
                data_list = res.data //필터링 데이터
                artist_list = res.artists //DB 아티스트 리스트
                platform_header = res.platform //수집 항목
    
                let crawling_artist_list = [] //크롤링 된 아티스트 리스트
                for (let i = 0; i<data_list.length; i++){
                    crawling_artist_list.push(data_list[i]['artist']);
                }
    
                let db_artist_list = [] //DB 에 있는 아티스트 리스트
                for (let i = 0; i<artist_list.length; i++){
                    db_artist_list.push(artist_list[i]);
                }

                $('thead').eq(0).empty();
                $('tbody').eq(0).empty();
                if(type === '누적'){
                    $('#update-data').show();
                } else{
                    $('#update-data').hide();
                }
                $('#platform-title').text(platform_name+' 리포트');
                showCrawledData(type,platform_header,data_list,db_artist_list,crawling_artist_list)
            },
            error : function (){
            }
          });
    }

     //tiktok
     if(platform_name === 'tiktok'){
        var artists = [];
        var followers = [];
        var uploads = [];
        var likes = [];
        for(var i = 4; i< th.length ; i++){
            artists.push(th[i].innerHTML);
        }
        for(var i = 0 ; i < trs_value.length ; i+=3){
            followers.push(uncomma(trs_value[i].value))
        }
        for(var i = 1 ; i < trs_value.length ; i+=3){
            uploads.push(uncomma(trs_value[i].value))
        }
        for(var i = 2 ; i < trs_value.length ; i+=3){
            likes.push(uncomma(trs_value[i].value))
        }

        $.ajax({
            type: 'POST',
            data : {'platform_name':platform_name,
            'artists[]':artists,
            'uploads[]':uploads,
            'followers[]' : followers,  
            'likes[]' : likes,  
            'start_date':start_date,
            },
            url: '/dataprocess/api/daily/',
            success: res => {
                alert("저장되었습니다.");
                let data_list = [];
                let artist_list = [];
                data_list = res.data //필터링 데이터
                artist_list = res.artists //DB 아티스트 리스트
                platform_header = res.platform //수집 항목
    
                let crawling_artist_list = [] //크롤링 된 아티스트 리스트
                for (let i = 0; i<data_list.length; i++){
                    crawling_artist_list.push(data_list[i]['artist']);
                }
    
                let db_artist_list = [] //DB 에 있는 아티스트 리스트
                for (let i = 0; i<artist_list.length; i++){
                    db_artist_list.push(artist_list[i]);
                }

                $('thead').eq(0).empty();
                $('tbody').eq(0).empty();
                if(type === '누적'){
                    $('#update-data').show();
                } else{
                    $('#update-data').hide();
                }
                $('#platform-title').text(platform_name+' 리포트');
                showCrawledData(type,platform_header,data_list,db_artist_list,crawling_artist_list)
            },
            error : function (){
            }
          });

       
    }

     //twitter 1, 2
     if(platform_name === 'twitter' || platform_name==='twitter2'){
        var artists = [];
        var followers = [];
        var twits = [];
        var user_creation = [];
        for(var i = 4; i< th.length ; i++){
            artists.push(th[i].innerHTML);
        }
        for(var i = 0 ; i < trs_value.length ; i+=3){
            followers.push(uncomma(trs_value[i].value))
        }
        for(var i = 1 ; i < trs_value.length ; i+=3){
            twits.push(uncomma(trs_value[i].value))
        }
        for(var i = 2 ; i < trs_value.length ; i+=3){
            user_creation.push(trs_value[i].value)
        }

        $.ajax({
            type: 'POST',
            data : {'platform_name':platform_name,
            'artists[]':artists,
            'followers[]' : followers,  
            'twits[]' : twits,  
            'user_creation[]' : user_creation,  
            'start_date':start_date
            },
           url: '/dataprocess/api/daily/',
            success: res => {
                alert("저장되었습니다.");
                let data_list = [];
                let artist_list = [];
                let platform_list = [];
                data_list = res.data //필터링 데이터
                artist_list = res.artists //DB 아티스트 리스트
                platform_header = res.platform //수집 항목

                console.log(res.success);
    
                let crawling_artist_list = [] //크롤링 된 아티스트 리스트
                for (let i = 0; i<data_list.length; i++){
                    crawling_artist_list.push(data_list[i]['artist']);
                }
    
                let db_artist_list = [] //DB 에 있는 아티스트 리스트
                for (let i = 0; i<artist_list.length; i++){
                    db_artist_list.push(artist_list[i]);
                }

                $('thead').eq(0).empty();
                $('tbody').eq(0).empty();
                if(type === '누적'){
                    $('#update-data').show();
                } else{
                    $('#update-data').hide();
                }
                $('#platform-title').text(platform_name+' 리포트');
                showCrawledData(type,platform_header,data_list,db_artist_list,crawling_artist_list)
            },
            error : function (){
            }
          });
    }


    //weverse
    if(platform_name === 'weverse'){
        var artists = [];
        var weverses = [];
        for(var i = 2; i< th.length ; i++){
            artists.push(th[i].innerHTML);
        }
        for(var i = 0 ; i < trs_value.length ; i+=1){
            weverses.push(uncomma(trs_value[i].value))
        }

        $.ajax({
            type: 'POST',
            data : {'platform_name':platform_name,
            'artists[]':artists,
            'weverses[]' : weverses,  
            'start_date':start_date
            },
            url: '/dataprocess/api/daily/',
            success: res => {
                alert("저장되었습니다.");
                console.log(res.success);
                let data_list = [];
                let artist_list = [];
                data_list = res.data //필터링 데이터
                artist_list = res.artists //DB 아티스트 리스트
                platform_header= res.platform //수집 항목
    
                let crawling_artist_list = [] //크롤링 된 아티스트 리스트
                for (let i = 0; i<data_list.length; i++){
                    crawling_artist_list.push(data_list[i]['artist']);
                }
    
                let db_artist_list = [] //DB 에 있는 아티스트 리스트
                for (let i = 0; i<artist_list.length; i++){
                    db_artist_list.push(artist_list[i]);
                }

                $('thead').eq(0).empty();
                $('tbody').eq(0).empty();
                if(type === '누적'){
                    $('#update-data').show();
                } else{
                    $('#update-data').hide();
                }
                $('#platform-title').text(platform_name+' 리포트');
                showCrawledData(type,platform_header,data_list,db_artist_list,crawling_artist_list)
            },
            error : function (e){
                console.log(e);
            }
          });
    }


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
$("#excel-form-open1").on({
    mouseenter: function () {
        document.getElementById("excel-form-open-hint1").style.display = "grid";
    },
    mouseleave: function () {
        document.getElementById("excel-form-open-hint1").style.display = "none";
    }
});
$("#excel-form-open2").on({
    mouseenter: function () {
        document.getElementById("excel-form-open-hint2").style.display = "grid";
    },
    mouseleave: function () {
        document.getElementById("excel-form-open-hint2").style.display = "none";
    }
});
$("#excel-form-open3").on({
    mouseenter: function () {
        document.getElementById("excel-form-open-hint3").style.display = "grid";
    },
    mouseleave: function () {
        document.getElementById("excel-form-open-hint3").style.display = "none";
    }
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