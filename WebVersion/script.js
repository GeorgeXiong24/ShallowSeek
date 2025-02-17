document.addEventListener('DOMContentLoaded', () => {
    // Initialize UI elements
    const outputText = document.getElementById('outputText');
    const inputText = document.getElementById('inputText');
    const sendButton = document.getElementById('sendButton');
    const deepThinkButton = document.getElementById('deepThinkButton');
    const searchButton = document.getElementById('searchButton');
    const attachButton = document.getElementById('attachButton');
    const messageLabel = document.getElementById('messageLabel');

    // Initialize button states
    let isProcessing = false;
    const buttons = [deepThinkButton, searchButton];
    let activeButton = null;

    // Show welcome dialog on load
    showWelcomeDialog();

    // Handle input submission
    function handleInput() {
        const userInput = inputText.value.trim();
        if (userInput) {
            // Add user message
            addMessage(userInput, 'user-message');
            inputText.value = '';

            // Process based on button states
            if (deepThinkButton.classList.contains('active')) {
                handleDeepThink(userInput);
            } else if (searchButton.classList.contains('active')) {
                handleSearch(userInput);
            } else {
                processInput(userInput);
            }
        }
    }

    // Event listeners
    sendButton.addEventListener('click', handleInput);
    inputText.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleInput();
        }
    });

    // Button toggle functionality with state management
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            if (isProcessing) return; // Prevent button toggle while processing
            
            if (activeButton === button) {
                // Deactivate current button
                button.classList.remove('active');
                activeButton = null;
            } else {
                // Deactivate previous button and activate new one
                if (activeButton) {
                    activeButton.classList.remove('active');
                }
                button.classList.add('active');
                activeButton = button;
            }
        });
    });

    // Attach file button functionality
    attachButton.addEventListener('click', showAttachDialog);

    // Helper functions
    function addMessage(text, className) {
        const messageDiv = document.createElement('div');
        messageDiv.className = className;
        messageDiv.textContent = text;
        outputText.appendChild(messageDiv);
        outputText.scrollTop = outputText.scrollHeight;
    }

    function showWelcomeDialog() {
        const dialog = document.createElement('div');
        dialog.className = 'dialog';
        dialog.innerHTML = `
            <div class="dialog-content">
                <p>Hello! This is ShallowSeek!<br>You can ask me any question you want!<br>Copyright © 2025 ShallowSeek by George Xiong, All Rights Reserved.</p>
                <button class="control-button">OK</button>
            </div>
        `;
        document.body.appendChild(dialog);

        dialog.querySelector('button').addEventListener('click', () => {
            dialog.remove();
        });
    }

    function showAttachDialog() {
        const dialog = document.createElement('div');
        dialog.className = 'dialog';
        dialog.innerHTML = `
            <div class="dialog-content">
                <p>Attach File is Unavailable</p>
                <button class="control-button">OK</button>
            </div>
        `;
        document.body.appendChild(dialog);

        dialog.querySelector('button').addEventListener('click', () => {
            dialog.remove();
        });
    }

    async function handleDeepThink(input) {
        const thinkTime = Math.floor(Math.random() * 16) + 5; // 5-20 seconds
        const thinkingMessage = `thinking for ${thinkTime} seconds`;
        const thinkingDiv = document.createElement('div');
        thinkingDiv.className = 'assistant-message';
        thinkingDiv.textContent = thinkingMessage;
        outputText.appendChild(thinkingDiv);

        let dots = 0;
        const interval = setInterval(() => {
            thinkingDiv.textContent = thinkingMessage + '.'.repeat(dots + 1);
            dots = (dots + 1) % 3;
        }, 500);

        await new Promise(resolve => setTimeout(resolve, thinkTime * 1000));
        clearInterval(interval);
        processInput(input);
    }

    async function handleSearch(input) {
        addMessage('searching through the web...', 'assistant-message');
        await new Promise(resolve => setTimeout(resolve, 3000));
        processInput(input);
    }

    async function processInput(input) {
        if (isProcessing) return;
        
        try {
            isProcessing = true;
            buttons.forEach(btn => btn.disabled = true);
            sendButton.disabled = true;
            
            addMessage('Processing...', 'processing-message');
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 30000); // 30s timeout
            
            const response = await fetch('http://localhost:3000/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ input }),
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error('Server endpoint not found. Please check if the server is running.');
                } else if (response.status === 500) {
                    throw new Error('Internal server error. Please try again later.');
                } else {
                    throw new Error(`Server error: ${response.status} ${response.statusText}`);
                }
            }
            
            const data = await response.json();
            if (!data || !data.response) {
                throw new Error('Invalid response from server');
            }
            
            addMessage(data.response, 'assistant-message');
        } catch (error) {
            if (error.name === 'AbortError') {
                addMessage('Request timed out. Please try again.', 'error-message');
            } else if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
                addMessage('The server is busy. Please try again later.', 'error-message');
            } else {
                addMessage(`Error: ${error.message}`, 'error-message');
            }
        } finally {
            isProcessing = false;
            buttons.forEach(btn => btn.disabled = false);
            sendButton.disabled = false;
        }
    }
});

// Add dialog styles
document.head.insertAdjacentHTML('beforeend', `
<style>
.dialog {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.dialog-content {
    background: #2B2D31;
    padding: 30px;
    border-radius: 8px;
    text-align: center;
    max-width: 500px;
    width: 90%;
}

.dialog-content p {
    margin-bottom: 20px;
    line-height: 1.5;
}

.dialog-content button {
    min-width: 100px;
}
</style>
`);