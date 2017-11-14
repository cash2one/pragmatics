$(window).bind("load resize", function(){
//    $(".movie-item").css('display', 'none');
    $('.off-canvas').css('min-height', window.innerHeight+'px');
    $('.off-canvas-content').css('min-height', window.innerHeight+'px');
});

function setProfileCookie(profile_id){
    Cookies.set('profile_id', profile_id, { expires: 7 });
    console.log('Setting cookie: "profile_id", ' + profile_id)
}

function profileCookieManager(){
    var profileCookie = Cookies.get('profile_id');

    if(profileCookie === undefined){
        var profile_id = $('#profile_select').find('option').eq(0).attr('value');
        setProfileCookie(profile_id);
    }
}

function rateUpAction(elem){
    $(elem).addClass("rated_up").removeClass("rate_up");
}

function rateDownAction(elem, movie_id){
    $(elem).addClass("rated_down").removeClass("rate_down");
    $('#movie-' + movie_id).fadeOut(500, function(){
        $(this).remove();
    });
}

function rateAjaxConnection(elem, url, rate_up){
    var profile_id = $('#profile_select').find(":selected").attr('value');
    var movie_id = $(elem).attr('data-movie-id');

    var success = false;
    $.ajax({
        method: "POST",
        url: url,
        data: { profile_id: profile_id, movie_id: movie_id },
        success : function (response)
        {
            success = response['status'] === 'success' ? true : false;
            if(success)
                if(rate_up)
                    rateUpAction(elem);
                else
                    rateDownAction(elem, movie_id);
        }

    });
}

$( document ).ready(function() {
    profileCookieManager();

    $('.add_profile').click(function(){
        window.location.replace(profile_url + 'new');
    });

    $('#profile_select').change(function(){
        var profile_id = $(this).find(":selected").attr('value');
        setProfileCookie(profile_id);
        location.reload();
    });

    $('.rate_down').click(function(){
        rateAjaxConnection(this, dismiss_suggestion_url, false);
    });

    $('.rate_up').click(function(){
        rateAjaxConnection(this, good_suggestion_url, true);
    });

});