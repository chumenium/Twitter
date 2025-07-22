import { ApiResponse } from '../types';

export const handleApiError = (error: any): string => {
  if (error.response?.data?.message) {
    return error.response.data.message;
  }
  if (error.message) {
    return error.message;
  }
  return '予期しないエラーが発生しました';
};

export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  const now = new Date();
  const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));
  
  if (diffInMinutes < 1) return '今';
  if (diffInMinutes < 60) return `${diffInMinutes}分前`;
  
  const diffInHours = Math.floor(diffInMinutes / 60);
  if (diffInHours < 24) return `${diffInHours}時間前`;
  
  const diffInDays = Math.floor(diffInHours / 24);
  if (diffInDays < 7) return `${diffInDays}日前`;
  
  return date.toLocaleDateString('ja-JP');
};

export const validateImageFile = (file: File): string | null => {
  const maxSize = 5 * 1024 * 1024; // 5MB
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
  
  if (file.size > maxSize) {
    return '画像サイズは5MB以下にしてください';
  }
  
  if (!allowedTypes.includes(file.type)) {
    return 'JPEG、PNG、GIF形式の画像のみアップロード可能です';
  }
  
  return null;
}; 