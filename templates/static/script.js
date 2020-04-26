$( document ).ready(function() {
	$(document).scroll(scrollHandler);
	scrollHandler();
});

function scrollHandler() {
	if($(window).scrollTop() > $(".header").height()){
		$("#banner").addClass("banner-locked");
	}
	else{
		$("#banner").removeClass("banner-locked");
	}
}