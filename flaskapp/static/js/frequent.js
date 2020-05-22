$(document).ready(function() {
    $("#contact").hide();
});



$("#contact-prompt").click(function() {
    console.log("working, working");
    if ($("#contact").is(":visible")) {
        $(".fa-chevron-up").hide();
        $(".fa-chevron-down").show();
        $("#contact").slideUp();
    } else {
        $(".fa-chevron-up").show();
        $(".fa-chevron-down").hide();
        $("#contact").slideDown();
    }
});