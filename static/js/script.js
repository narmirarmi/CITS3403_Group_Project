(function ($) {
    // Document ready function
    $(document).ready(function () {
        // Handle tab switching
        $('#tab-register').click(function () {
            $('#pills-login').removeClass('show active');
            $('#pills-register').addClass('show active');
            $('#tab-login').removeClass('active');
            $('#tab-register').addClass('active');
        });

        $('#tab-login').click(function () {
            $('#pills-register').removeClass('show active');
            $('#pills-login').addClass('show active');
            $('#tab-register').removeClass('active');
            $('#tab-login').addClass('active');
        });

        // Handle button clicks
        $('.btn').click(function () {
            var overlay = $(this).parent().find('.overlay');
            if ($(this).hasClass('btn-left')) {
                overlay.css('background-color', 'rgba(255, 0, 0, 0.5)'); // Red overlay for 'No'
            } else {
                overlay.css('background-color', 'rgba(0, 255, 0, 0.5)'); // Green overlay for 'Yes'
            }
            overlay.css('display', 'block');
            setTimeout(function () {
                overlay.css('display', 'none'); // Hide the overlay after 1 second
            }, 1000);
        });

        // Set button height to match image height
        $('.image-container').each(function () {
            var image = $(this).find('img');
            var button = $(this).find('.btn');
            button.css('height', image.height());
        });
    });
})(jQuery);
