// Function to send the message
function sendMessage() {
    const userInput = document.getElementById('userInput');
    const messageText = userInput.value;
    if (messageText.trim() === '') return; // Prevent sending empty messages

    // Create user message element
    const userMessage = document.createElement('div');
    userMessage.classList.add('chat-message', 'user');
    userMessage.textContent = messageText;

    // Append user message to chatbox
    const chatbox = document.getElementById('chatbox');
    chatbox.appendChild(userMessage);

    // Send message to server
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

        // Create an avatar element for the bot
        const botAvatar = document.createElement('img'); 
        botAvatar.classList.add('bot-avatar');

        // Append avatar and message text
        botMessage.appendChild(botAvatar);
        botMessage.innerHTML += data.response; // Use innerHTML to allow HTML content

        // Append bot message to chatbox
        chatbox.appendChild(botMessage);

        // Clear input field
        userInput.value = '';
        chatbox.scrollTop = chatbox.scrollHeight; // Scroll to the bottom
    })
    .catch(error => console.error('Error:', error));
}

// Add an event listener for the "Enter" key press
document.getElementById('userInput').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        sendMessage(); // Call sendMessage when "Enter" key is pressed
        event.preventDefault(); // Prevent default action of Enter key
    }
});
