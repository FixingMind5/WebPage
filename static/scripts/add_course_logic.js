var readyLabel = document.getElementById('ready')
var photoContainer = document.getElementById('image')
var container = document.getElementById('image-container')
var uploadImageButton = document.getElementById('image-label')
var lessonsContainerLength = 0;

var lessonsContainer = document.getElementById('lessons-container')

photoContainer.addEventListener('change', uploadedFile)

function uploadedFile() {
    readyLabel.classList.remove('hidden')
    container.style.color = "#466124"
    container.style.backgroundColor = "#A8E05E"
    uploadImageButton.style.backgroundColor = "#A8E05E"
}

$(document).ready(function(){
  $('#add').click(function() {
    // event.preventDefault()
    console.log("Hola mundo");
    $('#lessons-container').append(
      '<p>Hola mundo</p>'
    )
  });
});