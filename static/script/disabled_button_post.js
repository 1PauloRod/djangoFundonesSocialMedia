const postButton = document.getElementById("btn-post");
const inputTextArea = document.getElementById("auto-focus-textarea");
const fileImagePost = document.getElementById("image-input");

function toggleButtonState(){
    if (inputTextArea.value.trim() === ""){
        postButton.disabled = true;
        postButton.style.background = "#497ff372";
        postButton.style.cursor = "auto";
    }else{
        postButton.style.background = "#497FF3";
        postButton.disabled = false;
        postButton.style.cursor = "pointer";
    }

}

inputTextArea.addEventListener('input', toggleButtonState);

window.onload = toggleButtonState;