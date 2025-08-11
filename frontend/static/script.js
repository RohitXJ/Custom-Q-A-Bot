let sessionId = null;

document.getElementById("upload-btn").addEventListener("click", async () => {
    const files = document.getElementById("file-input").files;
    if (files.length === 0) {
        alert("Please select at least one document.");
        return;
    }

    const formData = new FormData();
    for (let file of files) {
        formData.append("files", file);
    }

    document.getElementById("upload-status").innerText = "Uploading...";

    try {
        const res = await fetch("/upload", {
            method: "POST",
            body: formData
        });
        const data = await res.json();
        if (data.session_id) {
            sessionId = data.session_id;
            document.getElementById("upload-status").innerText = "Upload successful!";
            document.getElementById("upload-section").style.display = "none";
            document.getElementById("chat-section").style.display = "block";
            document.getElementById("user-input").focus();
        } else {
            document.getElementById("upload-status").innerText = "Upload failed.";
        }
    } catch (err) {
        document.getElementById("upload-status").innerText = "Error uploading files.";
    }
});

const sendMessage = async () => {
    const input = document.getElementById("user-input");
    const question = input.value.trim();
    if (!question) return;

    addMessage("user", question);
    input.value = "";

    const formData = new FormData();
    formData.append("session_id", sessionId);
    formData.append("question", question);

    try {
        const res = await fetch("/chat", {
            method: "POST",
            body: formData
        });
        const data = await res.json();
        addMessage("bot", data.answer || "No response.");
    } catch {
        addMessage("bot", "Error contacting server.");
    }
};

document.getElementById("user-input").addEventListener("keyup", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

document.getElementById("end-session-btn").addEventListener("click", async () => {
    const formData = new FormData();
    formData.append("session_id", sessionId);
    await fetch("/end-session", { method: "POST", body: formData });
    alert("Session ended. Files deleted.");
    window.location.reload();
});

function addMessage(sender, text) {
    const chatBox = document.getElementById("chat-box");
    const msg = document.createElement("div");
    msg.className = `message ${sender}`;
    msg.innerText = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}