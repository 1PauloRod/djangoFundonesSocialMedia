const textarea = document.getElementById("auto-focus-textarea");
const search_bar = document.getElementById("search-bar");


 // Adiciona um evento de foco ao textarea
 textarea.addEventListener('focus', function() {
    // Adiciona um evento de clique em todo o documento para garantir que o textarea receba o foco
    textarea.style.height = "90px";
    textarea.style.borderBottom = "2px solid #497FF3";
    document.addEventListener('click', keepFocus, true);
});

// Função para garantir que o textarea mantenha o foco
function keepFocus(event) {

    if (event.target === search_bar){
        search_bar.focus();
    }else{
        textarea.focus();
    }



    /*if (event.target !== textarea) {
        textarea.focus();
    }*/
}

