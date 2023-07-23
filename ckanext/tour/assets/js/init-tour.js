this.ckan.module('init-tour', function (jQuery) {
    return {
        /* An object of module options */
        options: {
            template: [
                '<a id="intro-switch" href="#" class="btn btn-sm question"><i class="fa fa-lg fa-question-circle"></i></a>',
                '<i class="icon-question-sign"></i>',
                '</i>',
                '</a>'
            ].join('\n')
        },

        initialize: function () {
            intro = introJs();
            var introStart = true;
            var visited = localStorage.getItem('intro');
            introStart = visited ? false : true;
            var md = new MobileDetect(window.navigator.userAgent);
            var isMobile = md.mobile() ? true : false;

            intro.setOptions({
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
                steps: [
                    {
                        element: '.search-input-group',
                        intro: this._('Here you can search datasets by a keyword.')
                    },
                    {
                        element: '.filters',
                        intro: this._('Here you can filter datasets.'),
                        position: 'right'
                    },
                    {
                        element: '.dataset-list',
                        intro: this._('The matched datasets will list here.'),
                        position: 'right'
                    },
                    {
                        element: '#intro-switch',
                        intro: this._('Click this question mark to show this help again.'),
                        position: 'right'
                    },
                    {
                        title: 'Test!',
                        intro: '<img src="https://media3.giphy.com/media/xUNd9D6kBtEjkOGgYE/giphy.gif?cid=ecf05e47qlgq80obqtrt4q15om1rhttqgzct3k1ejhau0uu9&ep=v1_gifs_search&rid=giphy.gif&ct=g" /> test me up'
                    }
                ]
            });

            if (isMobile) {
                introStart = false;
            } else {
                this.createMark().appendTo('.breadcrumb .active');
                this.mark.on('click', this._onClick);
            }

            if (introStart) {
                localStorage.setItem('intro', 1);
                intro.start();
            }
        },

        createMark: function () {
            if (!this.mark) {
                var element = this.mark = jQuery(this.options.template);
            }
            return this.mark;
        },

        _onClick: function (event) {
            intro.start();
        }
    }
});
