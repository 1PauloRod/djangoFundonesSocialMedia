var editBioDescriptionButton = document.getElementById("bio-description-button");
var bioModalDescription = document.getElementById("bio-modal");
var spanClose = document.getElementsByClassName("close")[0];

editBioDescriptionButton.addEventListener("click", function () {
    bioModalDescription.style.display = "block";
});

spanClose.onclick = function(){
    bioModalDescription.style.display = "none";
}
