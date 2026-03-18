<template>
  <div class="conversations-container">
    <h1>Messages</h1>
    
    <div v-if="loading" class="loading">Loading conversations...</div>
    
    <div v-else-if="conversations.length === 0" class="no-conversations">
      <h3>No conversations yet</h3>
      <p>Match with someone to start chatting!</p>
      <router-link to="/browse" class="btn-primary">Browse Profiles</router-link>
    </div>
    
    <div v-else class="conversations-list">
      <div 
        v-for="conv in conversations" 
        :key="conv.user_id" 
        class="conversation-item"
        :class="{ unread: conv.unread_count > 0 }"
        @click="openChat(conv.user_id)"
      >
        <div class="conversation-avatar">
          <img v-if="conv.profile_picture" :src="`http://localhost:5000/uploads/${conv.profile_picture}`" alt="Profile" />
          <div v-else class="avatar-placeholder">{{ conv.user_name?.charAt(0) }}</div>
        </div>
        
        <div class="conversation-content">
          <div class="conversation-header">
            <h3>{{ conv.user_name }}</h3>
            <span class="time">{{ formatTime(conv.last_message_at) }}</span>
          </div>
          <p class="last-message">{{ conv.last_message || 'No messages yet' }}</p>
        </div>
        
        <div v-if="conv.unread_count > 0" class="unread-badge">
          {{ conv.unread_count }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import messageService from '../services/messageService';
import socketService from '../services/socketService';

const router = useRouter();
const conversations = ref([]);
const loading = ref(true);

const loadConversations = async () => {
  try {
    conversations.value = await messageService.getConversations();
  } catch (error) {
    console.error('Failed to load conversations:', error);
  } finally {
    loading.value = false;
  }
};

const openChat = (userId) => {
  router.push(`/chat/${userId}`);
};

const formatTime = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  const now = new Date();
  const diff = now - date;
  
  if (diff < 60000) return 'now';
  if (diff < 3600000) return `${Math.floor(diff / 60000)}m`;
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}h`;
  if (diff < 604800000) return `${Math.floor(diff / 86400000)}d`;
  return date.toLocaleDateString();
};

const handleNewMessage = (data) => {
  loadConversations();
};

onMounted(() => {
  loadConversations();
  socketService.on('new_message', handleNewMessage);
});

onUnmounted(() => {
  socketService.off('new_message', handleNewMessage);
});
</script>

<style scoped>
.conversations-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}

.conversations-list {
  display: flex;
  flex-direction: column;
}

.conversation-item {
  display: flex;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background 0.2s;
}

.conversation-item:hover {
  background: #f9f9f9;
}

.conversation-item.unread {
  background: #f0f7ff;
}

.conversation-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 15px;
  flex-shrink: 0;
}

.conversation-avatar img {
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
  font-size: 20px;
  font-weight: bold;
}

.conversation-content {
  flex: 1;
  min-width: 0;
}

.conversation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.conversation-header h3 {
  font-size: 16px;
  margin: 0;
}

.time {
  font-size: 12px;
  color: #888;
}

.last-message {
  color: #666;
  font-size: 14px;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.unread-badge {
  background: #ff6b6b;
  color: white;
  border-radius: 50%;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  margin-left: 10px;
}

.no-conversations {
  text-align: center;
  padding: 40px;
}

.btn-primary {
  display: inline-block;
  background: #ff6b6b;
  color: white;
  padding: 10px 20px;
  border-radius: 20px;
  text-decoration: none;
  margin-top: 15px;
}
</style>
