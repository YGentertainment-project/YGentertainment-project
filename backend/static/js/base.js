//loading select search function library
$('#platform-select').select2(
    {
        placeholder: '플랫폼을 선택하세요.'
    }
);
$('#target-select').select2(
    {
        placeholder: '지표를 선택하세요.'
    }
);

//플랫폼별로 크롤링 된 데이터 보여주기

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
        if(key === 'platform' || key === 'recorded_date' || key === 'url' || key=='user_created'){
            continue;
        }
        else{
            dataCol = $('<td></td>', {
                text:data[key],
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


//youtube
$('option[name=youtube]').click(function(){
    var platform = $('option[name=youtube]').val();
    var type = $(':radio[name="view_days"]:checked').val();
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();
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
            showYoutubeCrawledData(data_list) // Data들을 화면상에 표시
        },
        error: e => {
            alert('error!');
        },
    })
});

