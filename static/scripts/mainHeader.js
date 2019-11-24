window.onscroll = function () {
    becomeSticky();
};

var header = document.getElementById("header");
var sticky = header.offsetTop;

function becomeSticky() {
    if (window.pageYOffset > sticky) {
        header.classList.add("sticky");
    } else {
        header.classList.remove("sticky");
    }
}