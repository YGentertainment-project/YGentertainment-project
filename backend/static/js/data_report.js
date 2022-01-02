//플랫폼별로 크롤링 된 데이터 보여주기

//number format
function numToString(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

//uncomma string number
function uncomma(str) {
    str = String(str);
    return str.replace(/[^\d]+/g, '');
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


$('option[name=youtube]').click(function(){
    var platform = $('option[name=youtube]').val();
    var type = $(':radio[name="view_days"]:checked').val();
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();
    $('option[name=youtube]').addClass('platform-selected');
    $('option[name=vlive]').removeClass('platform-selected');
    $('option[name=melon]').removeClass('platform-selected');
    $('option[name=spotify]').removeClass('platform-selected');
    $('option[name=instagram]').removeClass('platform-selected');
    $('option[name=facebook]').removeClass('platform-selected');
    $('option[name=twitter]').removeClass('platform-selected');
    $('option[name=twitter2]').removeClass('platform-selected');
    $('option[name=tiktok]').removeClass('platform-selected');
    $('option[name=weverse]').removeClass('platform-selected');
    $.ajax({
        url: '/crawler/daily/dailyread/?' + $.param({
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
            data_list = res.data
            //console.log(data_list);
            $('tbody').eq(0).empty();
            showYoutubeCrawledData(data_list) // Data들을 화면상에 표시
        },
        error: e => {
            console.log(e);
            alert(e.responseText);
        },
    })
});

//vlive
//table creation
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
            dataCol = $('<td><input type="text" value="'+numToString(data[key])+'" style="width:100%"></input></td>')
        }
        tableRow.append(dataCol)
    }
    return tableRow
}

// show crawled data
const showVliveCrawledData = (datas) => {
    $('#board').append(createVliveTableHeader());
    datas.forEach(data => {
        $('#board').append(createVliveTableRow(data))
    })
}


