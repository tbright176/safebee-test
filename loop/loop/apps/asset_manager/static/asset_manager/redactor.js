function insertImageHTMLIntoBody(elem) {
    $.ajax({
	url: '/admin/asset_manager/image/image_html_snippet/?image_id=' + $(elem).val(),
	success: function(resp) {
	    $("#id_body").redactor('insertHtml', resp);
	},
    });
}

if (typeof RedactorPlugins === 'undefined') var RedactorPlugins = {};

RedactorPlugins.asset_manager = {
    init: function()
    {
	this.buttonAdd('image', 'Add Image', function() {
	    input = $('<div class="hide"><input class="vForeignKeyRawIdAdminField" id="id_redactor_asset_manager" name="redactor_asset_manager" type="text" value="" onchange="return insertImageHTMLIntoBody(this);" /><a href="/admin/asset_manager/image/?_to_field=id" class="related-lookup" id="lookup_id_redactor_asset_manager" onclick="return showRelatedObjectLookupPopup(this);"></a></div>');
	    input.appendTo('#id_body');
	    $("#lookup_id_redactor_asset_manager").click();
	});
    }
}
