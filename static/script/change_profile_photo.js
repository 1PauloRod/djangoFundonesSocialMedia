profile_photo = document.getElementById("profile-image");
buttonChangeProfilePhotoInput = document.getElementById("image-profile-input");
buttonSubmitProfilePhoto = document.getElementById("btn-change-profile-photo");

profile_photo.addEventListener('click', function () {
    buttonChangeProfilePhotoInput.click();
});

buttonChangeProfilePhotoInput.addEventListener("change", function () {
    buttonSubmitProfilePhoto.click();
});