'use client';

import { useState } from 'react';
import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import { Box } from '@/shared/ui/box';
import { PageHeader } from '@/shared/ui/page-header';
import { BellIcon } from '@/shared/ui/icons';
import { useToast, useToastActions } from '@/shared/hooks/useToast';

export default function ToastDemo() {
    const [customMessage, setCustomMessage] = useState('');
    const [loadingToastId, setLoadingToastId] = useState<string | null>(null);

    const toast = useToast();
    const {
        success,
        error,
        warning,
        info,
        loading,
        promise,
        saveSuccess,
        deleteSuccess
    } = useToastActions();

    const handleBasicToasts = () => {
        toast.toast('This is a basic toast message');
    };

    const handleSuccessToast = () => {
        success('Operation completed successfully!');
    };

    const handleErrorToast = () => {
        error('Something went wrong. Please try again.');
    };

    const handleWarningToast = () => {
        warning('This action cannot be undone.');
    };

    const handleInfoToast = () => {
        info('Here is some helpful information.');
    };

    const handleLoadingToast = () => {
        const id = loading('Processing your request...');
        setLoadingToastId(id);

        // Simulate dismissing after 3 seconds
        setTimeout(() => {
            toast.dismiss(id);
            success('Process completed!');
            setLoadingToastId(null);
        }, 3000);
    };

    const handleCustomToast = () => {
        if (!customMessage.trim()) {
            error('Please enter a message first!');
            return;
        }

        toast.toast(customMessage, {
            title: 'Custom Toast',
            description: 'This toast has a custom message and description',
            duration: 6000,
            action: {
                label: 'Undo',
                onClick: () => {
                    info('Undo action clicked!');
                }
            }
        });

        setCustomMessage('');
    };

    const handlePromiseToast = async () => {
        // Simulate an API call
        const apiCall = new Promise<string>((resolve, reject) => {
            setTimeout(() => {
                if (Math.random() > 0.5) {
                    resolve('API call successful!');
                } else {
                    reject(new Error('API call failed'));
                }
            }, 2000);
        });

        try {
            await promise(apiCall, {
                loading: 'Making API call...',
                success: (data) => `Success: ${data}`,
                error: (err) => `Error: ${err instanceof Error ? err.message : String(err)}`
            });
        } catch {
            // Error is handled by the promise toast
        }
    };

    const handleMultipleToasts = () => {
        success('First toast');
        setTimeout(() => info('Second toast'), 500);
        setTimeout(() => warning('Third toast'), 1000);
        setTimeout(() => error('Fourth toast'), 1500);
        setTimeout(() => success('Fifth toast'), 2000);
    };

    const handleConvenienceToasts = () => {
        saveSuccess('User Profile');
        setTimeout(() => deleteSuccess('Old File'), 1000);
    };

    const handlePositionChange = () => {
        const positions: Array<'top-left' | 'top-center' | 'top-right' | 'bottom-left' | 'bottom-center' | 'bottom-right'> = [
            'top-left', 'top-center', 'top-right',
            'bottom-left', 'bottom-center', 'bottom-right'
        ];

        const currentIndex = positions.indexOf(toast.position || 'bottom-right');
        const nextPosition = positions[(currentIndex + 1) % positions.length];

        toast.setPosition(nextPosition);
        info(`Toast position changed to: ${nextPosition}`);
    };

    const handleDismissAll = () => {
        toast.dismissAll();
        setTimeout(() => {
            info('All previous toasts were dismissed!');
        }, 100);
    };

    return (
        <div className="max-w-2xl mx-auto">
            <PageHeader
                icon={<BellIcon size={24} />}
                iconClassName="bg-green-500/15 text-green-600 dark:bg-green-500/20 dark:text-green-400"
                title="Toast System Demo"
                description="Notification system with multiple variants and positioning"
            />

            <Box size="lg">
                <div className="space-y-6">

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <Button onClick={handleBasicToasts} variant="outline">
                            Basic Toast
                        </Button>

                        <Button onClick={handleSuccessToast} variant="outline">
                            Success Toast
                        </Button>

                        <Button onClick={handleErrorToast} variant="destructive">
                            Error Toast
                        </Button>

                        <Button onClick={handleWarningToast} variant="outline">
                            Warning Toast
                        </Button>

                        <Button onClick={handleInfoToast} variant="outline">
                            Info Toast
                        </Button>

                        <Button onClick={handleLoadingToast} variant="outline" disabled={!!loadingToastId}>
                            {loadingToastId ? 'Loading...' : 'Loading Toast'}
                        </Button>

                        <Button onClick={handlePromiseToast} variant="outline">
                            Promise Toast
                        </Button>

                        <Button onClick={handleMultipleToasts} variant="outline">
                            Multiple Toasts
                        </Button>

                        <Button onClick={handleConvenienceToasts} variant="outline">
                            Convenience Toasts
                        </Button>

                        <Button onClick={handlePositionChange} variant="outline">
                            Change Position
                        </Button>

                        <Button onClick={handleDismissAll} variant="secondary">
                            Dismiss All
                        </Button>
                    </div>

                    <Box variant="muted" size="default" className="space-y-4">
                        <div className="flex gap-2">
                            <Input
                                placeholder="Enter custom message..."
                                value={customMessage}
                                onChange={(e) => setCustomMessage(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleCustomToast()}
                            />
                            <Button onClick={handleCustomToast}>
                                Custom Toast
                            </Button>
                        </div>

                        <div className="grid grid-cols-2 gap-4 text-sm">
                            <div className="bg-background p-3 rounded-[0.75rem] border">
                                <strong>Current Position:</strong> {toast.position}
                            </div>
                            <div className="bg-background p-3 rounded-[0.75rem] border">
                                <strong>Max Toasts:</strong> {toast.maxToasts}
                            </div>
                            <div className="bg-background p-3 rounded-[0.75rem] border">
                                <strong>Default Duration:</strong> {toast.defaultDuration}ms
                            </div>
                            <div className="bg-background p-3 rounded-[0.75rem] border">
                                <strong>Active Toasts:</strong> {toast.toasts.length}
                            </div>
                        </div>
                    </Box>
                </div>
            </Box>
        </div>
    );
}
