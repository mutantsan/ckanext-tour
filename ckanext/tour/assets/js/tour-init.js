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

            this.tour = null;
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
            var showed = localStorage.getItem('intro-' + introData.id);
            var shouldAttach = introData.state === "active";
            var shouldStart = !showed && !this.isMobile && window.location.pathname == introData.page;
            var anchorExists = $(introData.anchor).length;

            this.tour = new Shepherd.Tour({
                useModalOverlay: true,
                defaultStepOptions: {
                    floatingUIOptions: { middleware: [FloatingUICore.offset(20)]},
                    cancelIcon: {
                        enabled: true,
                        label: "Skip tour"
                    },
                    modalOverlayOpeningPadding: 5,
                    modalOverlayOpeningRadius: 5,
                    classes: 'tour-step',
                    scrollTo: { behavior: 'smooth', block: 'center' },
                    when: {
                        show() {
                            // prevent scrolling while we are showing tour
                            bodyScrollLock.disableBodyScroll(".tour-step");

                            const currentStep = this;
                            const currentStepIdx = this.tour.steps.indexOf(currentStep);

                            const progressListEl = document.createElement('ul');
                            progressListEl.classList = ["list-unstyled shepherd-stats"]

                            for (let i = 0; i < this.tour.steps.length; i++) {
                                const bulletElement = document.createElement('li');
                                bulletElement.innerText = " ";
                                bulletElement.dataset.stepId = this.tour.steps[i].id;

                                if (i === currentStepIdx) {
                                    bulletElement.classList = ["active"];
                                }

                                $(bulletElement).click((el) => {
                                    Shepherd.activeTour.show(el.target.dataset.stepId);
                                })

                                progressListEl.append(bulletElement)
                            }

                            $('.shepherd-footer').before(progressListEl);
                        },
                        destroy() {
                            // release scroll after tour
                            bodyScrollLock.clearAllBodyScrollLocks();
                        }
                    }
                },

            });

            this.tour.addSteps(this._prepareSteps(introData.steps));

            if (shouldAttach && !shouldStart) {
                this.createMark();

                this.mark.insertAfter(anchorExists ? introData.anchor : '.breadcrumb .active');
                this.mark.on('click', this._onClick);
            }

            if (shouldStart) {
                localStorage.setItem('intro-' + introData.id, 1);
                this.tour.start();
            }
        },

        _prepareSteps: function (steps) {
            steps.forEach((step, idx) => {
                let isLast = steps.length - 1 === idx;
                let isFirst = idx === 0;
                let lastButtonText = isLast ? this._("Done") : "→";
                let firstButtonClasses = isFirst ? 'shepherd-back disabled' : 'shepherd-back';

                if (step.image) {
                    step.text = step.intro + "<br><br>" + $("<img />", {
                        src: step.image.url
                    })[0].outerHTML;
                } else {
                    step.text = step.intro;
                }

                step.buttons = [
                    {
                        action() {
                            return this.back();
                        },
                        classes: firstButtonClasses,
                        text: "←"
                    },
                    {
                        action() {
                            return this.next();
                        },
                        classes: 'shepherd-next',
                        text: lastButtonText
                    }
                ]

                step.attachTo = {
                    element: step.element,
                    on: step.position
                }
            });

            return steps;
        },

        _onClick: function (e) {
            this.tour.start();
        }
    }
});
