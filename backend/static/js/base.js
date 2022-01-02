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

