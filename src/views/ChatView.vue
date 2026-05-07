<template>
  <div class="chat-container">
    <div class="chat-header">
      <button class="back-btn" @click="goBack">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="back-icon"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
            clip-rule="evenodd"
          />
        </svg>
      </button>
      <div v-if="otherUser" class="chat-user-info">
        <div class="avatar">
          <img
            v-if="otherUser.profile_picture"
            :src="`${API_BASE_URL}/uploads/${otherUser.profile_picture}`"
            alt="Profile"
          />
          <div v-else class="avatar-placeholder">
            {{ otherUser.name?.charAt(0) }}
          </div>
        </div>
        <div class="user-details">
          <h2>{{ otherUser.name }}</h2>
          <span v-if="typing" class="typing-status">typing...</span>
        </div>
      </div>
    </div>

    <div ref="messagesContainer" class="messages-container">
      <div v-if="loading" class="loading">
        <div class="loading-spinner"></div>
        <p>Loading messages...</p>
      </div>

      <div v-else-if="hasMore" class="load-more">
        <button class="load-more-btn" @click="loadMore">
          Load earlier messages
        </button>
      </div>

      <div
        v-for="message in messages"
        :key="message.id"
        class="message"
        :class="{
          sent: message.sender_id === currentUserId,
          received: message.sender_id !== currentUserId,
        }"
      >
        <div class="message-bubble">
          <p>{{ message.content }}</p>
          <div class="message-meta">
            <span class="time">{{ formatTime(message.created_at) }}</span>
            <span v-if="message.sender_id === currentUserId" class="status">
              <svg
                v-if="message.read_at"
                xmlns="http://www.w3.org/2000/svg"
                class="read-icon"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                />
              </svg>
              <svg
                v-else
                xmlns="http://www.w3.org/2000/svg"
                class="read-icon"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clip-rule="evenodd"
                />
              </svg>
            </span>
          </div>
        </div>
      </div>

      <div v-if="typing" class="typing-indicator">
        <div class="typing-dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
        <span>{{ typingUserName }} is typing...</span>
      </div>
    </div>

    <form class="message-form" @submit.prevent="sendMessage">
      <input
        v-model="newMessage"
        type="text"
        placeholder="Type a message..."
        maxlength="1000"
        class="message-input"
        @input="handleTyping"
      />
      <button type="submit" :disabled="!newMessage.trim()" class="send-btn">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="send-icon"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"
          />
        </svg>
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from "vue";
import { useRoute, useRouter } from "vue-router";
import messageService from "../services/messageService";
import socketService from "../services/socketService";
import authService from "../services/authService";
import { API_BASE_URL } from "../services/api";

const route = useRoute();
const router = useRouter();

const otherUserId = parseInt(route.params.userId);
const currentUserId = authService.getStoredUser()?.id;

const messages = ref([]);
const otherUser = ref(null);
const newMessage = ref("");
const loading = ref(true);
const typing = ref(false);
const typingUserName = ref("");
const hasMore = ref(true);
const messagesContainer = ref(null);

let typingSendTimeout = null;

const loadMessages = async (page = 1, prepend = false) => {
  try {
    const data = await messageService.getMessageHistory(otherUserId, page);
    if (prepend) {
      messages.value = [...data.messages, ...messages.value];
    } else {
      messages.value = data.messages;
    }
    otherUser.value = data.other_user;
    hasMore.value = data.has_next;
    await nextTick();
    if (!prepend) scrollToBottom();
  } catch (error) {
    console.error("Failed to load messages:", error);
    if (error.response?.status === 403) {
      router.push("/matches");
    }
  } finally {
    loading.value = false;
  }
};

const loadMore = async () => {
  const nextPage = Math.floor(messages.value.length / 50) + 1;
  await loadMessages(nextPage, true);
};

const sendMessage = async () => {
  if (!newMessage.value.trim()) return;

  const content = newMessage.value.trim();
  newMessage.value = "";

  try {
    const message = await messageService.sendMessage(otherUserId, content);
    messages.value.unshift(message);
    await nextTick();
    scrollToBottom();
  } catch (error) {
    console.error("Failed to send message:", error);
  }
};

const handleTyping = () => {
  if (typingSendTimeout) clearTimeout(typingSendTimeout);

  messageService.sendTypingStatus(otherUserId, true);

  typingSendTimeout = setTimeout(() => {
    messageService.sendTypingStatus(otherUserId, false);
  }, 2000);
};

const handleNewMessage = (data) => {
  if (data.sender_id === otherUserId) {
    messages.value.unshift({
      id: Date.now(),
      sender_id: data.sender_id,
      receiver_id: currentUserId,
      content: data.content,
      created_at: data.created_at,
      read_at: null,
    });
    nextTick(() => scrollToBottom());
  }
};

const handleTypingStatus = (data) => {
  if (data.user_id === otherUserId) {
    typing.value = data.is_typing;
    typingUserName.value = data.user_name;
  }
};

