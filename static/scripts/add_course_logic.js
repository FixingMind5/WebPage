var readyLabel = document.getElementById('ready')
var photoContainer = document.getElementById('image')
var container = document.getElementById('image-container')
var uploadImageButton = document.getElementById('image-label')

var lessonsContainer = document.getElementById('lessons-container')

photoContainer.addEventListener('change', uploadedFile)

function uploadedFile() {
    readyLabel.classList.remove('hidden')
    container.style.color = "#466124"
    container.style.backgroundColor = "#A8E05E"
    uploadImageButton.style.backgroundColor = "#A8E05E"
}

function addElement() {
  var category = document.getElementById('option')
    if (category.value == 0) {
      const div = document.createElement('div');
      div.className = "lesson"
      div.innerHTML = `
      <input type="button" class="remove" value="X" onclick="removeRow(this)">
      <p>Nombre de la clase</p>
      <input type="text">
      <p>Url</p>
      <input type="text">
      `
      lessonsContainer.appendChild(div);
    }

    if (category.value == 1) {
    const div = document.createElement('div');
    div.className = "module"
    div.innerHTML = `
    <input type="button" class="remove" value="X" onclick="removeRow(this)">
    <p>Nombre del módulo</p>
    <input type="text">
    <p>Nivel</p>
    <select name="module_title">
      <option value="1">1</option>
      <option value="2">2</option>
      <option value="3">3</option>
      <option value="4">4</option>
      <option value="5">5</option>
    </select>
    `
    lessonsContainer.appendChild(div);
    }
}

function removeRow(input) {
  lessonsContainer.removeChild(input.parentNode);
}