const initBg = (autoplay = true) => {
    const bgImgsNames = ['7-26_musicpick.booty.jpg', 'D6PkkWZUYAEboCb.jpg', 'maxresdefault.jpg', 'PB-vaderjosh.jpg'];
    const bgImgs = bgImgsNames.map(img => "/static/img/" + img);

    $.backstretch(bgImgs, {duration: 4000, fade: 500});

    if(!autoplay) {
      $.backstretch('pause');  
    }    
}

const setBg = id => {
    $.backstretch('show', id);
}

const setBgOverlay = () => {
    const windowWidth = window.innerWidth;
    const bgHeight = $('body').height();
    const tmBgLeft = $('.tm-bg-left');

    $('.tm-bg').height(bgHeight);

    // const x1 = document.getElementsByClassName('tm-content')[0].offsetWidth/2;
    const y1 = $(window).height(); 
    const y2 = document.getElementsByClassName('.tm-bg-left')[0].offsetHeight;
    const x1 = Math.floor($(window).width() / 2.0);
    const x2 = Math.floor(((y2 - y1) / 2) + x1)

    console.log("x1: " + x1)
    console.log("x2: " + x2)
    console.log("y1: " + y1)
    console.log("y2: " + y2)
    const newValue = x2 + "px solid rgba(0,0,0,0.5)";
    $('.tm-bg-left').css({ "border-right":newValue });

    // if(windowWidth > 768) {
    //      tmBgLeft.css('border-left', `0`)
    //              .css('border-top', `${bgHeight}px solid transparent`)
    //              .css('border-right', x2);                
    // } else {
    //     tmBgLeft.css('border-left', `${windowWidth}px solid transparent`)
    //             .css('border-top', `0`)
    //             .css('border-right', x2);
    // }



}

$(document).ready(function () {




    const autoplayBg = true;	// set Auto Play for Background Images
    initBg(autoplayBg);    
    setBgOverlay();

    const bgControl = $('.tm-bg-control');            
    bgControl.click(function() {
        bgControl.removeClass('active');
        $(this).addClass('active');
        const id = $(this).data('id');                
        setBg(id);
    });

    $(window).on("backstretch.after", function (e, instance, index) {        
        const bgControl = $('.tm-bg-control');
        bgControl.removeClass('active');
        const current = $(".tm-bg-controls-wrapper").find(`[data-id=${index}]`);        
        current.addClass('active');
    });

    $(window).resize(function() {
        setBgOverlay();
    });    








});
