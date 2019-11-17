var slideIndex = 1;

function plusSlides(n) {
  showSlide(slideIndex += n);
}

showSlide(slideIndex);

function showSlide(index) {
  var slides = document.getElementsByClassName("slide");
  var dots = document.getElementsByClassName("dot");
  if (index > slides.length) {
    slideIndex = 1;
  }
  if (index < 1) {
    slideIndex = slides.length;
  }
  for (let i = 0; i < slides.length ; i++) {
    slides[i].style.display = "none";
  }
  for (let i = 0; i < slides.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "")
  }
  slides[slideIndex - 1].style.display = "grid";
  dots[slideIndex - 1].className += " active";
}
