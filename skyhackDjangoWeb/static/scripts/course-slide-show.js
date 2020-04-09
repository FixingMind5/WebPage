var containers = document.getElementsByClassName('form-container')
var index = 0

function goNextSlide() {
    index++;

    if (index >= containers.length) {
        index = 0;
    }

    for (let i = 0 ; i < containers.length ; i++) {
        containers[i].classList.add("hidden")
    }
    containers[index].classList.remove("hidden")
}

function goPreviousSlide() {
    index--;

    if (index < 0) {
        index = containers.length - 1
    }

    for (let i = 0 ; i < containers.length ; i++) {
        containers[i].classList.add("hidden")
    }
    containers[index].classList.remove("hidden")
}