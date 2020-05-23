$(document).ready(function () {
    $("#footer, .jumbotron .container .overpass, #slogan, .navbar-inner, #extra-content, #title, #second, #third, .carousel, #footer").hide();
    $("#title").fadeIn();
    $(".jumbotron .container .overpass").fadeIn(500, function () {
        $(".navbar-inner").slideDown().delay(1000);
        $("#extra-content").fadeIn().delay();
        $("#slogan").slideDown(1000, function () {
            $("#third").slideDown(1000);
            $("#second").slideDown(1000, function () {
                $(".carousel, #footer").show();
                $("#footer").show();
            });
        });
    });
});

$("flash-message").slideDown();


$("#footer-collapse").click(function() {
    console.log("clicked!");
    $('html, body').animate({scrollTop: $(document).height()}, 'slow');
})

$("#second a").click(function () {
    console.log("clicked!");
    document.querySelector('.carousel').scrollIntoView({ 
        behavior: 'smooth' 
      });
});