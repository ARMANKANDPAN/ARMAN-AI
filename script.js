document.getElementById('chat-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    
    if (message) {
        // Display user message
        displayMessage(message, 'user');
        
        // Clear input
        userInput.value = '';
        
        // Send message to Flask backend
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(`HTTP error! status: ${response.status}, message: ${err.response || JSON.stringify(err)}`);
                });
            }
            return response.json();
        })
        .then(data => {
            displayMessage(data.text_response, 'ai');


        })
        .catch(error => {
            console.error('Fetch Error:', error);
            displayMessage(`Oops! Something went wrong: ${error.message}`, 'ai');
        });
    }
});

function displayMessage(message, sender) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender + '-message');
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}