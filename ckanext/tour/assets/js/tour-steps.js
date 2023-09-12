/**
 * A script to manage multiple steps fieldsets
 */
ckan.module("tour-steps", function ($) {
    return {
        initialize: function () {
            $.proxyAll(this, /_on/);
            var self = this;

            // this vars
            this.addStepBtn = $(".add-step");

            // add event listeners
            $(document).on('click', '.add-step', this._onAddStep);
            $(document).on('click', '.remove-step', this._onRemoveStep);

            // HTMX events
            document.body.addEventListener('htmx:afterSwap', function (e) {
                let requestPath = e.detail.pathInfo.requestPath;

                if (requestPath === "/admin_panel/config/tour/add_step") {
                    self._toggleRemoveBtns();
                    self._updateLastStepId();
                }
            });

            this._toggleRemoveBtns();
            this._updateLastStepId();

            new Sortable.default(document.querySelectorAll('.tour-steps__steps'), {
                draggable: '.tour-accordion',
                handle: ".dragger",
                sortAnimation: {
                    duration: 200,
                    easingFunction: 'ease-in-out',
                },
                plugins: [Plugins.SortAnimation]
            })
                .on('drag:start', () => console.log('drag:start'))
                .on('drag:move', () => console.log('drag:move'))
                .on('drag:stop', () => console.log('drag:stop'))
                .on("sortable:stop", () => console.log("sortable:stop"))

        },

        _onAddStep: function (e) {
            //
        },

        /**
         * Triggered on remove step
         *
         * @param {event} e
         */
        _onRemoveStep: function (e) {
            e.preventDefault();

            var self = this;

            $(e.target).closest(".tour-accordion").hide('slow', function () {
                this.remove();
                self._toggleRemoveBtns();
                self._updateLastStepId();
            });
        },

        /**
         * Should be at least 1 step for a tour. Disable remove step button if
         * only 1 left.
         */
        _toggleRemoveBtns: function () {
            var steps = $(".tour-steps__steps .tour-accordion");
            $(".remove-step").toggleClass("disabled", steps.length == 1)
        },

        /**
         * Update the stepId we are sending to a server when adding a new step
         */
        _updateLastStepId: function () {
            var steps = $(".tour-steps__steps .tour-step");

            this.addStepBtn.attr("hx-vals", JSON.stringify({
                stepId: steps.last().data("step-id") + 1
            }))
        }
    };
});
