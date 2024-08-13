const postBtn = document.getElementById("btn-post");
const inputImage = document.getElementById("image-input");
const fileNameImage = document.getElementById("file-name");

function createFileName(fileName){
    
    if (fileName.includes('-')){
        var file = fileName.replace(/-/g, " ");
    }
    if (fileName.includes('_')){
        var file = fileName.replace(/_/g, " ");
    }
    
    var list = file.split(" ");
    var afterDot = file.split(".");    
    var newFileName = list[0] + '.' + afterDot[1];
    return newFileName;
}

inputImage.addEventListener("change", function(){
    var file = event.target.files[0];
    if (file){
 
        fileNameImage.textContent = createFileName(file.name);

        postBtn.style.background = "#497FF3";
        postBtn.disabled = false;
        postBtn.style.cursor = "pointer";
    }else{
        postBtn.disabled = true;
        postBtn.style.background = "#497ff372";
        postBtn.style.cursor = "auto";
    }
});