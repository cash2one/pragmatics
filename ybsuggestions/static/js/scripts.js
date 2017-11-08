$(window).bind("load resize", function(){
    $('.off-canvas').css('min-height', window.innerHeight+'px');
    $('.off-canvas-content').css('min-height', window.innerHeight+'px');
});

function setProfileCookie(profile_id){
    Cookies.set('profile_id', profile_id, { expires: 7 });
    console.log('Setting cookie: "profile_id", ' + profile_id)
}

function profileCookieManager(){
    var profileCookie = Cookies.get('profile_id');
    console.log(profileCookie);

    if(profileCookie === undefined){
        var profile_id = $('#profile_select').find('option').eq(0).attr('value');
        setProfileCookie(profile_id);
    }
}

$( document ).ready(function() {
    profileCookieManager();

    $('.add_profile').click(function(){
        console.log('click');
        window.location.replace(profile_url + 'new');
    });

    $('#profile_select').change(function(){
        var profile_id = $(this).find(":selected").attr('value');
        setProfileCookie(profile_id);
        location.reload();
    });

});