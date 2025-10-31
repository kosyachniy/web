'use client';

import React, { Component, ReactNode } from 'react';
import { AlertIcon } from '@/shared/ui/icons';
import { Button } from '@/shared/ui/button';
import { Box } from '@/shared/ui/box';

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: React.ErrorInfo) => void;
  showToast?: boolean;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);

    // Call the optional error callback
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }

    // Show toast notification on client side
    if (this.props.showToast !== false && typeof window !== 'undefined') {
      // Dynamic import to avoid SSR issues
      import('@/shared/hooks/useToast').then(({ useToast }) => {
        // Note: We can't use hooks in class components, so we need to handle this differently
        // For now, we'll use the sonner toast directly
        import('sonner').then(({ toast }) => {
          toast.error('Something went wrong', {
            description: error.message || 'An unexpected error occurred',
            duration: 5000,
          });
        });
      });
    }
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: undefined });
  };

  render() {
    if (this.state.hasError) {
      // Custom fallback UI
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // Default error UI
      return (
        <Box variant="muted" size="lg" className="text-center">
          <div className="flex flex-col items-center gap-4">
            <div className="bg-red-500/15 text-red-600 dark:bg-red-500/20 dark:text-red-400 w-12 h-12 rounded-[0.75rem] flex items-center justify-center">
              <AlertIcon size={24} />
            </div>

            <div>
              <h3 className="text-lg font-semibold text-foreground mb-2">
                Something went wrong
              </h3>
              <p className="text-muted-foreground mb-4">
                {this.state.error?.message || 'An unexpected error occurred'}
              </p>
            </div>

            <Button
              variant="outline"
              onClick={this.handleRetry}
              className="cursor-pointer"
            >
              Try Again
            </Button>
          </div>
        </Box>
      );
    }

    return this.props.children;
  }
}

// Hook-based wrapper for functional components that need error boundary with toast
interface ErrorBoundaryWrapperProps {
  children: ReactNode;
  fallback?: ReactNode;
}

export function ErrorBoundaryWithToast({ children, fallback }: ErrorBoundaryWrapperProps) {
  const handleError = (error: Error, errorInfo: React.ErrorInfo) => {
    console.error('Error caught by boundary:', error, errorInfo);
  };

  return (
    <ErrorBoundary
      onError={handleError}
      showToast={true}
      fallback={fallback}
    >
      {children}
    </ErrorBoundary>
  );
}

// Utility function to wrap components with error boundary
export function withErrorBoundary<P extends object>(
  Component: React.ComponentType<P>,
  errorBoundaryProps?: Partial<ErrorBoundaryProps>
) {
  const WrappedComponent = (props: P) => (
    <ErrorBoundary {...errorBoundaryProps}>
      <Component {...props} />
    </ErrorBoundary>
  );

  WrappedComponent.displayName = `withErrorBoundary(${Component.displayName || Component.name})`;

  return WrappedComponent;
}