$('option[name=vlive]').click(function(){
    var platform = $('option[name=vlive]').val();
    var type = $(':radio[name="view_days"]:checked').val();
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();
    $('option[name=youtube]').removeClass('platform-selected');
    $('option[name=vlive]').addClass('platform-selected');
    $('option[name=melon]').removeClass('platform-selected');
    $('option[name=spotify]').removeClass('platform-selected');
    $('option[name=instagram]').removeClass('platform-selected');
    $('option[name=facebook]').removeClass('platform-selected');
    $('option[name=twitter]').removeClass('platform-selected');
    $('option[name=twitter2]').removeClass('platform-selected');
    $('option[name=tiktok]').removeClass('platform-selected');
    $('option[name=weverse]').removeClass('platform-selected');
    $.ajax({
        url: '/crawler/daily/dailyread/?' + $.param({
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
            const data_list = res.data
            $('tbody').eq(0).empty();
            showVliveCrawledData(data_list) // Data들을 화면상에 표시
        },
        error: e => {
            alert('error!');
        },
    })
});



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


$('option[name=weverse]').click(function(){
    var platform = $('option[name=weverse]').val();
    var type = $(':radio[name="view_days"]:checked').val();
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();
    $('option[name=youtube]').removeClass('platform-selected');
    $('option[name=vlive]').removeClass('platform-selected');
    $('option[name=melon]').removeClass('platform-selected');
    $('option[name=spotify]').removeClass('platform-selected');
    $('option[name=instagram]').removeClass('platform-selected');
    $('option[name=facebook]').removeClass('platform-selected');
    $('option[name=twitter]').removeClass('platform-selected');
    $('option[name=twitter2]').removeClass('platform-selected');
    $('option[name=tiktok]').removeClass('platform-selected');
    $('option[name=weverse]').addClass('platform-selected');
    $.ajax({
        url: '/crawler/daily/dailyread/?' + $.param({
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
            const data_list = res.data
            $('tbody').eq(0).empty();
            showWeverseCrawledData(data_list) // Data들을 화면상에 표시
        },
        error: e => {
            alert('error!');
        },
    })
});



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


$('option[name=twitter]').click(function(){
    var platform = $('option[name=twitter]').val();
    var type = $(':radio[name="view_days"]:checked').val();
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();
    $('option[name=youtube]').removeClass('platform-selected');
    $('option[name=vlive]').removeClass('platform-selected');
    $('option[name=melon]').removeClass('platform-selected');
    $('option[name=spotify]').removeClass('platform-selected');
    $('option[name=instagram]').removeClass('platform-selected');
    $('option[name=facebook]').removeClass('platform-selected');
    $('option[name=twitter]').addClass('platform-selected');
    $('option[name=twitter2]').removeClass('platform-selected');
    $('option[name=tiktok]').removeClass('platform-selected');
    $('option[name=weverse]').removeClass('platform-selected');
    $.ajax({
        url: '/crawler/daily/dailyread/?' + $.param({
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
            const data_list = res.data
            $('tbody').eq(0).empty();
            showTwitter1CrawledData(data_list) // Data들을 화면상에 표시
        },
        error: e => {
            alert('error!');
        },
    })
});

//twitter 2
$('option[name=twitter2]').click(function(){
    var platform = $('option[name=twitter2]').val();
    var type = $(':radio[name="view_days"]:checked').val();
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();
    $('option[name=youtube]').removeClass('platform-selected');
    $('option[name=vlive]').removeClass('platform-selected');
    $('option[name=melon]').removeClass('platform-selected');
    $('option[name=spotify]').removeClass('platform-selected');
    $('option[name=instagram]').removeClass('platform-selected');
    $('option[name=facebook]').removeClass('platform-selected');
    $('option[name=twitter]').removeClass('platform-selected');
    $('option[name=twitter2]').addClass('platform-selected');
    $('option[name=tiktok]').removeClass('platform-selected');
    $('option[name=weverse]').removeClass('platform-selected');
    $.ajax({
        url: '/crawler/daily/dailyread/?' + $.param({
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
            const data_list = res.data
            $('tbody').eq(0).empty();
            showTwitter1CrawledData(data_list) // Data들을 화면상에 표시
        },
        error: e => {
            alert('error!');
        },
    })
});


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


$('option[name=facebook]').click(function(){
    var platform = $('option[name=facebook]').val();
    var type = $(':radio[name="view_days"]:checked').val();
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();
    $('option[name=youtube]').removeClass('platform-selected');
    $('option[name=vlive]').removeClass('platform-selected');
    $('option[name=melon]').removeClass('platform-selected');
    $('option[name=spotify]').removeClass('platform-selected');
    $('option[name=instagram]').removeClass('platform-selected');
    $('option[name=facebook]').addClass('platform-selected');
    $('option[name=twitter]').removeClass('platform-selected');
    $('option[name=twitter2]').removeClass('platform-selected');
    $('option[name=tiktok]').removeClass('platform-selected');
    $('option[name=weverse]').removeClass('platform-selected');
    $.ajax({
        url: '/crawler/daily/dailyread/?' + $.param({
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
            const data_list = res.data
            $('tbody').eq(0).empty();
            showCrowdtangleCrawledData(data_list) // Data들을 화면상에 표시
        },
        error: e => {
            alert('error!');
        },
    })
});


$('option[name=instagram]').click(function(){
    var platform = $('option[name=instagram]').val();
    var type = $(':radio[name="view_days"]:checked').val();
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();
    $('option[name=youtube]').removeClass('platform-selected');
    $('option[name=vlive]').removeClass('platform-selected');
    $('option[name=melon]').removeClass('platform-selected');
    $('option[name=spotify]').removeClass('platform-selected');
    $('option[name=instagram]').addClass('platform-selected');
    $('option[name=facebook]').removeClass('platform-selected');
    $('option[name=twitter]').removeClass('platform-selected');
    $('option[name=twitter2]').removeClass('platform-selected');
    $('option[name=tiktok]').removeClass('platform-selected');
    $('option[name=weverse]').removeClass('platform-selected');
    $.ajax({
        url: '/crawler/daily/dailyread/?' + $.param({
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
            const data_list = res.data
            $('tbody').eq(0).empty();
            showCrowdtangleCrawledData(data_list) // Data들을 화면상에 표시
        },
        error: e => {
            alert('error!');
        },
    })
});


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


$('option[name=tiktok]').click(function(){
    var platform = $('option[name=tiktok]').val();
    var type = $(':radio[name="view_days"]:checked').val();
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();
    $('option[name=youtube]').removeClass('platform-selected');
    $('option[name=vlive]').removeClass('platform-selected');
    $('option[name=melon]').removeClass('platform-selected');
    $('option[name=spotify]').removeClass('platform-selected');
    $('option[name=instagram]').removeClass('platform-selected');
    $('option[name=facebook]').removeClass('platform-selected');
    $('option[name=twitter]').removeClass('platform-selected');
    $('option[name=twitter2]').removeClass('platform-selected');
    $('option[name=tiktok]').addClass('platform-selected');
    $('option[name=weverse]').removeClass('platform-selected');
    $.ajax({
        url: '/crawler/daily/dailyread/?' + $.param({
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
            const data_list = res.data
            $('tbody').eq(0).empty();
            showTiktokCrawledData(data_list) // Data들을 화면상에 표시
        },
        error: e => {
            alert('error!');
        },
    })
});

//update crawled data
$('#update-data').click(function(){
    var platform_name = $(".contents-platforms").find('.platform-selected').val(); //platform name
    var th = $('#board').find('th');
    var trs_value = $('input[type=text]');    

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
            url: '/crawler/daily/dailyupdate/',
            success: res => {
                console.log('success');
                let table_html = ''
                const data_list = res.data
                $('tbody').eq(0).empty();
                showYoutubeCrawledData(data_list) // Data들을 화면상에 표시
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


        $.ajax({
            type: 'POST',
            data : {'platform_name':platform_name,
            'artists[]':artists,
            'members[]' : members, 
            'videos[]': videos, 
            'likes[]': likes,
            'plays[]':plays, 
            },
            url: '/crawler/daily/dailyupdate/',
            success: res => {
                console.log('success');
                let table_html = ''
                const data_list = res.data
                $('tbody').eq(0).empty();
                showVliveCrawledData(data_list) // Data들을 화면상에 표시
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
            url: '/crawler/daily/dailyupdate/',
            success: res => {
                console.log('success');
                let table_html = ''
                const data_list = res.data
                $('tbody').eq(0).empty();
                showCrowdtangleCrawledData(data_list) // Data들을 화면상에 표시
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
            url: '/crawler/daily/dailyupdate/',
            success: res => {
                console.log('success');
                let table_html = ''
                const data_list = res.data
                $('tbody').eq(0).empty();
                showTiktokCrawledData(data_list) // Data들을 화면상에 표시
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
           url: '/crawler/daily/dailyupdate/',
            success: res => {
                console.log('success');
                let table_html = ''
                const data_list = res.data
                $('tbody').eq(0).empty();
                showTwitter1CrawledData(data_list) // Data들을 화면상에 표시
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
            },
            url: '/crawler/daily/dailyupdate/',
            success: res => {
                console.log('success');
                let table_html = ''
                const data_list = res.data
                $('tbody').eq(0).empty();
                showWeverseCrawledData(data_list) // Data들을 화면상에 표시
            },
            error : function (){
            }
          });
    }

})
