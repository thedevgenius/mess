(function ($) {

    jQuery('.menu-btn').click(function () {
        jQuery('.main-menu').addClass('open');
    });
    jQuery('.close-btn').click(function () {
        jQuery('.main-menu').removeClass('open');
    });

    // Sticky Menu
    $(window).scroll(function () {
        if ($('header').offset().top > 10) {
            $('#header').addClass('sticky');
            $('#header .col-md-7').addClass('bg-blue');
        } else {
            $('#header').removeClass('sticky');
            $('#header .col-md-7').removeClass('bg-blue');
        }
    });
    document.getElementsByClassName
    // Background-images
    $('[data-background]').each(function () {
        $(this).css({
            'background-image': 'url(' + $(this).data('background') + ')'
        });
    });

    

  
    
    // mixitup filter
    var containerEl = document.querySelector('[data-ref~="mixitup-container"]');
    var mixer;
    if (containerEl) {
        mixer = mixitup(containerEl, {
            selectors: {
                target: '[data-ref~="mixitup-target"]'
            }
        });
    }

    //  Count Up
    function counter() {
        var oTop;
        if ($('.count').length !== 0) {
            oTop = $('.count').offset().top - window.innerHeight;
        }
        if ($(window).scrollTop() > oTop) {
            $('.count').each(function () {
                var $this = $(this),
                    countTo = $this.attr('data-count');
                $({
                    countNum: $this.text()
                }).animate({
                    countNum: countTo
                }, {
                    duration: 1000,
                    easing: 'swing',
                    step: function () {
                        $this.text(Math.floor(this.countNum));
                    },
                    complete: function () {
                        $this.text(this.countNum);
                    }
                });
            });
        }
    }
    $(window).on('scroll', function () {
        counter();
    });

})(jQuery);