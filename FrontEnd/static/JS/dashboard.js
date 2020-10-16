const $ = window.$;

if ($(window).width() < 800) {
    $(".add_employee").val("ADD");
}
else {
    $(".add_employee").val("ADD employee");
}

/* Run script only after page is done loading */
$(document).ready(() => {

    $(window).resize(() => {
        if ($(window).width() < 800) {
            $(".add_employee").val("ADD");
        }
        else {
            $(".add_employee").val("ADD employee");
        }
    });

    $(".check_for_del").css("display", "none");

    $(".del").click(function() {
        $(this).closest(".on_employee").find(".cardBtn").css("display", "none");
        $(this).closest(".on_employee").find(".check_for_del").css({
            "display": "flex",
            "align-items": "center",
            "justify-content": "center",
            "flex-direction": "column",
        });
    });

    $(".no").click(function() {
        $(this).closest(".on_employee").find(".check_for_del").css("display", "none")
        $(this).closest(".on_employee").find(".cardBtn").css({
            "display": "flex",
            "align-items": "center",
            "justify-content": "space-between",
            "flex-direction": "row",
        });
    });
});

