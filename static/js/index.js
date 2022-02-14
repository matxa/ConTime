const $ = window.$;

if ($(window).width() < 751){
    $('.menu').hide()
    $('.menu-logout').hide()
}
else{
    $('.menu').show()
    $('.menu-logout').show()
}

/* Run script only after page is done loading */
$(document).ready(() => {
    if ($(window).width() < 751){
        $('.menu-icon').show()
    }
    else{
        $('.menu-icon').hide()
    }
    $('.select-box-none').hide()
    if ($('.select-box').val() == 'employee'){
        $('.select-box-none').val() == 'employee'
        $('#company-form').hide()
        $('#employee-form').show()
        console.log($('.select-box-none').val())
    }

    // SWITCH BETWEEN EMPLOYEE AND COMPANY FORM
    $('.select-box').change(function() {
        if ($('.select-box').val() == 'employee'){
            $('.select-box-none').val('employee')
            $('#company-form').hide()
            $('#employee-form').show()
            console.log($('.select-box-none').val())
        }
        if ($('.select-box').val() == 'company'){
            $('.select-box-none').val('company')
            $('#employee-form').hide()
            $('#company-form').show()
            console.log($('.select-box-none').val())
        }
    });

    // Hide JOB OFFER CARDS
    // $('.company-card').hide()
    $('.arrow').html('&#8679;')
    $('.arrow').click(function() {
        $('.company-card').toggle();
        if ($('.arrow').text() == '⇧'){
            $('.arrow').html('&#8681;')
        }
        else{
            $('.arrow').html('&#8679;')
        }
    });
    // COMFIRM IF USER WANTS TO DELETE CARD
    $('.yes-no').hide()
    $('.btn-three').click(function(){
        $(this).hide()
        $(this).closest('.company-card').find('.yes-no').show()
        $(this).closest('.company-card-work').find('.yes-no').show()
    });
    $('.btn-no').click(function(){
        $(this).closest('.company-card').find('.yes-no').hide()
        $(this).closest('.company-card-work').find('.yes-no').hide()
        $(this).closest('.company-card').find('.btn-three').show()
        $(this).closest('.company-card-work').find('.btn-three').show()
    });
    $('.confirm').hide()
    $('#login-btn').click(function(){
        $(this).hide()
        $('.confirm').show()
        $('.btn-no').click(function(){
            $('.confirm').hide()
            $('#login-btn').show()
        });

    });
    // SET TIMER FOR FLASHED MESSAGES
    setTimeout(function() {
        $('.flash-error').hide()
        $('.flash-success').hide()
    }, 5000);
    // HAMBURGER MENU
    $(window).resize(function(){
        if ($(window).width() < 751){
            $('.menu-icon').show()
            $('.menu').hide()
            $('.menu-logout').hide()
        }
        else{
            $('.menu-icon').hide()
            $('.menu').show()
            $('.menu-logout').show()
        }
    });

    $('.menu-icon').click(function(){
        $('.menu').toggle()
        $('.menu-logout').toggle()
    });
});
