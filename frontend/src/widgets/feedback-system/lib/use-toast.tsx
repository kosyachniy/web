'use client';

import { useState, useCallback } from 'react';

interface ToastOptions {
  title: string;
  description?: string;
  variant?: 'default' | 'destructive' | 'success';
}

// Simple toast implementation for now
export function useToast() {
  const [toasts, setToasts] = useState<ToastOptions[]>([]);

  const toast = useCallback((options: ToastOptions) => {
    // For now, we'll just use console.log as a fallback
    console.log(`Toast: ${options.title}`, options.description);
    
    // In a full implementation, this would trigger a visual toast
    setToasts(prev => [...prev, options]);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
      setToasts(prev => prev.slice(1));
    }, 3000);
  }, []);

  return {
    toast,
    toasts,
  };
}