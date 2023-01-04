var element = document.GetElementById('file2');
var file = element.files[0];
var blob = file.slice(0, file.size, 'image/png'); 
newFile = new File([blob], 'name.png', {type: 'image/png'});