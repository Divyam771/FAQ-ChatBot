const chatWindow = document.getElementById("chat-window");
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");

function appendMessage(text, sender) {
  const div = document.createElement("div");
  div.classList.add("message", sender);
  div.textContent = text;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendMessage(message) {
  appendMessage(message, "user");
  userInput.value = "";

  try {
    const response = await fetch("/get_response", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const data = await response.json();
    appendMessage(data.answer, "bot");
  } catch (err) {
    appendMessage("Oops, something went wrong. Please try again.", "bot");
  }
}

chatForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const message = userInput.value.trim();
  if (message) sendMessage(message);
});

function sendSuggested(question) {
  sendMessage(question);
}
