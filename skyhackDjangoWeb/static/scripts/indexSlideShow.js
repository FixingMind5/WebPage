var slideIndex = 0;
showSlides()

function showSlides() {
    var images = document.getElementsByClassName("photo");
    for (let i  = 0; i < images.length; i++) {
        images[i].style.display = "none";
    }
    slideIndex++;
    if (slideIndex > images.length) { slideIndex = 1 }
    images[slideIndex - 1].style.display = "grid";
    setTimeout(showSlides, 2000)
}