const menuIcon = document.querySelector(".menu-icon");
const popupMenu = document.querySelector(".popup-menu");
const closeBtn = document.querySelector(".close-btn");

menuIcon.addEventListener("click", function () {
    popupMenu.classList.add("active");
});

closeBtn.addEventListener("click", function () {
    popupMenu.classList.remove("active");
});