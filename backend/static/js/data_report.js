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

//not crawled artist
const createNotCrawledTableRow = (data) => {
    const tableRow = $('<tr></tr>');
    let col1 = $('<th></th>', {
        text:data
    })
    //조사 항목 개수만큼 넣기
    let col2 = `
    <td>
        <input type="text" value="" style="width:100%; background-color:lightgray"></input>
    </td>
    `
    let col3 = `
    <td>
        <input type="text" value="" style="width:100%; background-color:lightgray"></input>
    </td>
    `
    let col4 =  `
    <td>
        <input type="text" value="" style="width:100%; background-color:lightgray"></input>
    </td>
    `
    let col5 =  `
    <td>
        <input type="text" value="" style="width:100%; background-color:lightgray"></input>
    </td>
    `
    tableRow.append(col1)
    tableRow.append(col2)
    tableRow.append(col3)
    tableRow.append(col4)
    tableRow.append(col5)
    return tableRow;
}

const showNotCrawledData = (datas) => {
    datas.forEach(data => {
        $('#board').append(createNotCrawledTableRow(data))
    })
}

//creat header from data in DB
//플랫폼 이름을 받아옴
const createTableHeader = (platform) => {
    //ajax get
    $.ajax({
        url: '/dataprocess/api/platform_info/?' + $.param({
            platform: platform,
        }),
        type: 'GET',
        datatype:'json',
        contentType: 'application/json; charset=utf-8',
        success: res => {
            var datas = res.data 
            const tableHeader = $('<tr></tr>');
            for(let i = 0; i<datas.length; i++){
                let col = $('<th></th>', {
                    text: datas['target_name'][i],
                })
                tableHeader.append(col);
            }
            return tableHeader;
        },
        error: e => {
            console.log(e);
            alert(e.responseText);
        },
    })
}

// show table header (general)
const showTableHeader = (platform) => {
    $('#board').append(createTableHeader(platform));
}



//youtube
//table creation
const createYoutubeTableHeader = () => {
    const tableHeader = $('<tr></tr>');
    let col1 = $('<th></th>', {
        text: '아티스트',
    })
    let col2 = $('<th></th>', {
        text: '업로드 수',
    }) 
    let col3 = $('<th></th>', {
        text: '구독자 수',
    })
    let col4 =  $('<th></th>', {
        text: '총 조회 수',
    })
    tableHeader.append(col1)
    tableHeader.append(col2)
    tableHeader.append(col3)
    tableHeader.append(col4)
    return tableHeader;
}
// create rows for youtube
const createYoutubeTableRow = (data) => {
    const tableRow = $('<tr></tr>')
    // 해당 row에 대한 column 데이터들 넣기
    for(key in data){
        let dataCol;
        if(key === 'id'||key === 'platform' || key === 'recorded_date' || key === 'url' || key=='user_created'){
            continue;
        } else if(key === 'artist'){
            dataCol = $('<th></th>', {
                text:data[key],
            })
        }else{
            dataCol = $('<td><input type="text" value="'+numToString(data[key])+'" style="width:100%"></input></td>')
        }
        tableRow.append(dataCol)
    }
    return tableRow
}

// show crawled data
const showYoutubeCrawledData = (datas) => {
    $('#board').append(createYoutubeTableHeader());
    datas.forEach(data => {
        $('#board').append(createYoutubeTableRow(data))
    })
}

//vlive
const createVliveTableHeader = () => {
    const tableHeader = $('<tr></tr>');
    let col1 = $('<th></th>', {
        text: '아티스트',
    })
    let col2 = $('<th></th>', {
        text: '맴버 수',
    }) 
    let col3 = $('<th></th>', {
        text: '스타 영상 수',
    })
    let col4 =  $('<th></th>', {
        text: '좋아요 수',
    })
    let col5 =  $('<th></th>', {
        text: '재생 수',
    })
    tableHeader.append(col1)
    tableHeader.append(col2)
    tableHeader.append(col3)
    tableHeader.append(col4)
    tableHeader.append(col5)
    return tableHeader;
}
// create rows for youtube
const createVliveTableRow = (data) => {
    const tableRow = $('<tr></tr>')
    // 해당 row에 대한 column 데이터들 넣기
    for(key in data){
        let dataCol;
        if(key === 'id'|| key === 'recorded_date' || key === 'url'){
            continue;
        } else if(key === 'artist'){
            dataCol = $('<th></th>', {
                text:data[key],
            })
        }else{
            if(isEmpty(data[key])){
                dataCol = $('<td><input type="text" value="'+numToString(data[key])+'" style="width:100%; background-color:lightgray;"></input></td>')    
            } else{
                dataCol = $('<td><input type="text" value="'+numToString(data[key])+'" style="width:100%"></input></td>')
            }
        }
        tableRow.append(dataCol)
    }
    return tableRow
}

