var btn_notification = document.getElementById("btn-notification");
var modal_notification = document.getElementsByClassName("modal-notifications");
var btn_close_notification = document.getElementsByClassName("close-notification");
var profile = document.getElementsByClassName("form-profile-bio");

btn_notification.addEventListener('click', function (){
    modal_notification[0].style.display = "block";
});

btn_close_notification[0].addEventListener('click', function (){
    modal_notification[0].style.display = "none";
});