const handleMessageRead = (data) => {
  const message = messages.value.find((m) => m.id === data.message_id);
  if (message) {
    message.read_at = data.read_at;
  }
};

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

const formatTime = (dateString) => {
  if (!dateString) return "";
  const date = new Date(dateString);
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
};

const goBack = () => {
  router.push("/messages");
};

onMounted(() => {
  loadMessages();
  socketService.on("new_message", handleNewMessage);
  socketService.on("user_typing", handleTypingStatus);
  socketService.on("message_read", handleMessageRead);
});

onUnmounted(() => {
  socketService.off("new_message", handleNewMessage);
  socketService.off("user_typing", handleTypingStatus);
  socketService.off("message_read", handleMessageRead);
  messageService.sendTypingStatus(otherUserId, false);
});
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 8rem);
  max-width: 600px;
  margin: 0 auto;
  background: var(--bg);
  border-radius: 1rem;
  overflow: hidden;
}

[data-theme="dark"] .chat-container {
  background: var(--surface);
}

.chat-header {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: var(--bg);
  border-bottom: 1px solid var(--border);
}

[data-theme="dark"] .chat-header {
  background: var(--surface);
  border-color: var(--border);
}

.back-btn {
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  border-radius: 0.5rem;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.back-btn:hover {
  background: var(--surface);
}

.back-icon {
  width: 20px;
  height: 20px;
  color: var(--text-primary);
}

[data-theme="dark"] .back-icon {
  color: var(--text-primary);
}

.chat-user-info {
  display: flex;
  align-items: center;
  margin-left: 0.75rem;
}

.avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 0.75rem;
  border: 2px solid var(--primary);
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  color: var(--text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  font-weight: bold;
}

.user-details h2 {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.typing-status {
  font-size: 0.75rem;
  color: var(--primary);
  font-weight: 500;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.load-more {
  text-align: center;
  margin-bottom: 1rem;
}

.load-more-btn {
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  cursor: pointer;
  font-size: 0.8rem;
  color: var(--primary);
  transition: all 0.2s;
}

.load-more-btn:hover {
  background: var(--border);
}

.message {
  display: flex;
  margin-bottom: 0.25rem;
}

.message.sent {
  justify-content: flex-end;
}

.message.received {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 75%;
  padding: 0.7rem 1rem;
  border-radius: 1.25rem;
}

.sent .message-bubble {
  background: linear-gradient(135deg, var(--primary-light), var(--primary));
  color: var(--bg);
  border-bottom-right-radius: 0.4rem;
}

.received .message-bubble {
  background: var(--chat-other);
  border: 1px solid var(--border);
  color: var(--text-primary);
  border-bottom-left-radius: 0.4rem;
}

[data-theme="dark"] .received .message-bubble {
  background: var(--chat-other);
  border-color: var(--border);
  color: var(--text-primary);
}

.message-bubble p {
  margin: 0;
  word-wrap: break-word;
  font-size: 0.9rem;
  line-height: 1.4;
}

.message-meta {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin-top: 0.3rem;
  font-size: 0.65rem;
  gap: 0.3rem;
}

.received .message-meta {
  color: var(--text-secondary);
}

.status {
  color: var(--bg);
}

.read-icon {
  width: 14px;
  height: 14px;
}

.typing-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  color: var(--text-secondary);
  font-size: 0.8rem;
}

.typing-dots {
  display: flex;
  gap: 0.25rem;
}

.typing-dots span {
  width: 6px;
  height: 6px;
  background: var(--primary);
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) {
  animation-delay: 0s;
}
.typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}
.typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%,
  60%,
  100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-4px);
  }
}

.message-form {
  display: flex;
  padding: 1rem;
  border-top: 1px solid var(--border);
  background: var(--bg);
}

[data-theme="dark"] .message-form {
  background: var(--surface);
  border-color: var(--border);
}

.message-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border);
  border-radius: 9999px;
  outline: none;
  font-size: 0.9rem;
  background: var(--bg);
  color: var(--text-primary);
  transition: all 0.2s;
}

[data-theme="dark"] .message-input {
  background: var(--input-bg);
  border-color: var(--border);
  color: var(--text-primary);
}

.message-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px var(--surface);
}

.send-btn {
  margin-left: 0.75rem;
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, var(--primary-light), var(--primary));
  color: var(--bg);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-btn:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: var(--shadow-md);
}

.send-btn:disabled {
  background: var(--text-secondary);
  cursor: not-allowed;
}

.send-icon {
  width: 20px;
  height: 20px;
}

.loading {
  text-align: center;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--border);
  border-top-color: var(--primary);
  border-radius: 50%;
  margin-bottom: 0.75rem;
  animation: spin 0.8s linear infinite;
}

.loading p {
  color: var(--text-secondary);
  font-size: 0.85rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