// show crawled data
const showVliveCrawledData = (datas,platform) => {
    $('#board').append(createVliveTableHeader());
    //showTableHeader(platform)
    datas.forEach(data => {
        $('#board').append(createVliveTableRow(data))
    })
}


//weverse
//table creation
const createWeverseTableHeader = () => {
    const tableHeader = $('<tr></tr>');
    let col1 = $('<th></th>', {
        text: '아티스트',
    })
    let col2 = $('<th></th>', {
        text: 'Wever 수',
    }) 
    tableHeader.append(col1)
    tableHeader.append(col2)
    return tableHeader;
}
// create rows for youtube
const createWeverseTableRow = (data) => {
    const tableRow = $('<tr></tr>')
    // 해당 row에 대한 column 데이터들 넣기
    for(key in data){
        let dataCol;
        if(key === 'id'|| key === 'recorded_date' || key === 'url'){
            continue;
        } else if(key === 'artist'){
            dataCol = $('<th></th>', {
                text:data[key],
            })
        }else{
            dataCol = $('<td><input type="text" value="'+numToString(data[key])+'" style="width:100%"></input></td>')
        }
        tableRow.append(dataCol)
    }
    return tableRow
}

// show crawled data
const showWeverseCrawledData = (datas) => {
    $('#board').append(createWeverseTableHeader());
    datas.forEach(data => {
        $('#board').append(createWeverseTableRow(data))
    })
}

//twitter 1
//table creation
const createTwitter1TableHeader = () => {
    const tableHeader = $('<tr></tr>');
    let col1 = $('<th></th>', {
        text: '트위터 계정',
    })
    let col2 = $('<th></th>', {
        text: '팔로워 수',
    }) 
    let col3 = $('<th></th>', {
        text: '트윗 수',
    })
    tableHeader.append(col1)
    tableHeader.append(col2)
    tableHeader.append(col3)
    return tableHeader;
}
// create rows for twitter
const createTwitter1TableRow = (data) => {
    const tableRow = $('<tr></tr>')
    // 해당 row에 대한 column 데이터들 넣기
    for(key in data){
        let dataCol;
        if(key==='id' || key === 'recorded_date' || key === 'url' || key=='user_created'){
            continue;
        } else if(key === 'artist'){
            dataCol = $('<th></th>', {
                text:data[key],
            })
        }
        else{
            dataCol = $('<td><input type="text" value="'+numToString(data[key])+'" style="width:100%"></input></td>')
        }
        tableRow.append(dataCol)
    }
    return tableRow
}

// show crawled data
const showTwitter1CrawledData = (datas) => {
    $('#board').append(createTwitter1TableHeader());
    datas.forEach(data => {
        $('#board').append(createTwitter1TableRow(data))
    })
}

//facebook & insta
//table creation
const createCrowdtangleTableHeader = () => {
    const tableHeader = $('<tr></tr>');
    let col1 = $('<th></th>', {
        text: '아티스트 계정',
    })
    let col2 = $('<th></th>', {
        text: '팔로워 수',
    }) 
    tableHeader.append(col1)
    tableHeader.append(col2)
    return tableHeader;
}
// create rows for twitter
const createCrowdtangleTableRow = (data) => {
    const tableRow = $('<tr></tr>')
    // 해당 row에 대한 column 데이터들 넣기
    for(key in data){
        let dataCol;
        if(key==='id' || key === 'recorded_date' || key === 'url'){
            continue;
        } else if(key === 'artist'){
            dataCol = $('<th></th>', {
                text:data[key],
            })
        }
        else{
            dataCol =  $('<td><input type="text" value="'+numToString(data[key])+'" style="width:100%"></input></td>')
        }
        tableRow.append(dataCol)
    }
    return tableRow
}

