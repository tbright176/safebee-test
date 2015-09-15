if (!RedactorPlugins) var RedactorPlugins = {};
var redactorTextArea;

function insertImageHTMLIntoBody(elem) {
    var request_url = '/admin/asset_manager/image/image_html_snippet/?image_id=' + $(elem).val();
    if (typeof widgetWithValueOverride !== 'undefined') {
        request_url += "&alias=" + widgetWithValueOverride;
    }
    $.ajax({
    url: request_url,
    success: function(resp) {
        $(redactorTextArea).redactor('insert.html', resp);
    },
    });
}

RedactorPlugins.asset_manager = function()
{
    return {
        init: function ()
        {
        redactorTextArea = this.$textarea;
            var button = this.button.add('image', 'Add Image');
            this.button.addCallback(button, this.asset_manager.addImagePopup);
        },
        addImagePopup: function(buttonName)
        {
        input = $('<div class="hide"><input class="vForeignKeyRawIdAdminField" id="id_redactor_asset_manager" name="redactor_asset_manager" type="text" value="" onchange="return insertImageHTMLIntoBody(this);" /><a href="/admin/asset_manager/image/?_to_field=id" class="related-lookup" id="lookup_id_redactor_asset_manager" onclick="return showRelatedObjectLookupPopup(this);"></a></div>');
        input.appendTo(this.$textarea);
        $("#lookup_id_redactor_asset_manager").click();
        }
    };
};

RedactorPlugins.textinfo = function()
{
    return {
        getTemplate: function()
        {
        var counts = this.textinfo.count();
            return String()
            + '<section id="redactor-modal-textinfo">'
        + '<ul style="list-style-type: none;">'
        + '<li id="redactor-modal-textinfo-words">Words: ' + counts.words + '</li>'
        + '<li id="redactor-modal-textinfo-characters">Characters: ' + counts.characters + '</li>'
        + '<li id="redactor-modal-textinfo-characters-spaces">Spaces: ' + counts.spaces + '</li>'
        + '</ul>'
            + '</section>';
        },
        init: function ()
        {
            var button = this.button.add('textinfo', 'Info');
            this.button.addCallback(button, this.textinfo.show);

            // make your added button as Font Awesome's icon
            this.button.setAwesome('textinfo', 'fa-info-circle');
        },
        show: function()
        {
            this.modal.addTemplate('textinfo', this.textinfo.getTemplate());

            this.modal.load('textinfo', 'Text Info', 400);

            var button = this.modal.createActionButton('OK');
            button.on('click', this.textinfo.close);

            this.selection.save();
            this.modal.show();

            $('#mymodal-textarea').focus();
        },
    count: function() {
        var words = 0, characters = 0, spaces = 0;
        var html = this.code.get();
        var text = html.replace(/<\/(.*?)>/gi, ' ');
        text = text.replace(/<(.*?)>/gi, '');
        text = text.replace(/\t/gi, '');
        text = text.replace(/\n/gi, '');
        text = text.replace(/\r/gi, '');
        text = $.trim(text);

        if (text !== '')
        {
        var arrWords = text.split(/\s+/);
        var arrSpaces = text.match(/\s/g);

        if (arrWords) words = arrWords.length;
        if (arrSpaces) spaces = arrSpaces.length;
        characters = text.length;
        }

        return {words: words, characters: characters, spaces: spaces};
    },
        close: function()
        {
            this.modal.close();
        }
    };
};