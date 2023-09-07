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

            var stepId = $(e.target).closest(".tour-step").data("stepId");

            $(`#step_${stepId}`).remove();

            this._toggleRemoveBtns();
            this._updateLastStepId();
        },

        /**
         * Should be at least 1 step for a tour. Disable remove step button if
         * only 1 left.
         */
        _toggleRemoveBtns: function () {
            var steps = $(".tour-steps__steps .tour-step");
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
