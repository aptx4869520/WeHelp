const url1 = "https://cwpeng.github.io/test/assignment-3-1";
const url2 = "https://cwpeng.github.io/test/assignment-3-2";

let allSpots = [];
let currentIndex = 3;
const loadCount = 10;

window.addEventListener("load", function () {
    const menuIcon = document.querySelector(".menu-icon");
    const popupMenu = document.querySelector(".popup-menu");
    const closeBtn = document.querySelector(".close-btn");

    menuIcon.addEventListener("click", function () {
        popupMenu.classList.add("active");
    });

    closeBtn.addEventListener("click", function () {
        popupMenu.classList.remove("active");
    });

    Promise.all([
        fetch(url1).then(function (response) {
            return response.json();
        }),
        fetch(url2).then(function (response) {
            return response.json();
        })
    ])
        .then(function (results) {
            const data1 = results[0];
            const data2 = results[1];

            const list1 = data1.rows;
            const list2 = data2.rows;
            const host = data2.host;

            const spots = [];

            for (let i = 0; i < list1.length; i++) {
                const title = list1[i].sname;
                const serial = list1[i].serial;

                for (let j = 0; j < list2.length; j++) {
                    if (String(serial).trim() === String(list2[j].serial).trim()) {
                        const image = getFirstImage(list2[j].pics, host);

                        spots.push({
                            title: title,
                            image: image
                        });
                    }
                }
            }

            allSpots = spots;

            console.log("合併後資料：", allSpots);
            console.log("合併後資料筆數：", allSpots.length);

            renderFirstThreeAttractions(allSpots);

            renderCards(allSpots, currentIndex, loadCount);
            currentIndex = currentIndex + loadCount;

            const main = document.querySelector(".main");
            main.classList.add("loaded");

            const loadMoreBtn = document.querySelector('.load-more-btn');

            loadMoreBtn.addEventListener('click', function (){
                renderCards(allSpots, currentIndex, loadCount);

                currentIndex = currentIndex + loadCount;

                if (currentIndex >= allSpots.length) {
                    loadMoreBtn.style.display = "none"
                }
            });

            if (currentIndex >= allSpots.length) {
                loadMoreBtn.style.display = "none"
            }
        })
        .catch(function (error) {
            console.log("資料讀取或渲染發生錯誤：", error);
        });
});

function getFirstImage(pics, host) {
    const result = pics.match(/\/resources\/images\/[^/]+?\.jpg/i);

    if (result !== null) {
        return host + result[0];
    }

    return "";
}

function renderFirstThreeAttractions(spots) {
    const promotions = document.querySelector(".promotions");
    promotions.textContent = "";

    for (let i = 0; i < 3; i++) {
        const spot = spots[i];
        const bar = document.createElement("div");
        bar.className = "bar";

        const img = document.createElement("img");
        img.src = spot.image;
        img.alt = spot.title;

        const text = document.createElement("div");
        text.className = "bar-text";
        text.textContent = spot.title;

        bar.appendChild(img);
        bar.appendChild(text);

        promotions.appendChild(bar);
    }
}

function renderCards(spots, startIndex, count) {
    const cards = document.querySelector(".cards");
    
    const endIndex = startIndex + count;

    for (let i = startIndex; i < endIndex && i < spots.length; i++) {
        const spot = spots[i];

        const card = document.createElement("article");
        card.className = "card";

        const cardImg = document.createElement("img");
        cardImg.className = "card-img";
        cardImg.src = spot.image;
        cardImg.alt = spot.title;

        const star = document.createElement("img");
        star.className = "star";
        star.src = "pic/icon/star.png";
        star.alt = "star icon";

        const title = document.createElement("div");
        title.className = "card-title";
        title.textContent = spot.title;

        card.appendChild(cardImg);
        card.appendChild(star);
        card.appendChild(title);

        cards.appendChild(card);
    }
}