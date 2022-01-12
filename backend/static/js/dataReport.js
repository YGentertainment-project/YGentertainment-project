//number format
function numToString(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

//uncomma string number
function uncomma(str) {
    str = String(str);
    return str.replace(/[^\d]+/g, '');
}

//date setting

function addDays(date, days) { 
    const clone = new Date(date); 
    clone.setDate(date.getDate() + days) 
    return clone; 
}

//refresh button
$(document).on('click','input[name=refresh]',function(){
    $('input[name=start_date]').val("");
    $('input[name=end_date]').val("");
 })
 

$(document).on('click','input[name=day]',function(){
    const today = new Date();
    const next_day = addDays(today,-1);
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
     const next_day = addDays(today,-7);
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
const createTableHeader = (platform_list) => {
    const tableHeader = $('<tr></tr>');

    let c = $('<th></th>', {
        text:'artist',
    })
    tableHeader.append(c)
    for(let i = 0; i< platform_list.length; i++){
        let col = $('<th></th>', {
            text: platform_list[i]['target_name'],
        })
        tableHeader.append(col)
    }

    return tableHeader;
}


const createRow = (datas, platform_list,db_artist_list, crawling_artist_list) => {
    for(let i = 0; i< db_artist_list.length; i++){
        const tableRow = $('<tr></tr>')
        if(crawling_artist_list.includes(db_artist_list[i])){
            let dataCol = $('<th></th>', {
                text:db_artist_list[i],
            })
            tableRow.append(dataCol)
            for(let j =0; j<platform_list.length; j++){
                //console.log(crawling_artist_list.indexOf(db_artist_list[i]));
                let dataCol = $('<td><input type="text" value="'+numToString(datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]['target_name']])+'" style="width:100%"></input></td>')
                tableRow.append(dataCol)
            }
        } else{
            let dataCol = $('<th></th>', {
                text: db_artist_list[i],
            })
            tableRow.append(dataCol)
            for(let j =0; j<platform_list.length; j++){
                let dataCol = $('<td> <input type="text" value="" style="width:100%; background-color:lightgray"></input></td>')
                tableRow.append(dataCol)
            }
        }
        $('#board').append(tableRow);
    }
    
}


//show crawled data
const showCrawledData = (platform_list,datas,db_artist_list,crawling_artist_list) => {
    $('#board').append(createTableHeader(platform_list));
    createRow(datas,platform_list,db_artist_list,crawling_artist_list);
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

//when clicking platform name
$(document).on('click','.platform-name',function(){
    var platform = $(this).val();
    var type = $(':radio[name="view_days"]:checked').val();
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();

    //console.log($(this).attr("name"));

    if(type == undefined){
        alert("누적/기간별 중 선택해주세요.");
        return;
    }else if(type=="누적" && start_date==""){
        alert("시작 날짜를 선택해주세요.");
        return;
    }else if(type=="기간별" && (start_date=="" ||end_date=="" )){
        alert("시작과 끝 날짜를 선택해주세요.");
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


            let crawling_artist_list = [] //크롤링 된 아티스트 리스트
            for (let i = 0; i<data_list.length; i++){
                crawling_artist_list.push(data_list[i]['artist']);
            }

            let db_artist_list = [] //DB 에 있는 아티스트 리스트
            for (let i = 0; i<artist_list.length; i++){
                db_artist_list.push(artist_list[i]);
            }

            //let difference = db_artist_list.filter(x => !crawling_artist_list.includes(x))  //db 에만 있는 아티스트


            $('tbody').eq(0).empty();
            $('#update-data').show();
            $('#platform-title').text(platform+' 리포트');
            showCrawledData(platform_list,data_list,db_artist_list,crawling_artist_list)
        },
        error: e => {
            console.log(e);
            alert(e.responseText);
        },
    })
})


//update crawled data
$('#update-data').click(function(){
    var type = $(':radio[name="view_days"]:checked').val();
    if(type=="기간별"){
        alert("기간별 데이터는 수정할 수 없습니다.");
        return;
    }
    var platform_name = $(".contents-platforms").find('.platform-selected').val(); //platform name
    var th = $('#board tr:first').children();
    var artists = $('#board').find('th');
    var trs_value = $('input[type=text]');    
    trs_value = trs_value.slice(3)

    var table_header = [];
    for (let i =0; i<th.length; i++){
        table_header.push(th[i].innerHTML)
    }

    var artist_list = [];
    for(var i = table_header.length-1; i< artists.length; i++){
        artist_list.push(artists[i].innerHTML);
    }

    var target_items = [];
    for(var i = 0; i< trs_value.length; i++){
        target_items.push(trs_value[i].value)
    }

    $.ajax({
        type: 'POST',
        data : {'platform_name':platform_name,
        'artists[]':artist_list,
        'target_items[]':target_items,
        'platform_target_length':table_header.length-1,
        },
        url: '/dataprocess/api/daily/',
        success: res => {
            alert("Successfully save!");
            
            let data_list = [];
            let artist_list = [];
            let platform_list = [];
            data_list = res.data //필터링 데이터
            artist_list = res.artists //DB 아티스트 리스트
            platform_list = res.platform //수집 항목


            let crawling_artist_list = [] //크롤링 된 아티스트 리스트
            for (let i = 0; i<data_list.length; i++){
                crawling_artist_list.push(data_list[i]['artist']);
            }

            let db_artist_list = [] //DB 에 있는 아티스트 리스트
            for (let i = 0; i<artist_list.length; i++){
                db_artist_list.push(artist_list[i]);
            }
            $('tbody').eq(0).empty();
            $('#update-data').show();
            $('#platform-title').text(platform+' 리포트');
            showCrawledData(platform_list,data_list,db_artist_list,crawling_artist_list)
        },
        error : function (){
        }
      });

})


//excel popup
$(".excel-form-open").click(function(){
    if(this.innerHTML=="Excel파일로부터 크롤링데이터 DB에 저장하기"){
        document.getElementById("excel_form1").style.display = "flex";
        document.getElementById("excel_form2").style.display = "none";
        document.getElementById("excel_form3").style.display = "none";
    }else if(this.innerHTML=="Excel파일로 크롤링데이터 추출"){
        document.getElementById("excel_form1").style.display = "none";
        document.getElementById("excel_form2").style.display = "flex";
        document.getElementById("excel_form3").style.display = "none";
    }else if(this.innerHTML=="Excel파일로부터 수집정보 DB에 저장하기"){
        document.getElementById("excel_form1").style.display = "none";
        document.getElementById("excel_form2").style.display = "none";
        document.getElementById("excel_form3").style.display = "flex";
    }
    return;
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
    console.log("33");
    document.getElementById('progress-bar__bar3').classList.add('active');
}
