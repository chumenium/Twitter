import { User } from './auth';

export interface Message {
  id: number;
  sender: User;
  content: string;
  is_read: boolean;
  created_at: string;
}

export interface Conversation {
  id: number;
  participants: User[];
  last_message?: Message;
  unread_count: number;
  other_participant?: User;
  created_at: string;
  updated_at: string;
}

export interface ConversationsResponse {
  conversations: Conversation[];
  count: number;
}

export interface ConversationMessagesResponse {
  messages: Message[];
  conversation: Conversation;
  count: number;
}

export interface CreateConversationResponse {
  conversation: Conversation;
  is_new: boolean;
}

export interface UnreadMessagesResponse {
  unread_count: number;
} 