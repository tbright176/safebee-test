function set_streamitem_popup_links_for_related_items() {
    django.jQuery("a[id^=lookup_id_core-relateditem-content_type-object_id-], a[id$='-stream_item']").each(function() {
	if (!django.jQuery(this).hasClass('image-asset-widget')) {
	    var a_href = django.jQuery(this).attr('href');
	    a_href = a_href.split('?')[0];
	    a_href += "?e=1&status__exact=P";
	    django.jQuery(this).attr('href', a_href);
	}
    });
}

(function($) {
    $(document).ready(function() {
	set_streamitem_popup_links_for_related_items();
	$("#core-relateditem-content_type-object_id-group").change(function() {
	        set_streamitem_popup_links_for_related_items();
	    });
    });
})(django.jQuery);
