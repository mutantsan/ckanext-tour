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
                    self._updateStepsIndexes();
                }
            });

            this._toggleRemoveBtns();
            this._updateStepsIndexes();

            new Sortable.default(document.querySelectorAll('.tour-steps__steps'), {
                draggable: '.tour-accordion',
                handle: ".dragger",
                sortAnimation: {
                    duration: 200,
                    easingFunction: 'ease-in-out',
                },
                plugins: [Plugins.SortAnimation]
            }).on('drag:stopped', () => this._updateStepsIndexes())

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
                self._updateStepsIndexes();
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
         * Update the steps indexes on sorting or adding a new one
         */
        _updateStepsIndexes: function () {
            var steps = $(".tour-steps__steps .tour-accordion")
                .not(".draggable-source--is-dragging")
                .not(".draggable--original");

            steps.each((idx, step) => this._updateStepIndexes(idx + 1, step));
        },

        /**
         * Update a specific step indexes
         *  - update accordion header
         *  - update a hidden field we are sending to the server
         *
         * @param {HTMLElement} step
         */
        _updateStepIndexes: function (idx, step) {
            $(step).find(".step-number").text(idx);
            $(step).find("input[name='step_index']").val(idx);
        }
    };
});
