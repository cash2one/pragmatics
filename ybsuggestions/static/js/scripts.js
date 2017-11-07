$(window).bind("load resize", function(){
    $('.off-canvas').css('min-height', window.innerHeight+'px');
    $('.off-canvas-content').css('min-height', window.innerHeight+'px');
});

$( document ).ready(function() {

    $('.add_profile').click(function(){
        console.log('click');
        window.location.replace(profile_url + 'new');
    });
});