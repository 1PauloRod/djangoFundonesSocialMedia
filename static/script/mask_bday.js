document.getElementById('mask-bday').addEventListener('input', function (e) {
    let bday = e.target.value.replace(/\D/g, '');
    if (bday.length > 2) {
        bday = bday.substring(0, 2) + '/' + bday.substring(2);
    }

    if (bday.length > 5) {
        bday = bday.substring(0, 5) + '/' + bday.substring(5);
    }
   
    e.target.value = bday;
});