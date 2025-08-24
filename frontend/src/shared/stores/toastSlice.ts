import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface Toast {
    id: string;
    type: 'success' | 'error' | 'warning' | 'info' | 'loading' | 'default';
    title?: string;
    message: string;
    description?: string;
    duration?: number;
    // action is not stored in Redux state to avoid serialization issues
    // Actions are handled directly in the useToast hook with Sonner
    dismissible?: boolean;
    position?: 'top-left' | 'top-center' | 'top-right' | 'bottom-left' | 'bottom-center' | 'bottom-right';
    createdAt: number;
}

export interface ToastState {
    toasts: Toast[];
    defaultDuration: number;
    maxToasts: number;
    position: Toast['position'];
}

const initialState: ToastState = {
    toasts: [],
    defaultDuration: 4000,
    maxToasts: 5,
    position: 'bottom-right'
};

export interface AddToastPayload {
    type?: Toast['type'];
    title?: string;
    message: string;
    description?: string;
    duration?: number;
    // Note: action is intentionally omitted from Redux payload to avoid serialization issues
    // Actions are handled directly in the useToast hook with Sonner
    dismissible?: boolean;
}

export interface UpdateToastPayload {
    id: string;
    updates: Partial<Omit<Toast, 'id' | 'createdAt'>>;
}

const toastSlice = createSlice({
    name: 'toast',
    initialState,
    reducers: {
        addToast: (state, action: PayloadAction<AddToastPayload>) => {
            const toast: Toast = {
                id: `toast_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
                type: action.payload.type || 'default',
                title: action.payload.title,
                message: action.payload.message,
                description: action.payload.description,
                duration: action.payload.duration ?? state.defaultDuration,
                // action is not stored in Redux state to avoid serialization issues
                dismissible: action.payload.dismissible ?? true,
                position: state.position,
                createdAt: Date.now()
            };

            // Add new toast to the beginning
            state.toasts.unshift(toast);

            // Keep only the maximum number of toasts
            if (state.toasts.length > state.maxToasts) {
                state.toasts = state.toasts.slice(0, state.maxToasts);
            }
        },

        removeToast: (state, action: PayloadAction<string>) => {
            state.toasts = state.toasts.filter(toast => toast.id !== action.payload);
        },

        updateToast: (state, action: PayloadAction<UpdateToastPayload>) => {
            const toastIndex = state.toasts.findIndex(toast => toast.id === action.payload.id);
            if (toastIndex !== -1) {
                state.toasts[toastIndex] = {
                    ...state.toasts[toastIndex],
                    ...action.payload.updates
                };
            }
        },

        clearAllToasts: (state) => {
            state.toasts = [];
        },

        setToastPosition: (state, action: PayloadAction<Toast['position']>) => {
            state.position = action.payload;
        },

        setMaxToasts: (state, action: PayloadAction<number>) => {
            state.maxToasts = Math.max(1, Math.min(10, action.payload));
            // Trim toasts if new max is smaller
            if (state.toasts.length > state.maxToasts) {
                state.toasts = state.toasts.slice(0, state.maxToasts);
            }
        },

        setDefaultDuration: (state, action: PayloadAction<number>) => {
            state.defaultDuration = Math.max(1000, action.payload);
        },

        // Clean up expired toasts (can be called periodically)
        cleanupExpiredToasts: (state) => {
            const now = Date.now();
            state.toasts = state.toasts.filter(toast => {
                // Keep loading toasts and toasts with duration 0 (persistent)
                if (toast.type === 'loading' || toast.duration === 0) {
                    return true;
                }
                return (now - toast.createdAt) < (toast.duration || state.defaultDuration);
            });
        }
    }
});

export const {
    addToast,
    removeToast,
    updateToast,
    clearAllToasts,
    setToastPosition,
    setMaxToasts,
    setDefaultDuration,
    cleanupExpiredToasts
} = toastSlice.actions;

// Thunk actions for common toast types
export const showSuccessToast = (message: string, options?: Partial<AddToastPayload>) =>
    addToast({ ...options, type: 'success', message });

export const showErrorToast = (message: string, options?: Partial<AddToastPayload>) =>
    addToast({ ...options, type: 'error', message });

export const showWarningToast = (message: string, options?: Partial<AddToastPayload>) =>
    addToast({ ...options, type: 'warning', message });

export const showInfoToast = (message: string, options?: Partial<AddToastPayload>) =>
    addToast({ ...options, type: 'info', message });

export const showLoadingToast = (message: string, options?: Partial<AddToastPayload>) =>
    addToast({ ...options, type: 'loading', message, duration: 0 });

export { toastSlice };
export default toastSlice.reducer;
