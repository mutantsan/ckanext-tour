/**
* Extends core image-upload.js to prevent uploaded URL change.
*
* @param {Event} e
*/

var extendedModule = $.extend({}, ckan.module.registry["image-upload"].prototype);

extendedModule._fileNameFromUpload = function (url) {
    return url;
}

ckan.module("tour-image-upload", function ($, _) {
    "use strict";

    return extendedModule;
});
