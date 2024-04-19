(function ($) {
    document.getElementById('tab-register').addEventListener('click', function () {
        document.getElementById('pills-login').classList.remove('show', 'active');
        document.getElementById('pills-register').classList.add('show', 'active');
        document.getElementById('tab-login').classList.remove('active');
        document.getElementById('tab-register').classList.add('active');
    });

    document.getElementById('tab-login').addEventListener('click', function () {
        document.getElementById('pills-register').classList.remove('show', 'active');
        document.getElementById('pills-login').classList.add('show', 'active');
        document.getElementById('tab-register').classList.remove('active');
        document.getElementById('tab-login').classList.add('active');
    });

})(jQuery);