'use client';

import { useCallback } from 'react';
import { toast as sonnerToast } from 'sonner';
import { useAppDispatch, useAppSelector } from '@/shared/stores/store';
import {
    addToast,
    removeToast,
    updateToast,
    clearAllToasts,
    setToastPosition,
    setMaxToasts,
    setDefaultDuration,
    type AddToastPayload,
    type Toast,
} from '@/shared/stores/toastSlice';

// Extended interface for the hook that includes action (not stored in Redux)
interface ToastOptions extends AddToastPayload {
    action?: {
        label: string;
        onClick: () => void;
    };
}

export interface UseToastReturn {
    // Toast actions
    toast: (message: string, options?: Partial<ToastOptions>) => string;
    success: (message: string, options?: Partial<ToastOptions>) => string;
    error: (message: string, options?: Partial<ToastOptions>) => string;
    warning: (message: string, options?: Partial<ToastOptions>) => string;
    info: (message: string, options?: Partial<ToastOptions>) => string;
    loading: (message: string, options?: Partial<ToastOptions>) => string;

    // Toast management
    dismiss: (toastId: string) => void;
    dismissAll: () => void;
    update: (toastId: string, updates: Partial<Omit<Toast, 'id' | 'createdAt'>>) => void;

    // Promise-based toasts
    promise: <T>(
        promise: Promise<T>,
        options: {
            loading: string;
            success: string | ((data: T) => string);
            error: string | ((error: unknown) => string);
        }
    ) => Promise<T>;

    // Settings
    setPosition: (position: Toast['position']) => void;
    setMaxToasts: (max: number) => void;
    setDefaultDuration: (duration: number) => void;

    // State
    toasts: Toast[];
    position: Toast['position'];
    maxToasts: number;
    defaultDuration: number;
}

export function useToast(): UseToastReturn {
    const dispatch = useAppDispatch();
    const { toasts, position, maxToasts, defaultDuration } = useAppSelector((state) => state.toast);

    const showToast = useCallback((
        message: string,
        options: Partial<ToastOptions> = {}
    ): string => {
        const toastId = `toast_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

        // Separate action function from options to avoid storing in Redux
        const { action, ...reduxOptions } = options;

        // Add to Redux store (without the non-serializable action function)
        dispatch(addToast({ message, ...reduxOptions }));

        // Show with Sonner (with the action function)
        const toastConfig = {
            id: toastId,
            duration: options.duration === 0 ? Infinity : (options.duration ?? defaultDuration),
            description: options.description,
            action: action ? {
                label: action.label,
                onClick: action.onClick,
            } : undefined,
            dismissible: options.dismissible ?? true,
            onDismiss: () => {
                dispatch(removeToast(toastId));
            },
            onAutoClose: () => {
                dispatch(removeToast(toastId));
            },
        };

        const displayMessage = options.title
            ? `${options.title}: ${message}`
            : message;

        switch (options.type) {
            case 'success':
                sonnerToast.success(displayMessage, toastConfig);
                break;
            case 'error':
                sonnerToast.error(displayMessage, toastConfig);
                break;
            case 'warning':
                sonnerToast.warning(displayMessage, toastConfig);
                break;
            case 'info':
                sonnerToast.info(displayMessage, toastConfig);
                break;
            case 'loading':
                sonnerToast.loading(displayMessage, toastConfig);
                break;
            default:
                sonnerToast(displayMessage, toastConfig);
                break;
        }

        return toastId;
    }, [dispatch, defaultDuration]);

    const success = useCallback((message: string, options?: Partial<ToastOptions>) => {
        return showToast(message, { ...options, type: 'success' });
    }, [showToast]);

    const error = useCallback((message: string, options?: Partial<ToastOptions>) => {
        return showToast(message, { ...options, type: 'error' });
    }, [showToast]);

    const warning = useCallback((message: string, options?: Partial<ToastOptions>) => {
        return showToast(message, { ...options, type: 'warning' });
    }, [showToast]);

    const info = useCallback((message: string, options?: Partial<ToastOptions>) => {
        return showToast(message, { ...options, type: 'info' });
    }, [showToast]);

    const loading = useCallback((message: string, options?: Partial<ToastOptions>) => {
        return showToast(message, { ...options, type: 'loading', duration: 0 });
    }, [showToast]);

    const dismiss = useCallback((toastId: string) => {
        dispatch(removeToast(toastId));
        sonnerToast.dismiss(toastId);
    }, [dispatch]);

    const dismissAll = useCallback(() => {
        dispatch(clearAllToasts());
        sonnerToast.dismiss();
    }, [dispatch]);

    const update = useCallback((toastId: string, updates: Partial<Omit<Toast, 'id' | 'createdAt'>>) => {
        dispatch(updateToast({ id: toastId, updates }));
        // Note: Sonner doesn't support updating toasts, so we'd need to dismiss and recreate
        // For now, we just update the Redux state
    }, [dispatch]);

    const promiseToast = useCallback(async <T>(
        promise: Promise<T>,
        options: {
            loading: string;
            success: string | ((data: T) => string);
            error: string | ((error: unknown) => string);
        }
    ): Promise<T> => {
        const loadingToastId = loading(options.loading);

        try {
            const result = await promise;
            dismiss(loadingToastId);

            const successMessage = typeof options.success === 'function'
                ? options.success(result)
                : options.success;
            success(successMessage);

            return result;
        } catch (err) {
            dismiss(loadingToastId);

            const errorMessage = typeof options.error === 'function'
                ? options.error(err)
                : options.error;
            error(errorMessage);

            throw err;
        }
    }, [loading, dismiss, success, error]);

    const setPositionHandler = useCallback((newPosition: Toast['position']) => {
        dispatch(setToastPosition(newPosition));
    }, [dispatch]);

    const setMaxToastsHandler = useCallback((max: number) => {
        dispatch(setMaxToasts(max));
    }, [dispatch]);

    const setDefaultDurationHandler = useCallback((duration: number) => {
        dispatch(setDefaultDuration(duration));
    }, [dispatch]);

    return {
        toast: showToast,
        success,
        error,
        warning,
        info,
        loading,
        dismiss,
        dismissAll,
        update,
        promise: promiseToast,
        setPosition: setPositionHandler,
        setMaxToasts: setMaxToastsHandler,
        setDefaultDuration: setDefaultDurationHandler,
        toasts,
        position,
        maxToasts,
        defaultDuration,
    };
}

// Convenience hooks for specific toast types
export const useToastActions = () => {
    const { success, error, warning, info, loading, promise } = useToast();

    return {
        success,
        error,
        warning,
        info,
        loading,
        promise,
        // Common patterns
        saveSuccess: (item = 'Item') => success(`${item} saved successfully!`),
        saveError: (item = 'Item') => error(`Failed to save ${item.toLowerCase()}`),
        deleteSuccess: (item = 'Item') => success(`${item} deleted successfully!`),
        deleteError: (item = 'Item') => error(`Failed to delete ${item.toLowerCase()}`),
        loadingOperation: (operation = 'Processing') => loading(`${operation}...`),
    };
};
