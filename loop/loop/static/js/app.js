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

$(document).ready(function() {
    // check cookie
    var visited = getModalCookie("visited");

    if (visited == null) {
        setModalCookie('visited', 1);
    }
    else {
        visited = parseInt(visited);
        if (visited === 1 && Modernizr.mq('(min-width: 480px)')) { // 2nd pageview
            $('#nl_signup_modal').ajaxChimp({
                url: 'http://mnn.us4.list-manage.com/subscribe/post?u=6df70d8dcc50e45d16f196d8c&amp;id=6e238acf12',
                callback: mcSignupCallback,
            });
            $('#nl_signup_modal').modal();
            ga('send', 'event', 'Newsletter Popup', 'Modal Displayed');
        }
        setModalCookie('visited', visited + 1);
    }
});
