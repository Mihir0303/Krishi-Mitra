$(document).ready(function () {

    $('.fa-bars').click(function () {
        $(this).toggleClass('fa-time');
        $('.navbar').toggleClass('nav-toggle');
    });

    $(window).on('load scroll', function () {
        $('.fa-bars').removeClass('fa-time')
        $('.navbar').removeClass('nav-toggle')

        // navbar move function
        if ($(window).scrollTop() > 30) {
            $('.header').css({ 'background': '#65b741', 'box-shadow': '0 .3rem .5rem rgba(0, 0, 0, .3)' })
        } else
            $('.header').css({ 'background': 'none', 'box-shadow': 'none' })
    });

    // FAQ function 
    $('.subject-header').click(function () {
        $('.subject .subject-body').slideUp();
        $(this).next('.subject-body').slideDown();
        $('.subject .subject-header span').text('+')
        $(this).children('span').text('-')
    });

    // Smooth scroll for navbar links
    document.querySelectorAll('.navbar a').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').slice(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 60, // Adjust offset if header height
                    behavior: 'smooth'
                });
            }
        });
    });

});
