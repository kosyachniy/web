'use client';

import { useEffect } from 'react';
import { Toaster } from 'sonner';
import { useAppDispatch, useAppSelector } from '@/shared/stores/store';
import { cleanupExpiredToasts } from '@/shared/stores/toastSlice';

export function ToastProvider() {
    const dispatch = useAppDispatch();
    const { position, maxToasts } = useAppSelector((state) => state.toast);

    // Clean up expired toasts periodically
    useEffect(() => {
        const interval = setInterval(() => {
            dispatch(cleanupExpiredToasts());
        }, 5000); // Check every 5 seconds

        return () => clearInterval(interval);
    }, [dispatch]);

    return (
        <Toaster
            position={position}
            richColors={false}
            closeButton
            expand={true}
            visibleToasts={maxToasts}
            toastOptions={{
                style: {
                    background: 'var(--background)',
                    color: 'var(--foreground)',
                    border: '1px solid var(--border)',
                    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
                    backdropFilter: 'none',
                    opacity: '1',
                },
                className: 'sonner-toast',
                duration: 4000,
                unstyled: false,
            }}
            theme={undefined}
        />
    );
}

export default ToastProvider;
