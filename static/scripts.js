// =========================================
// TravelMate AI - Chat JavaScript
// =========================================


// =========================================
// DOM ELEMENTS
// =========================================

const chatForm = document.getElementById("chat-form");

const messageInput = document.getElementById("message-input");

const chatWindow = document.getElementById("chat-window");

const sendButton = document.getElementById("send-button");

const typingIndicator =
    document.getElementById("typing-indicator");

const errorBanner =
    document.getElementById("error-banner");

const quickPrompts =
    document.querySelectorAll(".quick-prompt");


// =========================================
// ADD MESSAGE TO CHAT
// =========================================

function addMessage(message, sender) {

    const messageWrapper =
        document.createElement("div");

    messageWrapper.classList.add(
        "message"
    );

    if (sender === "user") {

        messageWrapper.classList.add(
            "user-message"
        );

    } else {

        messageWrapper.classList.add(
            "bot-message"
        );
    }


    // Avatar
    const avatar =
        document.createElement("div");

    avatar.classList.add("avatar");

    avatar.textContent =
        sender === "user" ? "👤" : "✈️";


    // Content
    const content =
        document.createElement("div");

    content.classList.add(
        "message-content"
    );


    // Name
    const name =
        document.createElement("div");

    name.classList.add(
        "message-name"
    );

    name.textContent =
        sender === "user"
            ? "You"
            : "TravelMate AI";


    // Message bubble
    const bubble =
        document.createElement("div");

    bubble.classList.add(
        "message-bubble"
    );


    // Convert text safely into formatted HTML
    bubble.innerHTML =
        formatMessage(message);


    content.appendChild(name);

    content.appendChild(bubble);


    messageWrapper.appendChild(avatar);

    messageWrapper.appendChild(content);


    chatWindow.appendChild(
        messageWrapper
    );


    scrollToBottom();
}


// =========================================
// FORMAT BOT MESSAGE
// =========================================

function formatMessage(text) {

    if (!text) {
        return "";
    }


    // Escape HTML first
    let formatted =
        escapeHtml(text);


    // Bold markdown
    formatted =
        formatted.replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        );


    // Convert line breaks
    formatted =
        formatted.replace(
            /\n/g,
            "<br>"
        );


    return formatted;
}


// =========================================
// ESCAPE HTML
// =========================================

function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


// =========================================
// SCROLL CHAT TO BOTTOM
// =========================================

function scrollToBottom() {

    chatWindow.scrollTop =
        chatWindow.scrollHeight;
}


// =========================================
// SHOW TYPING INDICATOR
// =========================================

function showTyping() {

    typingIndicator.classList.remove(
        "hidden"
    );

    scrollToBottom();
}


// =========================================
// HIDE TYPING INDICATOR
// =========================================

function hideTyping() {

    typingIndicator.classList.add(
        "hidden"
    );
}


// =========================================
// SHOW ERROR
// =========================================

function showError(message) {

    errorBanner.textContent =
        message;

    errorBanner.classList.remove(
        "hidden"
    );
}


// =========================================
// HIDE ERROR
// =========================================

function hideError() {

    errorBanner.classList.add(
        "hidden"
    );

    errorBanner.textContent = "";
}


// =========================================
// SEND MESSAGE TO FLASK
// =========================================

async function sendMessage(message) {

    message =
        message.trim();


    if (!message) {
        return;
    }


    // Hide previous error
    hideError();


    // Show user's message
    addMessage(
        message,
        "user"
    );


    // Clear input
    messageInput.value = "";


    // Disable input
    messageInput.disabled = true;

    sendButton.disabled = true;


    // Show typing animation
    showTyping();


    try {

        const response =
            await fetch(
                "/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })
                }
            );


        const data =
            await response.json();


        hideTyping();


        // Server error
        if (!response.ok) {

            throw new Error(
                data.error ||
                "Something went wrong."
            );
        }


        // Check bot response
        if (!data.response) {

            throw new Error(
                "TravelMate did not return a response."
            );
        }


        // Show TravelMate response
        addMessage(
            data.response,
            "bot"
        );


    } catch (error) {

        hideTyping();

        console.error(
            "TravelMate Error:",
            error
        );


        showError(
            error.message ||
            "Unable to connect to TravelMate."
        );


    } finally {

        // Enable input again
        messageInput.disabled = false;

        sendButton.disabled = false;


        // Put cursor back
        messageInput.focus();
    }
}


// =========================================
// FORM SUBMIT
// =========================================

chatForm.addEventListener(
    "submit",
    function (event) {

        event.preventDefault();


        const message =
            messageInput.value.trim();


        if (!message) {
            return;
        }


        sendMessage(message);
    }
);


// =========================================
// QUICK PROMPTS
// =========================================

quickPrompts.forEach(
    function (button) {

        button.addEventListener(
            "click",
            function () {

                const prompt =
                    button.dataset.prompt;


                if (!prompt) {
                    return;
                }


                messageInput.value =
                    prompt;


                messageInput.focus();
            }
        );
    }
);


// =========================================
// ENTER KEY
// =========================================

messageInput.addEventListener(
    "keydown",
    function (event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            chatForm.requestSubmit();
        }
    }
);


// =========================================
// INITIAL FOCUS
// =========================================

window.addEventListener(
    "load",
    function () {

        messageInput.focus();

        scrollToBottom();
    }
);
