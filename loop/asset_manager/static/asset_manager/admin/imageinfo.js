function imageAssetWidgetInputValueChanged(elem) {
    $.ajax({
        url: "/admin/asset_manager/image/widget_with_value/?image_id=" + $(elem).val() + "&name=" + elem.name,
        success: function(resp) {
            $(elem).parent().parent().html(resp);
        }
    });
}

$(document).ready(function() {

    window.dismissRelatedLookupPopup = function(win, chosenId) {
        var name = windowname_to_id(win.name);
        var elem = document.getElementById(name);
        if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
            elem.value += ',' + chosenId;
        } else {
            document.getElementById(name).value = chosenId;
            try {
                document.getElementById(name).onchange();
	    }
	    catch(err) {}
        }
        win.close();
    }

    window.dismissAddAnotherPopup = function(win, newId, newRepr) {
        // newId and newRepr are expected to have previously been escaped by
        // django.utils.html.escape.
        newId = html_unescape(newId);
        newRepr = html_unescape(newRepr);
        var name = windowname_to_id(win.name);
        var elem = document.getElementById(name);
        var o;
        if (elem) {
            var elemName = elem.nodeName.toUpperCase();
            if (elemName == 'SELECT') {
                o = new Option(newRepr, newId);
                elem.options[elem.options.length] = o;
                o.selected = true;
            } else if (elemName == 'INPUT') {
                if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
                    elem.value += ',' + newId;
                } else {
                    elem.value = newId;
                    try {
                        elem.onchange();
                    }
                    catch(err) {}
                }
            }
        } else {
            var toId = name + "_to";
            o = new Option(newRepr, newId);
            SelectBox.add_to_cache(toId, o);
            SelectBox.redisplay(toId);
        }
        win.close();
    }

});
