const $ = window.$;

if ($(window).width() < 800) {
    $(".add_employee").val("ADD");
}
else {
    $(".add_employee").val("ADD employee");
}


if ($(window).width() > 650) {
    
    $(".form_add").hide();
    $(".form_hide").hide();
}
else {
    $(".add_employees").hide();

    $(".form_add").show();
}

$(".form_hide").hide();
$(".check_for_del").hide();
$(".boss_for_del").hide();
$(".cal-table").hide();


// Tables
$(".employee-hour").first().css({
    "box-shadow": "0px 0px 2px 2px #cc4100",
});

$(".cal-table").first().show()


/* Run script only after page is done loading */
$(document).ready(() => {

    $(window).resize(() => {

        $(".form_add").css("background-color", "#67d380");
        $(".form_add").text("ADD a new employee");

        if ($(window).width() < 800) {
            $(".add_employee").val("ADD");
        }
        else {
            $(".add_employee").val("ADD employee");
        }

        if ($(window).width() > 650) {
    
            $(".form_add").css("display", "none");
            $(".add_employees").show();
        }
        else {
            $(".add_employees").hide();
        
            $(".form_add").show();
            $(".form_hide").hide();
        }

    });

    // Tables
    $(".employee-hour").click(function() {
        const tb_id = "#tb-"+$(this).attr('id')
        $(".cal-table").hide();
        $(tb_id).show()
    });
    //  End

    $(".form_add").click(() => {
        $(".form_hide").show()
        $(".form_add").hide()
        $(".add_employees").show();
    });

    $(".form_hide").click(() => {
        $(".form_hide").hide()
        $(".form_add").show()
        $(".add_employees").hide();
    });


    $(".check_for_del").hide();
    $(".boss_for_del").hide()


    $(".del").click(function() {
        $(this).closest(".on_employee").find(".cardBtn").hide();
        $(this).closest(".on_employee").find(".check_for_del").show();
    });

    $(".del_account").click(function() {
        $(this).hide();
        $(".boss_for_del").show()
    });

    $(".b_no").click(function() {
        $(".del_account").show()
        $(".boss_for_del").hide()
    });

    $(".no").click(function() {
        $(this).closest(".on_employee").find(".check_for_del").hide();
        $(this).closest(".on_employee").find(".cardBtn").show();
    });

    $(".employee-hour").click(function() {
        $(".employee-hour").css({"box-shadow": "1px 1px 1px 1px rgba(0,0,0,0.15)"});
        $(this).css({
            "box-shadow": "0px 0px 2px 2px #cc4100",
        });
    });
});
