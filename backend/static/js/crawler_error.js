$(document).ready(function(){
    $.ajax({
        url: '/dataprocess/api/crawler_error',
        type: 'GET',
        datatype: 'json',
        contentType: 'application/json; charset=utf-8',
        success: res => {
          console.log(res.data);
          var log_info = res.data
          
        },
        error: e => {
           console.log(e);
        },
    })
})