// show crawled data
const showCrowdtangleCrawledData = (datas) => {
    $('#board').append(createCrowdtangleTableHeader());
    datas.forEach(data => {
        $('#board').append(createCrowdtangleTableRow(data))
    })
}

//tik tok
//table creation
const createTiktokTableHeader = () => {
    const tableHeader = $('<tr></tr>');
    let col1 = $('<th></th>', {
        text: '아티스트',
    })
    let col2 = $('<th></th>', {
        text: '팔로워 수',
    }) 
    let col3 = $('<th></th>', {
        text: '업로드 수',
    })
    let col4 =  $('<th></th>', {
        text: '좋아요 수',
    })
    tableHeader.append(col1)
    tableHeader.append(col2)
    tableHeader.append(col3)
    tableHeader.append(col4)
    return tableHeader;
}
// create rows for tiktok
const createTiktokTableRow = (data) => {
    const tableRow = $('<tr></tr>')
    // 해당 row에 대한 column 데이터들 넣기
    for(key in data){
        let dataCol;
        if(key==='id' || key === 'recorded_date' || key === 'url' ){
            continue;
        } else if(key === 'artist'){
            dataCol = $('<th></th>', {
                text:data[key],
            })
        }
        else{
            dataCol = $('<td><input type="text" value="'+numToString(data[key])+'" style="width:100%"></input></td>')
        }
        tableRow.append(dataCol)
    }
    return tableRow
}

// show crawled data
const showTiktokCrawledData = (datas) => {
    $('#board').append(createTiktokTableHeader());
    datas.forEach(data => {
        $('#board').append(createTiktokTableRow(data))
    })
}

$('option').click(function(){
    if($(this).hasClass("platform-selected")){
      $(this).removeClass("platform-selected");
    }else{
      $(this).addClass("platform-selected");  
      $('option').not($(this)).removeClass("platform-selected");  
    }
});

