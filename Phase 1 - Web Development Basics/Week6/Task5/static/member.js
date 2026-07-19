const messageForm = document.querySelector("#message-form");
const messageInput = document.querySelector("#message-content");
const messagesContainer = document.querySelector("#messages-container");


async function loadMessages() {
    try {
        const response = await fetch("/api/message", {
            method: "GET"
        });

        const result = await response.json();

        if (result.error === true) {
            window.location.href = "/";
            return;
        }

        renderMessages(result.data);

    } catch (error) {
        console.error("取得留言失敗：", error);

        messagesContainer.textContent = "留言載入失敗";
    }
}


function renderMessages(messages) {
    messagesContainer.replaceChildren();

    if (messages.length === 0) {
        const emptyText = document.createElement("p");
        emptyText.textContent = "目前沒有留言";

        messagesContainer.appendChild(emptyText);
        return;
    }

    for (const message of messages) {
        const messageItem = document.createElement("div");
        messageItem.className = "message-item";

        const messageText = document.createElement("p");

        const author = document.createElement("strong");
        author.textContent = message.name;

        const content = document.createTextNode(
            `：${message.content}`
        );

        messageText.appendChild(author);
        messageText.appendChild(content);

        messageItem.appendChild(messageText);

        messagesContainer.appendChild(messageItem);
    }
}


messageForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const content = messageInput.value.trim();

    if (content === "") {
        alert("留言內容不可空白");
        return;
    }

    try {
        const response = await fetch("/api/message", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                content: content
            })
        });

        const result = await response.json();

        if (result.ok === true) {
            messageInput.value = "";

            await loadMessages();
            return;
        }

        alert("留言新增失敗");

    } catch (error) {
        console.error("新增留言失敗：", error);

        alert("留言新增失敗");
    }
});


loadMessages();