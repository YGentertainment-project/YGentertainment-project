// csrf 토큰을 가져옵니다.
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
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
    $side.addClass('open');
    var $sidebt = $('.sidebar-btn').on('click', function(){
        $side.toggleClass('open');

        if($side.hasClass('open')) {
            $side.stop(true).animate({left:'0px'}, duration);
            $header.stop(true).animate({left:'250px',width:'85%'}, duration);
            $dataform.stop(true).animate({left:'300px',width:'80%'}, duration);
            $sidebt.find('span').html('<i class="fas fa-chevron-left"></i>');
        }else{
            $side.stop(true).animate({left:'-250px'}, duration);
            $header.stop(true).animate({left:'50px',width:'90%'}, duration);
            $dataform.stop(true).animate({left:'50px',width:'90%'}, duration);
            $sidebt.find('span').html('<i class="fas fa-chevron-right"></i>');
        };
    });
});


//------account functions------
//login
function login_function(){
    var data = {
        "username": "username",
        "password": "password"
    };
    $.ajax({
        url: '/api/login/',
        type: 'POST',
        datatype:'json',
        data: JSON.stringify(data),
        success: res => {
            console.log(res);
        },
        error: e => {
            alert(e.responseText);
        },
    })
};

//simple login
function simple_login_function(){
    $.ajax({
        url: '/api/simplelogin/',
        type: 'GET',
        datatype:'json',
        contentType: 'application/json; charset=utf-8',
        success: res => {
            console.log(res);
        },
        error: e => {
            alert(e.responseText);
        },
    });
};

//logout
function logout_function(){
    $.ajax({
        url: '/api/logout/',
        type: 'GET',
        datatype:'json',
        contentType: 'application/json; charset=utf-8',
        success: res => {
            console.log(res);
        },
        error: e => {
            alert(e.responseText);
        },
    });
};

//register
function register_function(){
    var data = {
        "username": "username",
        "password": "password",
        "email": "email"
    };
    $.ajax({
        url: '/api/register/',
        type: 'POST',
        datatype:'json',
        data: JSON.stringify(data),
        success: res => {
            console.log(res);
        },
        error: e => {
            alert(e.responseText);
        },
    })
}

//change password
function change_password_function(){
    var data = {
        "username": "username",
        "new_password": "new_password"
    };
    $.ajax({
        url: '/api/change_password/',
        type: 'POST',
        datatype:'json',
        data: JSON.stringify(data),
        success: res => {
            console.log(res);
        },
        error: e => {
            alert(e.responseText);
        },
    })
}

$("#login-btn").click(function(){
    simple_login_function();
});

$("#logout-btn").click(function(){
    logout_function();
});

//alert message
if(document.getElementById("alert")){
    alert(document.getElementById("alert").innerHTML);
}