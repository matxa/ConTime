const $ = window.$;

/* Run script only after page is done loading */
$(document).ready(() => {
    setTimeout(() => {
        $('.flash-success').fadeOut('slow');
    }, 10000);
});

console.log("HEY")