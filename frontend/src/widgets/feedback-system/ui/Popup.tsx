'use client';

import { ReactNode } from 'react';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogFooter,
    DialogTitle,
    DialogDescription,
} from '@/shared/ui/dialog';
import { Button } from '@/shared/ui/button';
import { cn } from '@/shared/lib/utils';

export interface PopupProps {
    // Core popup state
    isOpen: boolean;
    onClose: () => void;

    // Content
    children?: ReactNode;
    title?: string;
    description?: string;

    // Layout options
    size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
    centered?: boolean;

    // Background
    overlay?: 'light' | 'dark' | 'transparent';

    // Close options
    showCloseButton?: boolean;
    closeOnOverlayClick?: boolean;
    closeOnEscape?: boolean;

    // Footer actions
    actions?: ReactNode;

    // Custom styling
    className?: string;
    contentClassName?: string;
}

const sizeClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    full: 'max-w-[95vw] max-h-[95vh]'
};



export default function Popup({
    isOpen,
    onClose,
    children,
    title,
    description,
    size = 'md',
    overlay = 'dark',
    showCloseButton = true,
    closeOnOverlayClick = true,
    closeOnEscape = true,
    actions,
    className,
    contentClassName
}: PopupProps) {

    const handleOpenChange = (open: boolean) => {
        if (!open) {
            onClose();
        }
    };

    const handleOverlayClick = (e: React.MouseEvent) => {
        if (closeOnOverlayClick && e.target === e.currentTarget) {
            onClose();
        }
    };

    return (
        <Dialog
            open={isOpen}
            onOpenChange={handleOpenChange}
            modal={true}
        >
            <DialogContent
                className={cn(
                    sizeClasses[size],
                    !showCloseButton && '[&>button]:hidden',
                    contentClassName
                )}
                onPointerDownOutside={closeOnOverlayClick ? undefined : (e) => e.preventDefault()}
                onEscapeKeyDown={closeOnEscape ? undefined : (e) => e.preventDefault()}
            >
                {/* Custom overlay for transparent background */}
                {overlay === 'transparent' && (
                    <div
                        className="fixed inset-0 z-40 bg-transparent"
                        onClick={handleOverlayClick}
                    />
                )}

                <div className={cn('relative z-50', className)}>
                    {/* Header */}
                    {(title || description) && (
                        <DialogHeader>
                            {title && <DialogTitle>{title}</DialogTitle>}
                            {description && <DialogDescription>{description}</DialogDescription>}
                        </DialogHeader>
                    )}

                    {/* Content */}
                    {children && (
                        <div className={cn(
                            'py-4',
                            !title && !description && 'pt-0',
                            !actions && 'pb-0'
                        )}>
                            {children}
                        </div>
                    )}

                    {/* Footer */}
                    {actions && (
                        <DialogFooter>
                            {actions}
                        </DialogFooter>
                    )}
                </div>
            </DialogContent>
        </Dialog>
    );
}

// Convenience components for common popup types
export function AlertPopup({
    title,
    message,
    confirmText = 'OK',
    onConfirm,
    ...props
}: Omit<PopupProps, 'children' | 'actions'> & {
    message: string;
    confirmText?: string;
    onConfirm: () => void;
}) {
    return (
        <Popup
            {...props}
            title={title}
            actions={
                <Button onClick={onConfirm} className="w-full sm:w-auto">
                    {confirmText}
                </Button>
            }
        >
            <p className="text-sm text-muted-foreground">{message}</p>
        </Popup>
    );
}

export function ConfirmPopup({
    title,
    message,
    confirmText = 'Confirm',
    cancelText = 'Cancel',
    variant = 'default',
    onConfirm,
    onCancel,
    ...props
}: Omit<PopupProps, 'children' | 'actions'> & {
    message: string;
    confirmText?: string;
    cancelText?: string;
    variant?: 'default' | 'destructive';
    onConfirm: () => void;
    onCancel: () => void;
}) {
    return (
        <Popup
            {...props}
            title={title}
            actions={
                <div className="flex flex-col-reverse sm:flex-row gap-2 w-full sm:w-auto">
                    <Button variant="outline" onClick={onCancel} className="flex-1 sm:flex-none">
                        {cancelText}
                    </Button>
                    <Button
                        variant={variant === 'destructive' ? 'destructive' : 'default'}
                        onClick={onConfirm}
                        className="flex-1 sm:flex-none"
                    >
                        {confirmText}
                    </Button>
                </div>
            }
        >
            <p className="text-sm text-muted-foreground">{message}</p>
        </Popup>
    );
}
