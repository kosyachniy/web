'use client';

import { api, ApiError } from './client';
import { toast } from 'sonner';

export interface ApiCallOptions {
  showSuccessToast?: boolean;
  showErrorToast?: boolean;
  successMessage?: string;
  errorMessage?: string;
  suppressDefaultErrors?: boolean;
}

/**
 * Enhanced API wrapper that automatically shows toast notifications
 * for errors and optionally for success messages
 */
class ApiWithToast {
  private getErrorMessage(error: unknown, customMessage?: string): string {
    if (customMessage) return customMessage;

    if (error instanceof ApiError) {
      return error.message;
    }

    if (error instanceof Error) {
      return error.message;
    }

    return 'An unexpected error occurred';
  }

  private async handleRequest<T>(
    requestFn: () => Promise<T>,
    options: ApiCallOptions = {}
  ): Promise<T> {
    const {
      showSuccessToast = false,
      showErrorToast = true,
      successMessage,
      errorMessage,
      suppressDefaultErrors = false
    } = options;

    try {
      const result = await requestFn();

      if (showSuccessToast && successMessage) {
        toast.success(successMessage);
      }

      return result;
    } catch (error) {
      if (showErrorToast && !suppressDefaultErrors) {
        const message = this.getErrorMessage(error, errorMessage);
        toast.error(message);
      }

      throw error; // Re-throw so components can still handle errors if needed
    }
  }

  async get<T = unknown>(
    endpoint: string,
    params?: Record<string, unknown>,
    options?: ApiCallOptions
  ): Promise<T> {
    return this.handleRequest(
      () => api.get<T>(endpoint, params),
      options
    );
  }

  async post<T = unknown>(
    endpoint: string,
    body?: unknown,
    options?: ApiCallOptions
  ): Promise<T> {
    return this.handleRequest(
      () => api.post<T>(endpoint, body),
      options
    );
  }

  async put<T = unknown>(
    endpoint: string,
    body?: unknown,
    options?: ApiCallOptions
  ): Promise<T> {
    return this.handleRequest(
      () => api.put<T>(endpoint, body),
      options
    );
  }

  async patch<T = unknown>(
    endpoint: string,
    body?: unknown,
    options?: ApiCallOptions
  ): Promise<T> {
    return this.handleRequest(
      () => api.patch<T>(endpoint, body),
      options
    );
  }

  async delete<T = unknown>(
    endpoint: string,
    options?: ApiCallOptions
  ): Promise<T> {
    return this.handleRequest(
      () => api.delete<T>(endpoint),
      options
    );
  }
}

// Export singleton instance
export const apiWithToast = new ApiWithToast();

// Convenience function for one-off requests with custom options
export function createApiCall<T>(
  requestFn: () => Promise<T>,
  options?: ApiCallOptions
): Promise<T> {
  const apiInstance = new ApiWithToast();
  return apiInstance['handleRequest'](requestFn, options);
}

// Convenience wrapper for existing API calls
export function withAutoToast<TArgs extends unknown[], TReturn>(
  apiFunction: (...args: TArgs) => Promise<TReturn>,
  defaultOptions?: ApiCallOptions
) {
  return async (...args: TArgs): Promise<TReturn> => {
    const apiInstance = new ApiWithToast();
    return apiInstance['handleRequest'](
      () => apiFunction(...args),
      defaultOptions
    );
  };
}