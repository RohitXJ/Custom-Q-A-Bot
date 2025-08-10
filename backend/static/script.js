const chatContainer = document.getElementById("chatContainer");

// Handle file upload
document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);

    // Show uploading status
    chatContainer.innerHTML = `<div class="bot-msg">📂 Uploading file...</div>`;

    try {
        let response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        let result = await response.json();

        if (result.success) {
            chatContainer.innerHTML += `<div class="bot-msg">✅ File processed. Ask your question below.</div>`;
        } else {
            chatContainer.innerHTML += `<div class="bot-msg">❌ Error: ${result.message}</div>`;
        }
    } catch (err) {
        chatContainer.innerHTML += `<div class="bot-msg">❌ Upload failed.</div>`;
    }
});

// Function to send a question to backend
async function sendQuestion(question) {
    chatContainer.innerHTML += `<div class="user-msg">${question}</div>`;

    try {
        let res = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });

        let data = await res.json();
        chatContainer.innerHTML += `<div class="bot-msg">${data.answer}</div>`;
    } catch (err) {
        chatContainer.innerHTML += `<div class="bot-msg">❌ Failed to get response.</div>`;
    }
}
