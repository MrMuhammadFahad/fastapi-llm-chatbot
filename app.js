const chat = document.getElementById("chat");
const input = document.getElementById("input");

window.onload = () => {
    const saved = localStorage.getItem("chat");
    if (saved) {
        chat.innerHTML = saved;
    }

    if (localStorage.getItem("theme") === "true") {
        document.body.classList.add("dark");
    }
};

function saveChat() {
    localStorage.setItem("chat", chat.innerHTML);
}

function addMessage(text, className, isMarkdown = false) {
    const msg = document.createElement("div");
    msg.className = `message ${className}`;

    if (isMarkdown) {
        msg.innerHTML = marked.parse(text);
    } else {
        msg.textContent = text;
    }

    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
    saveChat();
}

async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, "user");
    input.value = "";

    const typing = document.createElement("div");
    typing.className = "typing";
    typing.textContent = "Bot is typing...";
    chat.appendChild(typing);

    try {
        const response = await fetch("http://localhost:8000/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt: message })
        });

        const data = await response.json();
        typing.remove();

        // Streaming effect
        let text = "";
        const botMsg = document.createElement("div");
        botMsg.className = "message bot";
        chat.appendChild(botMsg);

        for (let char of data.response) {
            text += char;
            botMsg.innerHTML = marked.parse(text);
            await new Promise(r => setTimeout(r, 10));
        }

        saveChat();

    } catch (err) {
        typing.remove();
        addMessage("Error connecting to server.", "bot");
    }
}

const toggle = document.getElementById("toggleTheme");

toggle.onclick = () => {
    document.body.classList.toggle("dark");
    localStorage.setItem("theme", document.body.classList.contains("dark"));
};