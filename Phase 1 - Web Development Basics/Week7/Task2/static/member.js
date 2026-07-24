const messageForm = document.querySelector("#message-form");
const messageInput = document.querySelector("#message-content");
const messagesContainer = document.querySelector("#messages-container");

const generateTokenButton = document.querySelector("#generate-token-button");
const accessToken = document.querySelector("#access-token");
const tokenMessage = document.querySelector("#token-message");

generateTokenButton.addEventListener("click", async function () {
  generateTokenButton.disabled = true;

  accessToken.textContent = "";
  tokenMessage.textContent = "產生中……";

  try {
    const response = await fetch(
      "/api/token",
      {
        method: "PUT",
      },
    );

    const result = await response.json();

    if (result.ok === true) {
      accessToken.textContent = result.token;
      tokenMessage.textContent = "Token 產生成功";
      return;
    }

    tokenMessage.textContent = "Token 產生失敗，請確認登入狀態";
  } catch (error) {
    console.error("Token 產生失敗：", error);

    tokenMessage.textContent = "無法連線至 Token API";
  } finally {
    generateTokenButton.disabled = false;
  }
});

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

       if (message.self === true) {
            const deleteButton = document.createElement("button");

            deleteButton.type = "button";
            deleteButton.textContent = "X"   ;
            deleteButton.className = "delete-button";

            deleteButton.addEventListener("click",function () {
                    deleteMessage(message.id);
                }
            );

            messageItem.appendChild(deleteButton);
        }

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

async function deleteMessage(messageId) {
    const confirmed = confirm("確定要刪除這則留言嗎？");

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(
            `/api/message/${messageId}`,
            {
                method: "DELETE"
            }
        );

        const result = await response.json();

        if (result.ok === true) {
            await loadMessages();
            return;
        }

        alert("留言刪除失敗");

    } catch (error) {
        console.error("刪除留言失敗：", error);

        alert("留言刪除失敗");
    }
}

generateTokenButton.addEventListener(
  "click",

  async function () {
    generateTokenButton.disabled = true;

    accessToken.textContent = "";

    tokenMessage.textContent = "產生中……";

    try {
      const response = await fetch(
        "http://127.0.0.1:3000/api/token",

        {
          method: "PUT",

          credentials: "include",
        },
      );

      const result = await response.json();

      if (result.ok === true) {
        accessToken.textContent = result.token;

        tokenMessage.textContent = "Token 產生成功";

        return;
      }

      tokenMessage.textContent = "Token 產生失敗，請確認登入狀態";
    } catch (error) {
      console.error(
        "Token 產生失敗：",

        error,
      );

      tokenMessage.textContent = "無法連線至 Token API";
    } finally {
      generateTokenButton.disabled = false;
    }
  },
);


loadMessages();
