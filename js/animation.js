
$(document).ready(function() {
    $(window).on("scroll", function() {
        if ($(window).scrollTop() >= 20) {
            $(".navbar-brand").addClass("compressed");
        } else {
            $(".navbar-brand").removeClass("compressed");
        }
    });
});