(function() {
  var contentDiv = $("div.content");
  if (contentDiv.length) {
    var classNames = contentDiv.attr("class").toString().split(' ');
    $.each(classNames, function(i, className) {
      if (className.match(/(photooftheday|article|slideshow)-\d+/) != null) {
        tokens = className.split("-");
        window.location = "http://staging.fromthegrapevine.com/admin/core/" + tokens[0] + "/" + tokens[1] + "/";
      }
    });
  }
})($);
