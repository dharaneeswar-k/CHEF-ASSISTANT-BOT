function sendMessage() {
    const userInput = document.getElementById('userInput');
    const messageText = userInput.value;
    if (messageText.trim() === '') return;

    const userMessage = document.createElement('div');
    userMessage.classList.add('chat-message', 'user');
    userMessage.textContent = messageText;

    const chatbox = document.getElementById('chatbox');
    chatbox.appendChild(userMessage);

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: messageText })
    })
    .then(response => response.json())
    .then(data => {
        const botMessage = document.createElement('div');
        botMessage.classList.add('chat-message', 'bot');

        const botAvatar = document.createElement('img');
        botAvatar.classList.add('bot-avatar');
        botAvatar.src = '/static/images/logo.png';
        botAvatar.alt = 'Bot Logo';

        botMessage.appendChild(botAvatar);
        botMessage.innerHTML += data.response;

        chatbox.appendChild(botMessage);

        userInput.value = '';
        chatbox.scrollTop = chatbox.scrollHeight;
    })
    .catch(error => console.error('Error:', error));
}

document.getElementById('userInput').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
        event.preventDefault();
    }
});
