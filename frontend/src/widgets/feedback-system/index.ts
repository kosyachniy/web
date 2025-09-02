import React from 'react';

export { useToast } from './lib/use-toast';

// Stub providers to satisfy existing imports
export const ToastProvider = ({ children }: { children?: React.ReactNode }) => children || null;
export const PopupProvider = ({ children }: { children: React.ReactNode }) => children;

// Stub hook to satisfy existing imports
export const usePopupActions = () => ({
  showPopup: (content: React.ReactNode) => console.log('Popup:', content),
  hidePopup: () => console.log('Hide popup'),
  alert: (options: { title?: string; message?: string; [key: string]: unknown }) => Promise.resolve(console.log('Alert:', options)),
  confirm: (options: { title?: string; message?: string; [key: string]: unknown }) => Promise.resolve(true),
  confirmDelete: (options: string | { title?: string; message?: string; [key: string]: unknown }) => Promise.resolve(true),
  success: (options: string | { title?: string; message?: string; [key: string]: unknown }) => Promise.resolve(console.log('Success:', options)),
  error: (options: string | { title?: string; message?: string; [key: string]: unknown }) => Promise.resolve(console.log('Error:', options)),
  show: (options: { title?: string; message?: string; [key: string]: unknown }) => Promise.resolve(console.log('Show:', options)),
  close: () => console.log('Close'),
});
