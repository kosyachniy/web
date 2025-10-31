'use client';

import { useCallback, useMemo } from 'react';
import { api, ApiError } from '@/shared/services/api/client';
import { useToast } from './useToast';

export interface ApiCallOptions {
  showSuccessToast?: boolean;
  showErrorToast?: boolean;
  successMessage?: string;
  errorMessage?: string;
  suppressDefaultErrors?: boolean;
}

/**
 * Hook that provides an API client with automatic toast notifications
 * Usage: const apiClient = useApiWithToast();
 */
export function useApiWithToast() {
  const { success, error } = useToast();

  const getErrorMessage = useCallback((err: unknown, customMessage?: string): string => {
    if (customMessage) return customMessage;

    if (err instanceof ApiError) {
      return err.message;
    }

    if (err instanceof Error) {
      return err.message;
    }

    return 'An unexpected error occurred';
  }, []);

  const handleRequest = useCallback(async <T>(
    requestFn: () => Promise<T>,
    options: ApiCallOptions = {}
  ): Promise<T> => {
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
        success(successMessage);
      }

      return result;
    } catch (err) {
      if (showErrorToast && !suppressDefaultErrors) {
        const message = getErrorMessage(err, errorMessage);
        error(message);
      }

      throw err; // Re-throw so components can still handle errors if needed
    }
  }, [success, error, getErrorMessage]);

  const get = useCallback(<T = unknown>(
    endpoint: string,
    params?: Record<string, unknown>,
    options?: ApiCallOptions
  ): Promise<T> => {
    return handleRequest(
      () => api.get<T>(endpoint, params),
      options
    );
  }, [handleRequest]);

  const post = useCallback(<T = unknown>(
    endpoint: string,
    body?: unknown,
    options?: ApiCallOptions
  ): Promise<T> => {
    return handleRequest(
      () => api.post<T>(endpoint, body),
      options
    );
  }, [handleRequest]);

  const put = useCallback(<T = unknown>(
    endpoint: string,
    body?: unknown,
    options?: ApiCallOptions
  ): Promise<T> => {
    return handleRequest(
      () => api.put<T>(endpoint, body),
      options
    );
  }, [handleRequest]);

  const patch = useCallback(<T = unknown>(
    endpoint: string,
    body?: unknown,
    options?: ApiCallOptions
  ): Promise<T> => {
    return handleRequest(
      () => api.patch<T>(endpoint, body),
      options
    );
  }, [handleRequest]);

  const del = useCallback(<T = unknown>(
    endpoint: string,
    options?: ApiCallOptions
  ): Promise<T> => {
    return handleRequest(
      () => api.delete<T>(endpoint),
      options
    );
  }, [handleRequest]);

  // Wrapper for existing API functions
  const wrap = useCallback(<TArgs extends unknown[], TReturn>(
    apiFunction: (...args: TArgs) => Promise<TReturn>,
    options?: ApiCallOptions
  ) => {
    return (...args: TArgs): Promise<TReturn> => {
      return handleRequest(
        () => apiFunction(...args),
        options
      );
    };
  }, [handleRequest]);

  return useMemo(() => ({
    get,
    post,
    put,
    patch,
    delete: del,
    wrap,
    // Direct access to the request handler for custom use
    handleRequest
  }), [get, post, put, patch, del, wrap, handleRequest]);
}

// Convenience hook for specific operations
export function useApiActions() {
  const apiClient = useApiWithToast();

  return useMemo(() => ({
    ...apiClient,
    // Pre-configured common actions
    create: <T>(endpoint: string, data: unknown) =>
      apiClient.post<T>(endpoint, data, {
        showSuccessToast: true,
        successMessage: 'Created successfully!',
        errorMessage: 'Failed to create'
      }),

    update: <T>(endpoint: string, data: unknown) =>
      apiClient.put<T>(endpoint, data, {
        showSuccessToast: true,
        successMessage: 'Updated successfully!',
        errorMessage: 'Failed to update'
      }),

    remove: (endpoint: string) =>
      apiClient.delete(endpoint, {
        showSuccessToast: true,
        successMessage: 'Deleted successfully!',
        errorMessage: 'Failed to delete'
      }),

    load: <T>(endpoint: string, params?: Record<string, unknown>) =>
      apiClient.get<T>(endpoint, params, {
        errorMessage: 'Failed to load data'
      })
  }), [apiClient]);
}