/**
 * This is a first implementation of tour with intro.js library.
 * Unfortunately, the license of this library is not suitable for us, since it's
 * not free for commercial use. Leaving it there for a while, maybe the new implementation
 * with shepherd.js has some significant flaws.
 */
this.ckan.module('tour-init', function (jQuery) {
    return {
        options: {
            template: [
                '<a id="intro-switch" href="#" class="btn btn-sm question"><i class="fa fa-lg fa-question-circle"></i></a>',
                '<i class="icon-question-sign"></i>',
                '</i>',
                '</a>'
            ].join('\n')
        },

        initialize: function () {
            $.proxyAll(this, /_/);

            this.intro = null;
            this.isMobile = this._isMobile()

            $.ajax({
                url: this.sandbox.url("/api/action/tour_list"),
                success: this._onSuccessRequest
            });
        },

        _isMobile: function () {
            var md = new MobileDetect(window.navigator.userAgent);
            return md.mobile() ? true : false;
        },

        /**
         * Creates a tour mark if not exist
         *
         * @returns
         */
        createMark: function () {
            if (!this.mark) {
                this.mark = jQuery(this.options.template);
            }
            return this.mark;
        },

        _onSuccessRequest: function (data) {
            data.result.forEach(element => this._initIntro(element));
        },

        _initIntro: function (introData) {
            console.log(introData);
            var showed = localStorage.getItem('intro-' + introData.id);
            var shouldAttach = introData.state === "active";
            var shouldStart = !showed && !this.isMobile && window.location.pathname == introData.page;
            var anchorExists = $(introData.anchor).length;

            this.intro = introJs();
            this.intro.setOptions({
                overlayOpacity: 0.7,
                nextLabel: ' &rarr; ',
                prevLabel: '&larr; ',
                skipLabel: this._('Skip'),
                doneLabel: this._('Got it!'),
                showStepNumbers: false,
                exitOnEsc: true, // default
                exitOnOverlayClick: true, // default
                keyboardNavigation: true, // default
                showButtons: true, // default
                showBullets: true, // default,
                showProgress: false, // default
                steps: this._prepareSteps(introData.steps),
            });

            if (shouldAttach && !shouldStart) {
                this.createMark();

                this.mark.insertAfter(anchorExists ? introData.anchor : '.breadcrumb .active');
                this.mark.on('click', this._onClick);
            }

            if (shouldStart) {
                localStorage.setItem('intro-' + introData.id, 1);
                this.intro.start();
            }
        },

        _prepareSteps: function (steps) {
            steps.forEach(step => {
                if (step.image) {
                    step.intro = step.intro + "<br><br>" + $("<img />", {
                        src: step.image.url
                    })[0].outerHTML;
                }
            });

            return steps;
        },

        _onClick: function (e) {
            this.intro.start();
        }
    }
});
