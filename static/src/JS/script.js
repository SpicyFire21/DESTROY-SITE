// ######################################
// carousel
// ######################################

const slide = ["/static/assets/img/carrousel-1.png",
    "/static/assets/img/carrousel-2.png",
    "/static/assets/img/carrousel-3.png",
    "/static/assets/img/carrousel-4.png",
    "/static/assets/img/carrousel-5.png"];
let index = 0;
let index_old = index - 1;
let index_new = index + 1;

const timeStamp = 5000; //ms
let autoSlide
if (timeStamp <= 800){
    ntimeStamp = timeStamp + 200;
} else {
    ntimeStamp = timeStamp
}
let transitionDelay =timeStamp/4;

if (transitionDelay > 800) {
    transitionDelay = 800;
}




function ChangeSlide(sens) {
    clearTimeout(autoSlide);


    const previousButton = document.querySelector('#previous');
    const nextButton = document.querySelector('#next');
    previousButton.style.display = "none";
    nextButton.style.display = "none";



    index = index + sens;
    index_old = index_old + sens;
    index_new = index_new + sens;
    if (index < 0) {
        index = slide.length - 1;
    }
    if (index > slide.length - 1) {
        index = 0;
    }
    if (index_old < 0) {
        index_old = slide.length - 1;
    }
    if (index_old > slide.length - 1) {
        index_old = 0;
    }
    if (index_new < 0) {
        index_new = slide.length - 1;
    }
    if (index_new > slide.length - 1) {
        index_new = 0;
    }
    const WidthCarrousel = document.querySelector('.slider-1').offsetWidth; // la bordure est compté dans la longueur donc je retire les pixels en trop
    const divslide = document.getElementById("container");

    if (sens > 0) {
        divslide.style.transition = "transform "+ transitionDelay +"ms ease";
        divslide.style.transform = "translateX(-" + WidthCarrousel + "px)";
        setTimeout(() => {
            divslide.style.transition = "";
            divslide.style.transform = "";
            document.getElementById("slide-old").src = slide[index_old];
            document.getElementById("slide").src = slide[index];
            document.getElementById("slide-new").src = slide[index_new];
            previousButton.style.display = "";
            nextButton.style.display = "";

        }, transitionDelay + 50);
    } else if (sens < 0) {
        const divslide = document.getElementById("container");
        divslide.style.transition = "transform "+ transitionDelay +"ms ease";
        divslide.style.transform = "translateX(" + WidthCarrousel + "px)";
        setTimeout(() => {
            divslide.style.transition = "";
            divslide.style.transform = "";
            document.getElementById("slide-old").src = slide[index_old];
            document.getElementById("slide").src = slide[index];
            document.getElementById("slide-new").src = slide[index_new];
            previousButton.style.display = "";
            nextButton.style.display = "";

        }, transitionDelay + 50);

    }

    autoSlide =setTimeout(() => ChangeSlide(1), ntimeStamp);
}

setTimeout(() => ChangeSlide(1), ntimeStamp);



