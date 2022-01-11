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
   const next_day = addDays(today,1);
   var year = next_day.getFullYear();
   var month = ("0" + (1 + next_day.getMonth())).slice(-2);
   var day = ("0" + next_day.getDate()).slice(-2);
   $('input[name=start_date]').val(year+'-'+month+'-'+day);  
})

$(document).on('click','input[name=week]',function(){
    const today = new Date();
    const next_day = addDays(today,7);
    var year = next_day.getFullYear();
    var month = ("0" + (1 + next_day.getMonth())).slice(-2);
    var day = ("0" + next_day.getDate()).slice(-2);
    $('input[name=start_date]').val(year+'-'+month+'-'+day);  
 })

$(document).on('click','input[name=month]',function(){
    const today = new Date();
    const next_day = addDays(today,30);
    var year = next_day.getFullYear();
    var month = ("0" + (1 + next_day.getMonth())).slice(-2);
    var day = ("0" + next_day.getDate()).slice(-2);
    $('input[name=start_date]').val(year+'-'+month+'-'+day);  
 })



//show crawled data

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
            let platform_targets = [];
            data_list = res.data //필터링 데이터
            artist_list = res.artists //DB 아티스트 리스트
            platform_list = res.platform //수집 항목

            
            //console.log(data_list[0]['artist']);
            //console.log(artist_list[0]['name']);
            //console.log(platform_list.length);

            $('tbody').eq(0).empty();
        },
        error: e => {
            console.log(e);
            alert(e.responseText);
        },
    })
})


//update crawled data
$('#update-data').click(function(){
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
            url: '/dataprocess/api/daily/',
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
            url: '/dataprocess/api/daily/',
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
           url: '/dataprocess/api/daily/',
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

