const chatBox = document.getElementById('chat-box');
const input = document.getElementById('commandInput');
const micBtn = document.getElementById('mic-btn');
let voiceActive = false;

function addMessage(role, text, isError = false) {
    const div = document.createElement('div');
    div.className = `msg ${role.toLowerCase()} ${isError ? 'error-msg' : ''}`;
    div.innerHTML = `<span class="${role.toLowerCase()}">${role}:</span> ${text}`;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendCommand() {
    const msg = input.value.trim();
    if (!msg) return;
    
    addMessage('USER', msg);
    input.value = '';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: msg})
        });
        
        if (!response.ok) throw new Error('Offline');
        const data = await response.json();
        addMessage('JARVIS', data.reply);
    } catch (error) {
        addMessage('JARVIS', "Server unreachable. Operating on emergency backup power.", true);
    }
}

async function toggleVoice() {
    const endpoint = voiceActive ? '/voice/stop' : '/voice/start';
    try {
        const res = await fetch(endpoint, { method: 'POST' });
        if (res.ok) {
            voiceActive = !voiceActive;
            micBtn.classList.toggle('active', voiceActive);
            addMessage('JARVIS', voiceActive ? "Voice monitoring activated." : "Voice monitoring suspended.");
        }
    } catch (err) {
        addMessage('JARVIS', "Unable to interface with audio drivers.", true);
    }
}

window.onload = () => {
    setTimeout(() => addMessage('JARVIS', 'Systems stabilized. Core protocols updated. At your service, sir.'), 800);
};  
