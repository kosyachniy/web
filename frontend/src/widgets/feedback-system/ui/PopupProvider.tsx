'use client';

import { createContext, useContext, useState, ReactNode, useCallback } from 'react';
import Popup, { PopupProps } from './Popup';

interface PopupContextType {
    // Basic popup control
    showPopup: (props: Omit<PopupProps, 'isOpen' | 'onClose'>) => void;
    closePopup: () => void;

    // Convenience methods
    showAlert: (options: {
        title?: string;
        message: string;
        confirmText?: string;
    }) => Promise<void>;

    showConfirm: (options: {
        title?: string;
        message: string;
        confirmText?: string;
        cancelText?: string;
        variant?: 'default' | 'destructive';
    }) => Promise<boolean>;

    // State
    isOpen: boolean;
}

const PopupContext = createContext<PopupContextType | undefined>(undefined);

interface PopupProviderProps {
    children: ReactNode;
}

export function PopupProvider({ children }: PopupProviderProps) {
    const [isOpen, setIsOpen] = useState(false);
    const [popupProps, setPopupProps] = useState<Omit<PopupProps, 'isOpen' | 'onClose'>>({});
    const [currentPromiseResolve, setCurrentPromiseResolve] = useState<((value: unknown) => void) | null>(null);

    const showPopup = useCallback((props: Omit<PopupProps, 'isOpen' | 'onClose'>) => {
        setPopupProps(props);
        setIsOpen(true);
    }, []);

    const closePopup = useCallback(() => {
        setIsOpen(false);
        // Resolve any pending promises
        if (currentPromiseResolve) {
            currentPromiseResolve(false);
            setCurrentPromiseResolve(null);
        }
    }, [currentPromiseResolve]);

    const showAlert = useCallback((options: {
        title?: string;
        message: string;
        confirmText?: string;
    }) => {
        return new Promise<void>((resolve) => {
            setCurrentPromiseResolve(() => resolve);
            showPopup({
                title: options.title,
                children: <p className="text-sm text-muted-foreground">{options.message}</p>,
                actions: (
                    <button
                        onClick={() => {
                            resolve();
                            closePopup();
                        }}
                        className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2 w-full sm:w-auto"
                    >
                        {options.confirmText || 'OK'}
                    </button>
                )
            });
        });
    }, [showPopup, closePopup]);

    const showConfirm = useCallback((options: {
        title?: string;
        message: string;
        confirmText?: string;
        cancelText?: string;
        variant?: 'default' | 'destructive';
    }) => {
        return new Promise<boolean>((resolve) => {
            setCurrentPromiseResolve(() => resolve);
            showPopup({
                title: options.title,
                children: <p className="text-sm text-muted-foreground">{options.message}</p>,
                actions: (
                    <div className="flex flex-col-reverse sm:flex-row gap-2 w-full sm:w-auto">
                        <button
                            onClick={() => {
                                resolve(false);
                                closePopup();
                            }}
                            className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2 flex-1 sm:flex-none"
                        >
                            {options.cancelText || 'Cancel'}
                        </button>
                        <button
                            onClick={() => {
                                resolve(true);
                                closePopup();
                            }}
                            className={`inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 h-10 px-4 py-2 flex-1 sm:flex-none ${options.variant === 'destructive'
                                ? 'bg-destructive text-destructive-foreground hover:bg-destructive/90'
                                : 'bg-primary text-primary-foreground hover:bg-primary/90'
                                }`}
                        >
                            {options.confirmText || 'Confirm'}
                        </button>
                    </div>
                )
            });
        });
    }, [showPopup, closePopup]);

    const contextValue: PopupContextType = {
        showPopup,
        closePopup,
        showAlert,
        showConfirm,
        isOpen
    };

    return (
        <PopupContext.Provider value={contextValue}>
            {children}
            <Popup
                {...popupProps}
                isOpen={isOpen}
                onClose={closePopup}
            />
        </PopupContext.Provider>
    );
}

export function usePopup() {
    const context = useContext(PopupContext);
    if (context === undefined) {
        throw new Error('usePopup must be used within a PopupProvider');
    }
    return context;
}

// Example usage hook for common patterns
export function usePopupActions() {
    const { showAlert, showConfirm, showPopup, closePopup } = usePopup();

    return {
        // Simple alert
        alert: showAlert,

        // Confirmation dialog
        confirm: showConfirm,

        // Custom popup
        show: showPopup,
        close: closePopup,

        // Quick success/error alerts
        success: (message: string) => showAlert({
            title: 'Success',
            message,
            confirmText: 'OK'
        }),

        error: (message: string) => showAlert({
            title: 'Error',
            message,
            confirmText: 'OK'
        }),

        // Destructive confirmation
        confirmDelete: (message: string = 'Are you sure you want to delete this item?') =>
            showConfirm({
                title: 'Delete Confirmation',
                message,
                confirmText: 'Delete',
                cancelText: 'Cancel',
                variant: 'destructive'
            })
    };
}
