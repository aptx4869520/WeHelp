const loginForm = document.querySelector("#login-form");
const agreeCheckbox = document.querySelector("#agree");

loginForm.addEventListener('submit', function(event) {
    if (!agreeCheckbox.checked) {
        event.preventDefault();
        alert("請勾選同意條款");
    }
});