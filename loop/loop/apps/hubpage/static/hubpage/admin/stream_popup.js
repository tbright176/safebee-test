function set_streamitem_popup_links_for_category() {
    var cat_value = django.jQuery('#id_category option:selected').val();
    if (cat_value) {
	django.jQuery("a[id^=lookup_id_contentmoduleitem_set]").each(function() {
	    if (!django.jQuery(this).hasClass('image-asset-widget')) {
		var a_href = django.jQuery(this).attr('href');
		a_href = a_href.split('?')[0];
		a_href += "?e=1&category__id__exact=" + cat_value;
		a_href += "&status__exact=P";
		django.jQuery(this).attr('href', a_href);
	    }
	});
    }
}

(function($) {
    $(document).ready(function() {
	set_streamitem_popup_links_for_category();
	$("#id_category").change(function() {
	    set_streamitem_popup_links_for_category();
	});
    });
})(django.jQuery);
