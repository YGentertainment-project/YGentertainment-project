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
   if(!$('.data-report-in').hasClass("show")){
    $('.data-report-in').removeClass("hide")
    $('.data-report-in').addClass("show")
   } else{
    $('.data-report-in').removeClass("show")
    $('.data-report-in').addClass("hide")
   }
});



$(".platforms-m").click(function(){
    if(!$('.platform-in').hasClass("show")){
        $('.platform-in').removeClass("hide")
        $('.platform-in').addClass("show")
    } else{
        $('.platform-in').removeClass("show")
        $('.platform-in').addClass("hide")
    }
});



$(".artists-m").click(function(){
    if(!$('.artist-in').hasClass("show")){
        $('.artist-in').removeClass("hide")
        $('.artist-in').addClass("show")
    } else{
        $('.artist-in').removeClass("show")
        $('.artist-in').addClass("hide")
    }
});

$(".monitering-m").click(function(){
    if(!$('.monitering-in').hasClass("show")){
        $('.monitering-in').removeClass("hide")
        $('.monitering-in').addClass("show")
    } else{
        $('.monitering-in').removeClass("show")
        $('.monitering-in').addClass("hide")
    }
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
            $dataform.stop(true).animate({left:'250px',width:'80%'}, duration);
            $sidebt.stop(true).animate({left:'220px'}, duration);
            $sidebt.find('span').html('<i class="fas fa-chevron-left"></i>');
        }else{
            $side.stop(true).animate({left:'-220px'}, duration);
            $header.stop(true).animate({left:'50px',width:'90%'}, duration);
            $dataform.stop(true).animate({left:'50px',width:'90%'}, duration);
            $sidebt.stop(true).animate({left:'0px'}, duration);
            $sidebt.find('span').html('<i class="fas fa-chevron-right"></i>');
        };
    });
});


//alert message
if(document.getElementById("alert")){
    alert(document.getElementById("alert").innerHTML);
}