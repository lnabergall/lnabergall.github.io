var compress = function() {
    if ($(window).scrollTop() >= 100) {
        $(".navbar-brand").addClass("compressed");
    } else {
        $(".navbar-brand").removeClass("compressed");
    }
}