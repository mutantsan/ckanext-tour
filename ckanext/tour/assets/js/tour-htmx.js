/**
 * A hack script to properly load CKAN modules on an AJAX loaded HTML
 */
ckan.module("tour-htmx", function ($) {
    return {
        initialize: function () {
            $.proxyAll(this, /_on/);
            console.log('loaded');
            document.addEventListener('htmx:beforeRequest', this._onHTMXbeforeRequest);
            document.addEventListener('htmx:afterSettle', this._onHTMXafterSettle);
            document.addEventListener('htmx:pushedIntoHistory', this._onHTMXpushedIntoHistory);
        },

        _onHTMXbeforeRequest: function (e) {
            $(e.detail.target).find("[data-module]").unbind()

            for (const [key, _] of Object.entries(ckan.module.instances)) {
                ckan.module.instances[key] = null;
            }
        },

        _onHTMXafterSettle: function (e) {
            const doNotInitialize = ["tour-htmx"]

            if (e.detail.pathInfo.requestPath === "/admin_panel/config/tour/add_step") {
                var newStep = $(".tour-steps__steps .tour-step").last();

                newStep.find("[data-module]").each(function (_, element) {
                    const moduleName = $(element).attr("data-module");

                    if (!doNotInitialize.includes(moduleName)) {
                        ckan.module.initializeElement(element);
                    }
                })
            }

        },
    };
});
