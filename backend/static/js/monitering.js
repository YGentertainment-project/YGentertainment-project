function getTaskinfo(){
    $.ajax({
        url: api_domain + 'taskinfos/',
        type: 'GET',
        datatype: 'json',
        contentType: 'application/json; charset=utf-8',
        success: res => {
          const taskinfos = res.taskinfos;
          return taskinfos
        },
        error: e => {
            const taskinfos = [];
            return taskinfos
        },
    })
}

$(document).ready(function(){
    let success = 0;
    let error = 0;
    let running = 0;

    $('.state-description-success').text('정상 '+success+'건');
    $('.state-description-error').text('오류 '+error+'건');
    $('.state-description-running').text('실행 중 ' +running+'건');
})