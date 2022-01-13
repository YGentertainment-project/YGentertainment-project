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
$(document).on('click','input[name=refresh]',function(){
    $('input[name=start_date]').val("");
    $('input[name=end_date]').val("");
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
    })
    tableHeader.append(c)
    for(let i = 0; i< platform_header.length; i++){
        let col = $('<th></th>', {
            text: platform_header[i],
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
                let dataCol;
                if(datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]]){
                    if(!isString(datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]])){
                        dataCol = $('<td><input type="text" value="'+numToString(datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]])+'" style="width:100%"></input></td>')
                    } else{
                        dataCol = $('<td><input type="text" value="'+datas[crawling_artist_list.indexOf(db_artist_list[i])][platform_list[j]]+'" style="width:100%"></input></td>')
                    }
                }
                else{
                    dataCol = $('<td> <input type="text" value="" style="width:100%; background-color:lightgray"></input></td>')
                }
                tableRow.append(dataCol)
            }
        } else{
            let dataCol = $('<th></th>', {
                text: db_artist_list[i],
            })
            tableRow.append(dataCol)
            for(let j =0; j<platform_list.length; j++){
                let dataCol = $('<td> <input type="text" value="" style="width:100%; background-color:lightgray" disabled></input></td>')
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

            //헤더 순서를 db 컬럼 순하고 맞추기
            let platform_target_name = [];
            let platform_header = [];
            for(let i = 0; i<platform_list.length; i++){
                platform_target_name.push(platform_list[i]['target_name'])
            }


            for (key in data_list[0]){
                if(platform_target_name.includes(key)){
                    platform_header.push(key)
                }
            }

            console.log(platform_header);

            $('tbody').eq(0).empty();
            $('#update-data').show();
            $('#platform-title').text(platform+' 리포트');
            showCrawledData(platform_header,data_list,db_artist_list,crawling_artist_list)
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
    var th = $('#board').find('th');
    var trs_value = $('input[type=text]');    
    trs_value = trs_value.slice(3)
    var type = $(':radio[name="view_days"]:checked').val();
    var start_date = $('input[name=start_date]').val();
    var end_date = $('input[name=end_date]').val();


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
            console.log(trs_value[i].value);
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
                let platform_list = [];
                data_list = res.data //필터링 데이터
                artist_list = res.artists //DB 아티스트 리스트
                platform_list = res.platform //수집 항목


                console.log(data_list);



            let crawling_artist_list = [] //크롤링 된 아티스트 리스트
            for (let i = 0; i<data_list.length; i++){
                crawling_artist_list.push(data_list[i]['artist']);
            }

            let db_artist_list = [] //DB 에 있는 아티스트 리스트
            for (let i = 0; i<artist_list.length; i++){
                db_artist_list.push(artist_list[i]);
            }

             //헤더 순서를 db 컬럼 순하고 맞추기
             let platform_target_name = [];
             let platform_header = [];
             for(let i = 0; i<platform_list.length; i++){
                 platform_target_name.push(platform_list[i]['target_name'])
             }
 
 
             for (key in data_list[0]){
                 if(platform_target_name.includes(key)){
                     platform_header.push(key)
                 }
             }

            $('tbody').eq(0).empty();
            $('#update-data').show();
            $('#platform-title').text(platform_name+' 리포트');
            showCrawledData(platform_header,data_list,db_artist_list,crawling_artist_list)
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
                alert("Successfully save!");
                let data_list = [];
                let artist_list = [];
                let platform_list = [];
                data_list = res.data //필터링 데이터
                artist_list = res.artists //DB 아티스트 리스트
                platform_list = res.platform //수집 항목


                console.log(data_list);



            let crawling_artist_list = [] //크롤링 된 아티스트 리스트
            for (let i = 0; i<data_list.length; i++){
                crawling_artist_list.push(data_list[i]['artist']);
            }

            let db_artist_list = [] //DB 에 있는 아티스트 리스트
            for (let i = 0; i<artist_list.length; i++){
                db_artist_list.push(artist_list[i]);
            }

             //헤더 순서를 db 컬럼 순하고 맞추기
             let platform_target_name = [];
             let platform_header = [];
             for(let i = 0; i<platform_list.length; i++){
                 platform_target_name.push(platform_list[i]['target_name'])
             }
 
 
             for (key in data_list[0]){
                 if(platform_target_name.includes(key)){
                     platform_header.push(key)
                 }
             }

            $('tbody').eq(0).empty();
            $('#update-data').show();
            $('#platform-title').text(platform_name+' 리포트');
            showCrawledData(platform_header,data_list,db_artist_list,crawling_artist_list)
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

             //헤더 순서를 db 컬럼 순하고 맞추기
             let platform_target_name = [];
             let platform_header = [];
             for(let i = 0; i<platform_list.length; i++){
                 platform_target_name.push(platform_list[i]['target_name'])
             }
 
 
             for (key in data_list[0]){
                 if(platform_target_name.includes(key)){
                     platform_header.push(key)
                 }
             }

            $('tbody').eq(0).empty();
            $('#update-data').show();
            $('#platform-title').text(platform_name+' 리포트');
            showCrawledData(platform_header,data_list,db_artist_list,crawling_artist_list)
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

                 //헤더 순서를 db 컬럼 순하고 맞추기
            let platform_target_name = [];
            let platform_header = [];
            for(let i = 0; i<platform_list.length; i++){
                platform_target_name.push(platform_list[i]['target_name'])
            }


            for (key in data_list[0]){
                if(platform_target_name.includes(key)){
                    platform_header.push(key)
                }
            }
    
                $('tbody').eq(0).empty();
                $('#update-data').show();
                $('#platform-title').text(platform_name+' 리포트');
                showCrawledData(platform_header,data_list,db_artist_list,crawling_artist_list)
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

                 //헤더 순서를 db 컬럼 순하고 맞추기
            let platform_target_name = [];
            let platform_header = [];
            for(let i = 0; i<platform_list.length; i++){
                platform_target_name.push(platform_list[i]['target_name'])
            }


            for (key in data_list[0]){
                if(platform_target_name.includes(key)){
                    platform_header.push(key)
                }
            }
    
                $('tbody').eq(0).empty();
                $('#update-data').show();
                $('#platform-title').text(platform_name+' 리포트');
                showCrawledData(platform_header,data_list,db_artist_list,crawling_artist_list)
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
            'start_date':start_date
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

                 //헤더 순서를 db 컬럼 순하고 맞추기
            let platform_target_name = [];
            let platform_header = [];
            for(let i = 0; i<platform_list.length; i++){
                platform_target_name.push(platform_list[i]['target_name'])
            }


            for (key in data_list[0]){
                if(platform_target_name.includes(key)){
                    platform_header.push(key)
                }
            }
    
                $('tbody').eq(0).empty();
                $('#update-data').show();
                $('#platform-title').text(platform_name+' 리포트');
                showCrawledData(platform_header,data_list,db_artist_list,crawling_artist_list)
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
                alert("Successfully save!");
                let data_list = [];
                let artist_list = [];
                let platform_list = [];
                data_list = res.data //필터링 데이터
                artist_list = res.artists //DB 아티스트 리스트
                platform_list = res.platform //수집 항목

                console.log(res.success);
    
                let crawling_artist_list = [] //크롤링 된 아티스트 리스트
                for (let i = 0; i<data_list.length; i++){
                    crawling_artist_list.push(data_list[i]['artist']);
                }
    
                let db_artist_list = [] //DB 에 있는 아티스트 리스트
                for (let i = 0; i<artist_list.length; i++){
                    db_artist_list.push(artist_list[i]);
                }

                 //헤더 순서를 db 컬럼 순하고 맞추기
            let platform_target_name = [];
            let platform_header = [];
            for(let i = 0; i<platform_list.length; i++){
                platform_target_name.push(platform_list[i]['target_name'])
            }


            for (key in data_list[0]){
                if(platform_target_name.includes(key)){
                    platform_header.push(key)
                }
            }
    
                $('tbody').eq(0).empty();
                $('#update-data').show();
                $('#platform-title').text(platform_name+' 리포트');
                showCrawledData(platform_header,data_list,db_artist_list,crawling_artist_list)
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

        console.log(artists);

        console.log(trs_value);

        $.ajax({
            type: 'POST',
            data : {'platform_name':platform_name,
            'artists[]':artists,
            'weverses[]' : weverses,  
            'start_date':start_date
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

                 //헤더 순서를 db 컬럼 순하고 맞추기
            let platform_target_name = [];
            let platform_header = [];
            for(let i = 0; i<platform_list.length; i++){
                platform_target_name.push(platform_list[i]['target_name'])
            }


            for (key in data_list[0]){
                if(platform_target_name.includes(key)){
                    platform_header.push(key)
                }
            }
    
                $('tbody').eq(0).empty();
                $('#update-data').show();
                $('#platform-title').text(platform_name+' 리포트');
                showCrawledData(platform_header,data_list,db_artist_list,crawling_artist_list)
            },
            error : function (){
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
    console.log("33");
    document.getElementById('progress-bar__bar3').classList.add('active');
}