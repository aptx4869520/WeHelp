document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.querySelector("#login-form");
    const agreeCheckbox = document.querySelector("#agree");

    if (loginForm && agreeCheckbox) {
        loginForm.addEventListener("submit", function (event) {
            if (!agreeCheckbox.checked) {
                event.preventDefault();
                alert("請勾選同意條款");
            }
        });
    }

    const hotelButton = document.querySelector("#hotel-button");
    const hotelIdInput = document.querySelector("#hotel-id");

    if (hotelButton && hotelIdInput) {
        hotelButton.addEventListener("click", function () {
            const hotelId = hotelIdInput.value.trim();

            if (!/^[1-9][0-9]*$/.test(hotelId)) {
                alert("請輸入正整數");
                return;
            }

            window.location.href = "/hotel/" + hotelId;
        });
    }
});