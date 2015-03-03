$.modal.defaults['showClose'] = false;
$.modal.defaults['zIndex'] = 9999999;

function setModalCookie(key, value) {
    var expires = new Date();
    expires.setTime(expires.getTime() + (1 * 24 * 60 * 60 * 1000 * 365));
    document.cookie = key + '=' + value + ';expires=' + expires.toUTCString() + ';path=/';
}

function getModalCookie(key) {
    var keyValue = document.cookie.match('(^|;) ?' + key + '=([^;]*)(;|$)');
    return keyValue ? keyValue[2] : null;
}

function mcSignupCallback(resp) {
    if (resp.result === 'success') {
        var submit = $("#nl_signup_modal_submit");
        submit.attr("disabled", true);
        submit.css({"background-color": "#b6541e", "color": "#fff"});
        submit.text("Thanks!");
        setTimeout(function() {
            $.modal.close();
        }, 2000)
    }
}

function sbSidebarResize() {
    if (window.innerWidth<=640) {return;}
    var main_div;
    if ($('#article-content').length) {main_div='#article-content';}
    if ($('#index-content').length) {main_div='#index-content';}
    if ($('#recall-content').length) {main_div='#recall-content';}
    if ($('#homepage-content').length) {
        main_div = '#homepage-content';
        var main_width = $(main_div).width();
        var total_padding = 2*parseFloat($(main_div).children(".medium-7").css('padding-left')) + 2*parseFloat($(main_div).children(".medium-2").css('padding-left'))  + 2*parseFloat($('#sidebar').css('padding-left'));
        var left_col_width = 7*(main_width - total_padding - 301)/9;
        var mid_col_width = 2*(main_width - total_padding - 301)/9;
        $(main_div).children(".medium-7").width(left_col_width);
        $(main_div).children(".medium-2").width(mid_col_width);
        $('#sidebar').width(300);
        return;
    }
    if (main_div) {
        var main_width = $(main_div).width();
        var total_padding = 2*parseFloat($(main_div).children(".medium-9").css('padding-left')) + 2*parseFloat($('#sidebar').css('padding-left'));
        var left_col_width = main_width - total_padding - 301;
        $(main_div).children(".medium-9").width(left_col_width);
        $('#sidebar').width(300);
    }
}

$(document).ready(function() {
    sbSidebarResize();
    $(window).resize(function() {
        sbSidebarResize();
    }
    // check cookie
    var visited = getModalCookie("visited");

    if (visited == null) {
        setModalCookie('visited', 1);
    }
    else {
        visited = parseInt(visited);
        if (visited === 1 && Modernizr.mq('(min-width: 480px)') && (window.location.href.search('/newsletter/') == -1)) { // 2nd pageview
            $('#nl_signup_modal').ajaxChimp({
                url: 'http://mnn.us4.list-manage.com/subscribe/post?u=6df70d8dcc50e45d16f196d8c&amp;id=e5f09fa457',
                callback: mcSignupCallback,
            });
            $('#nl_signup_modal').modal();
            ga('send', 'event', 'Newsletter Popup', 'Modal Displayed');
        }
        setModalCookie('visited', visited + 1);
    }
});
