bad}

(function($) {
    $(document).ready(function() {
        var question_count = $('#id_quizquestion_set-INITIAL_FORMS').val();

        $('.dynamic-quizquestion_set .add-another').after(
    });
})(django.jQuery);





// $(function(){

//     $("select+a.add-another").each(function(){
//         $(this).after("&nbsp;<a class='changelink' href='#'></a>");
//         $(this).next().click(function(){

//             var linkvalue = $(this).prev().prev().attr('value');
//             if (linkvalue) {
//                 var linkname = ($(this).prev().attr('href')+'../'+linkvalue);
//                 var link = linkname + '?_popup=1';
//             }  else  {
//                 var linkname = ($(this).prev().attr('href').replace("add/", ""));
//                 var link = linkname + "?t=id&pop=1";
//             }

//             var win = window.open(linkname, link, 'height=600,width=1000,resizable=yes,scrollbars=yes');
//             win.focus();
//             return false;

//         });
//     });
