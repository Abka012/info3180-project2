import { io } from 'socket.io-client';
import authService from './authService';

let socket = null;

export const socketService = {
  connect() {
    if (socket?.connected) return socket;
    
    socket = io('http://localhost:5000', {
      transports: ['websocket', 'polling'],
      autoConnect: true
    });
    
    socket.on('connect', () => {
      console.log('Socket connected:', socket.id);
      
      // Subscribe to user notifications
      const user = authService.getStoredUser();
      if (user) {
        socket.emit('subscribe', { user_id: user.id });
      }
    });
    
    socket.on('disconnect', () => {
      console.log('Socket disconnected');
    });
    
    socket.on('connect_error', (error) => {
      console.error('Socket connection error:', error);
    });
    
    return socket;
  },
  
  disconnect() {
    if (socket) {
      const user = authService.getStoredUser();
      if (user) {
        socket.emit('unsubscribe', { user_id: user.id });
      }
      socket.disconnect();
      socket = null;
    }
  },
  
  getSocket() {
    return socket;
  },
  
  on(event, callback) {
    if (socket) {
      socket.on(event, callback);
    }
  },
  
  off(event, callback) {
    if (socket) {
      socket.off(event, callback);
    }
  }
};

export default socketService;