$(document).on('click','.platform-name',function(){
    var platform = $(this).val();
    var type = $(':radio[name="view_days"]:checked').val();
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();
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
            let table_html = ''
            let data_list = [];
            let artist_list = [];
            data_list = res.data
            artist_list = res.artists
            console.log(data_list[0]['artist']);

            let data_artist_list = []; //크롤링 된 데이터에 있는 아티스트 리스트
            for(let i = 0; i<data_list.length; i++){
                data_artist_list.push(data_list[i]['artist']);
            }

            //let db_artist_list = [] //DB 에 있는 아티스트 리스트
            //for (let i = 0; i<artist_list.length; i++){
            //    db_artist_list.push(artist_list[i]['name']);
            //}

            //let not_crawled_artists=[];
            //for(let i = 0; i<db_artist_list.length; i++){
            //    if(db_artist_list[i] in data_artist_list){
            //        continue;
            //    } else{
            //        not_crawled_artists.push(db_artist_list[i]);
            //    }
            //}
            

            $('tbody').eq(0).empty();
            $('#update-data').show();
            $('#platform-title').text(platform+' 리포트');
            if(platform === 'youtube'){
                showYoutubeCrawledData(data_list);
            } else if(platform === 'vlive'){
                showVliveCrawledData(data_list);
            } else if(platform === 'instagram' || platform === 'facebook'){
                showCrowdtangleCrawledData(data_list);
            } else if(platform === 'twitter' || platform === 'twitter2'){
                showTwitter1CrawledData(data_list);
            } else if(platform === 'tiktok'){
                showTiktokCrawledData(data_list);
            } else if(platform === 'weverse'){
                showWeverseCrawledData(data_list);
            }
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
    console.log(type);
    if(type=="기간별"){
        alert("기간별 데이터는 수정할 수 없습니다.");
        return;
    }
    var platform_name = $(".contents-platforms").find('.platform-selected').val(); //platform name
    var th = $('#board').find('th');
    var trs_value = $('input[type=text]');    
    trs_value = trs_value.slice(3)

    //youtube
    if(platform_name === 'youtube'){
        var artists = [];
        var uploads = [];
        var subscribers = [];
        var views = [];
        for(var i = 4; i< th.length ; i++){
            artists.push(th[i].innerHTML);
        }
        for(var i = 0 ; i < trs_value.length ; i+=3){
            uploads.push(uncomma(trs_value[i].value))
        }
        for(var i = 1 ; i < trs_value.length ; i+=3){
            subscribers.push(uncomma(trs_value[i].value))
        }
        for(var i = 2 ; i < trs_value.length ; i+=3){
            views.push(uncomma(trs_value[i].value))
        }


        $.ajax({
            type: 'POST',
            data : {'platform_name':platform_name,
            'artists[]':artists,
            'uploads[]' : uploads, 
            'subscribers[]': subscribers, 
            'views[]': views, 
            },
            url: '/dataprocess/api/daily/',
            success: res => {
                alert("Successfully save!");
                console.log('success');
                let table_html = ''
                const data_list = res.data;
                $('tbody').eq(0).empty();
                showYoutubeCrawledData(data_list); // Data들을 화면상에 표시
                alert("Successfully save!");
            },
            error : function (){
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

        console.log(trs_value);

        $.ajax({
            type: 'POST',
            data : {'platform_name':platform_name,
            'artists[]':artists,
            'members[]' : members, 
            'videos[]': videos, 
            'likes[]': likes,
            'plays[]':plays, 
            },
            url: '/dataprocess/api/daily/',
            success: res => {
                alert("Successfully save!");
                console.log('success');
                let table_html = '';
                const data_list = res.data;
                $('tbody').eq(0).empty();
                showVliveCrawledData(data_list); // Data들을 화면상에 표시
                alert("Successfully save!");
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
            },
            url: '/dataprocess/api/daily/',
            success: res => {
                alert("Successfully save!");
                console.log('success');
                let table_html = '';
                const data_list = res.data;
                $('tbody').eq(0).empty();
                showCrowdtangleCrawledData(data_list); // Data들을 화면상에 표시
                alert("Successfully save!");
            },
            error : function (){
            }
          });
    }

     //tiktok
     if(platform_name === 'tiktok'){
        var artists = [];
        var uploads = [];
        var followers = [];
        var likes = [];
        for(var i = 4; i< th.length ; i++){
            artists.push(th[i].innerHTML);
        }
        for(var i = 0 ; i < trs_value.length ; i+=3){
            uploads.push(uncomma(trs_value[i].value))
        }
        for(var i = 1 ; i < trs_value.length ; i+=3){
            followers.push(uncomma(trs_value[i].value))
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
            },
            url: '/dataprocess/api/daily/',
            success: res => {
                alert("Successfully save!");
                console.log('success');
                let table_html = '';
                const data_list = res.data;
                $('tbody').eq(0).empty();
                showTiktokCrawledData(data_list); // Data들을 화면상에 표시
                alert("Successfully save!");
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
        for(var i = 3; i< th.length ; i++){
            artists.push(th[i].innerHTML);
        }
        for(var i = 0 ; i < trs_value.length ; i+=2){
            followers.push(uncomma(trs_value[i].value))
        }
        for(var i = 1 ; i < trs_value.length ; i+=2){
            twits.push(uncomma(trs_value[i].value))
        }

        $.ajax({
            type: 'POST',
            data : {'platform_name':platform_name,
            'artists[]':artists,
            'followers[]' : followers,  
            'twits[]' : twits,  
            },
           url: '/dataprocess/api/daily/',
            success: res => {
                alert("Successfully save!");
                console.log('success');
                let table_html = '';
                const data_list = res.data;
                $('tbody').eq(0).empty();
                showTwitter1CrawledData(data_list); // Data들을 화면상에 표시
                alert("Successfully save!");
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
            weverses.push(parseInt(uncomma(trs_value[i].value)))
        }

        console.log(trs_value);

        $.ajax({
            type: 'POST',
            data : {'platform_name':platform_name,
            'artists[]':artists,
            'weverses[]' : weverses,  
            },
            url: '/dataprocess/api/daily/',
            success: res => {
                alert("Successfully save!");
                console.log('success');
                const data_list = res.data;
                $('tbody').eq(0).empty();
                showWeverseCrawledData(data_list); // Data들을 화면상에 표시
            },
            error : function (){
            }
          });
    }

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