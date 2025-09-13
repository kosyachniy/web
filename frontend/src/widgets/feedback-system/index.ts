// Re-export the real implementations from the ui directory
export { ToastProvider } from './ui/ToastProvider';
export { PopupProvider, usePopupActions } from './ui/PopupProvider';
export { default as Popup } from './ui/Popup';

// Re-export toast functionality from shared hooks for consistency
export { useToast } from '@/shared/hooks/useToast';
