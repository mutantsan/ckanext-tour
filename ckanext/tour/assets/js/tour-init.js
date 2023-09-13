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
                // data: {},
                success: this._onSuccessRequest
            });
        },

        _isMobile: function () {
            var md = new MobileDetect(window.navigator.userAgent);
            return md.mobile() ? true : false;
        },

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
            var showed = localStorage.getItem('intro-' + introData.id);
            var shouldStart = !showed && !this.isMobile;
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


            this.createMark().appendTo(anchorExists ? introData.anchor : '.breadcrumb .active');
            this.mark.on('click', this._onClick);

            // if (shouldStart) {
            //     // for development
            //     localStorage.setItem('intro-' + introData.id, 1);
            //     this.intro.start();
            // }
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
