import apiClient from './client';
import { ConversationsResponse, ConversationMessagesResponse, CreateConversationResponse, UnreadMessagesResponse, Message } from '../types/message';

export const messagesApi = {
  // 会話一覧を取得
  getConversations: async (): Promise<ConversationsResponse> => {
    const response = await apiClient.get('/api/messages/conversations/');
    return response.data as ConversationsResponse;
  },

  // 会話のメッセージ一覧を取得
  getConversationMessages: async (conversationId: number): Promise<ConversationMessagesResponse> => {
    const response = await apiClient.get(`/api/messages/conversations/${conversationId}/`);
    return response.data as ConversationMessagesResponse;
  },

  // メッセージを送信
  sendMessage: async (conversationId: number, content: string): Promise<{ message: Message }> => {
    const response = await apiClient.post(`/api/messages/conversations/${conversationId}/send/`, {
      content
    });
    return response.data as { message: Message };
  },

  // 新しい会話を作成
  createConversation: async (userId: number): Promise<CreateConversationResponse> => {
    const response = await apiClient.post('/api/messages/conversations/create/', {
      user_id: userId
    });
    return response.data as CreateConversationResponse;
  },

  // 未読メッセージ数を取得
  getUnreadMessagesCount: async (): Promise<UnreadMessagesResponse> => {
    const response = await apiClient.get('/api/messages/unread-count/');
    return response.data as UnreadMessagesResponse;
  },

  // 会話のメッセージを既読にする
  markConversationRead: async (conversationId: number): Promise<{ message: string }> => {
    const response = await apiClient.post(`/api/messages/conversations/${conversationId}/read/`);
    return response.data as { message: string };
  },

  // メッセージを削除
  deleteMessage: async (messageId: number): Promise<{ message: string }> => {
    const response = await apiClient.delete(`/api/messages/${messageId}/delete/`);
    return response.data as { message: string };
  },

  // 会話を検索
  searchConversations: async (query: string): Promise<ConversationsResponse> => {
    const response = await apiClient.get(`/api/messages/conversations/search/?q=${query}`);
    return response.data as ConversationsResponse;
  },
}; 