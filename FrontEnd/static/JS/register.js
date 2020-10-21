const $ = window.$;

/* Run script only after page is done loading */
$(document).ready(() => {
    setTimeout(() => {
        $('.flash-success').fadeOut('slow');
    }, 10000);
    setTimeout(() => {
        $('.flash-error').fadeOut('slow');
    }, 15000);
    setTimeout(() => {
        $('.flash-bye').fadeOut('slow');
    }, 20000);
});
