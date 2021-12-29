/* Data Report */

//sidebar toggle 
$(".data-report").click(function(){
    $(".in-data-report").slideToggle();
});

$(".platforms-m").click(function(){
    $(".in-platforms").slideToggle();
});

$(".artists-m").click(function(){
    $(".in-artists").slideToggle();
});

$(function(){
    var duration = 300;

    var $side = $('.sidebar');
    var $header = $('.header');
    var $dataform = $('.forms');
    var $sidebt = $('.sidebar-btn').on('click', function(){
        $side.toggleClass('open');

        if($side.hasClass('open')) {
            $side.stop(true).animate({left:'0px'}, duration);
            $header.stop(true).animate({left:'250px',width:'85%'}, duration);
            $dataform.stop(true).animate({left:'300px',width:'70%'}, duration);
            $sidebt.find('span').html('<i class="fas fa-chevron-left"></i>');
        }else{
            $side.stop(true).animate({left:'-250px'}, duration);
            $header.stop(true).animate({left:'50px',width:'90%'}, duration);
            $dataform.stop(true).animate({left:'50px',width:'90%'}, duration);
            $sidebt.find('span').html('<i class="fas fa-chevron-right"></i>');
        };
    });
});

//플랫폼별로 크롤링 된 데이터 보여주기

//number format
function numToString(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
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
            dataCol = $('<td></td>', {
                text:numToString(data[key]),
            })
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
            const data_list = res.data
            $('tbody').eq(0).empty();
            showYoutubeCrawledData(data_list) // Data들을 화면상에 표시
        },
        error: e => {
            alert('error!');
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
            dataCol = $('<td></td>', {
                text:numToString(data[key]),
            })
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
            dataCol = $('<td></td>', {
                text:numToString(data[key]),
            })
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
            dataCol = $('<td></td>', {
                text:numToString(data[key]),
            })
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
            dataCol = $('<td></td>', {
                text:numToString(data[key]),
            })
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
            dataCol = $('<td></td>', {
                text:numToString(data[key]),
            })
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