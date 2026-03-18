<template>
  <div class="chat-container">
    <div class="chat-header">
      <button class="back-btn" @click="goBack">←</button>
      <div class="chat-user-info" v-if="otherUser">
        <div class="avatar">
          <img v-if="otherUser.profile_picture" :src="`http://localhost:5000/uploads/${otherUser.profile_picture}`" alt="Profile" />
          <div v-else class="avatar-placeholder">{{ otherUser.name?.charAt(0) }}</div>
        </div>
        <h2>{{ otherUser.name }}</h2>
      </div>
    </div>
    
    <div class="messages-container" ref="messagesContainer">
      <div v-if="loading" class="loading">Loading messages...</div>
      
      <div v-else-if="hasMore" class="load-more">
        <button @click="loadMore">Load earlier messages</button>
      </div>
      
      <div 
        v-for="message in messages" 
        :key="message.id" 
        class="message"
        :class="{ sent: message.sender_id === currentUserId, received: message.sender_id !== currentUserId }"
      >
        <div class="message-bubble">
          <p>{{ message.content }}</p>
          <div class="message-meta">
            <span class="time">{{ formatTime(message.created_at) }}</span>
            <span v-if="message.sender_id === currentUserId" class="status">
              {{ message.read_at ? '✓✓' : '✓' }}
            </span>
          </div>
        </div>
      </div>
      
      <div v-if="typing" class="typing-indicator">
        <span>{{ typingUserName }} is typing...</span>
      </div>
    </div>
    
    <form class="message-form" @submit.prevent="sendMessage">
      <input 
        v-model="newMessage" 
        type="text" 
        placeholder="Type a message..."
        @input="handleTyping"
        maxlength="1000"
      />
      <button type="submit" :disabled="!newMessage.trim()">Send</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import messageService from '../services/messageService';
import socketService from '../services/socketService';
import authService from '../services/authService';

const route = useRoute();
const router = useRouter();

const otherUserId = parseInt(route.params.userId);
const currentUserId = authService.getStoredUser()?.id;

const messages = ref([]);
const otherUser = ref(null);
const newMessage = ref('');
const loading = ref(true);
const typing = ref(false);
const typingUserName = ref('');
const hasMore = ref(true);
const messagesContainer = ref(null);
const typingTimeout = ref(null);

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
    console.error('Failed to load messages:', error);
    if (error.response?.status === 403) {
      router.push('/matches');
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
  newMessage.value = '';
  
  try {
    const message = await messageService.sendMessage(otherUserId, content);
    messages.value.unshift(message);
    await nextTick();
    scrollToBottom();
  } catch (error) {
    console.error('Failed to send message:', error);
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
      read_at: null
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
  const message = messages.value.find(m => m.id === data.message_id);
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
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

const goBack = () => {
  router.push('/conversations');
};

onMounted(() => {
  loadMessages();
  socketService.on('new_message', handleNewMessage);
  socketService.on('user_typing', handleTypingStatus);
  socketService.on('message_read', handleMessageRead);
});

onUnmounted(() => {
  socketService.off('new_message', handleNewMessage);
  socketService.off('user_typing', handleTypingStatus);
  socketService.off('message_read', handleMessageRead);
  messageService.sendTypingStatus(otherUserId, false);
});
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 600px;
  margin: 0 auto;
}

.chat-header {
  display: flex;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eee;
  background: white;
}

.back-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: 5px 10px;
}

.chat-user-info {
  display: flex;
  align-items: center;
  margin-left: 10px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 10px;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: #ff6b6b;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: bold;
}

.chat-user-info h2 {
  font-size: 18px;
  margin: 0;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
  display: flex;
  flex-direction: column;
}

.load-more {
  text-align: center;
  margin-bottom: 15px;
}

.load-more button {
  background: #f0f0f0;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
}

.message {
  display: flex;
  margin-bottom: 10px;
}

.message.sent {
  justify-content: flex-end;
}

.message.received {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 70%;
  padding: 10px 14px;
  border-radius: 18px;
}

.sent .message-bubble {
  background: #ff6b6b;
  color: white;
  border-bottom-right-radius: 4px;
}

.received .message-bubble {
  background: #f0f0f0;
  color: black;
  border-bottom-left-radius: 4px;
}

.message-bubble p {
  margin: 0;
  word-wrap: break-word;
}

.message-meta {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin-top: 4px;
  font-size: 11px;
  gap: 4px;
}

.received .message-meta {
  color: #666;
}

.status {
  color: rgba(255,255,255,0.8);
}

.typing-indicator {
  padding: 10px;
  color: #888;
  font-style: italic;
}

.message-form {
  display: flex;
  padding: 15px;
  border-top: 1px solid #eee;
  background: white;
}

.message-form input {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 24px;
  outline: none;
  font-size: 14px;
}

.message-form button {
  margin-left: 10px;
  padding: 12px 20px;
  background: #ff6b6b;
  color: white;
  border: none;
  border-radius: 24px;
  cursor: pointer;
}

.message-form button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #888;
}
</style>
