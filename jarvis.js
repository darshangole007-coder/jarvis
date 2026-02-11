const chat = document.getElementById("chat");
const input = document.getElementById("input");

let micOn = true;

function add(text) {
    const d = document.createElement("div");
    d.textContent = text;
    chat.appendChild(d);
    chat.scrollTop = chat.scrollHeight;
}

function send(msg=null) {
    const text = msg || input.value.trim();
    if (!text) return;

    add("You: " + text);
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
    })
    .then(r => r.json())
    .then(d => add("JARVIS: " + d.reply));
}

function toggleMic() {
    micOn = !micOn;
}

const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
const rec = new SR();
rec.continuous = true;

rec.onresult = e => {
    if (!micOn) return;
    const text = e.results[e.results.length - 1][0].transcript;
    send(text);
};

rec.start();
