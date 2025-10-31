'use client';

import { toast } from 'sonner';
import { ApiError } from './client';

interface GlobalApiErrorHandlerOptions {
  enableToasts?: boolean;
  suppressDefaultToasts?: boolean;
  customErrorHandler?: (error: unknown) => void;
}

let globalOptions: GlobalApiErrorHandlerOptions = {
  enableToasts: true,
  suppressDefaultToasts: false
};

/**
 * Configure global API error handling behavior
 */
export function configureGlobalApiErrorHandler(options: GlobalApiErrorHandlerOptions) {
  globalOptions = { ...globalOptions, ...options };
}

/**
 * Get current global error handling configuration
 */
export function getGlobalApiErrorConfig(): GlobalApiErrorHandlerOptions {
  return { ...globalOptions };
}

/**
 * Handle API errors globally with toast notifications
 * This function should be called from the main API client
 */
export function handleGlobalApiError(error: unknown, endpoint?: string): never {
  // Custom error handler takes precedence
  if (globalOptions.customErrorHandler) {
    globalOptions.customErrorHandler(error);
  }

  // Show toast notification if enabled and not suppressed
  if (globalOptions.enableToasts && !globalOptions.suppressDefaultToasts && typeof window !== 'undefined') {
    const errorMessage = getErrorMessage(error, endpoint);
    toast.error(errorMessage, {
      duration: 5000,
      dismissible: true
    });
  }

  // Re-throw the error so components can still handle it if needed
  throw error;
}

/**
 * Extract a user-friendly error message from various error types
 */
function getErrorMessage(error: unknown, endpoint?: string): string {
  if (error instanceof ApiError) {
    // Handle specific HTTP status codes
    switch (error.status) {
      case 0:
        return 'Network error - please check your internet connection';
      case 401:
        return 'Authentication required - please log in';
      case 403:
        return 'Access denied - insufficient permissions';
      case 404:
        return 'Resource not found';
      case 408:
        return 'Request timeout - please try again';
      case 500:
        return 'Server error - please try again later';
      case 502:
        return 'Service temporarily unavailable - please try again';
      case 503:
        return 'Service unavailable - please try again later';
      default:
        return error.message || 'An error occurred';
    }
  }

  if (error instanceof Error) {
    // Handle specific error messages
    if (error.message === 'Failed to fetch') {
      return 'Network error - please check your internet connection';
    }
    return error.message;
  }

  // Fallback error message
  const endpointInfo = endpoint ? ` (${endpoint})` : '';
  return `An unexpected error occurred${endpointInfo}`;
}

/**
 * Temporarily suppress toast notifications for specific operations
 */
export function withSuppressedToasts<T>(operation: () => Promise<T>): Promise<T> {
  const originalSuppressed = globalOptions.suppressDefaultToasts;
  globalOptions.suppressDefaultToasts = true;

  return operation().finally(() => {
    globalOptions.suppressDefaultToasts = originalSuppressed;
  });
}

/**
 * Enable toast notifications globally (default is enabled)
 */
export function enableGlobalToasts() {
  globalOptions.enableToasts = true;
}

/**
 * Disable toast notifications globally
 */
export function disableGlobalToasts() {
  globalOptions.enableToasts = false;
}