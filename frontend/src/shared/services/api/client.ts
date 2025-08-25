/**
 * Common API client for making requests to the backend API
 * Provides centralized error handling, authentication, and configuration
 */

// Use different base URLs for server-side vs client-side requests
const getApiBaseUrl = () => {
    // Server-side rendering (SSR) - use internal Docker network without /api/ prefix
    // (nginx strips /api/ prefix when forwarding to backend)
    if (typeof window === 'undefined') {
        return process.env.API_BASE_URL || 'http://api:5000/';
    }
    // Client-side rendering (CSR) - use public URL through nginx proxy
    return process.env.NEXT_PUBLIC_API || 'http://localhost/api/';
};

const API_BASE_URL = getApiBaseUrl();

export class ApiError extends Error {
    constructor(
        public status: number,
        message: string,
        public data?: unknown
    ) {
        super(message);
        this.name = 'ApiError';
    }
}

export interface ApiRequestOptions extends Omit<RequestInit, 'body'> {
    body?: unknown;
    params?: Record<string, unknown>;
    timeout?: number;
}

export interface ApiResponse<T = unknown> {
    data: T;
    status: number;
    headers: Headers;
}

/**
 * Common API client function
 * @param endpoint - API endpoint (e.g., '/posts/get/')
 * @param options - Request options
 * @returns Promise with typed response data
 */
export async function apiClient<T = unknown>(
    endpoint: string,
    options: ApiRequestOptions = {}
): Promise<T> {
    const {
        body,
        params,
        timeout = 10000,
        headers = {},
        method = 'GET',
        ...restOptions
    } = options;

    // Build URL with query parameters for GET requests
    let url = `${API_BASE_URL.replace(/\/$/, '')}${endpoint}`;
    if (params && method === 'GET') {
        const searchParams = new URLSearchParams();
        Object.entries(params).forEach(([key, value]) => {
            if (value !== undefined && value !== null) {
                searchParams.append(key, String(value));
            }
        });
        if (searchParams.toString()) {
            url += `?${searchParams.toString()}`;
        }
    }

    // Prepare headers
    const defaultHeaders: HeadersInit = {
        'Content-Type': 'application/json',
    };

    // Add authentication headers if available
    if (typeof window !== 'undefined') {
        const token = localStorage.getItem('authToken');
        if (token) {
            defaultHeaders.Authorization = `Bearer ${token}`;
        }
    } else {
        // For SSR requests, don't add auth headers for public endpoints
        // This prevents 401 errors on public data fetching during SSR
    }

    // Prepare request body
    let requestBody: string | FormData | undefined;
    if (body) {
        if (body instanceof FormData) {
            requestBody = body;
            // Remove Content-Type header for FormData (browser will set it with boundary)
            delete defaultHeaders['Content-Type'];
        } else if (typeof body === 'object' && body !== null) {
            requestBody = JSON.stringify(body);
        } else if (typeof body === 'string') {
            requestBody = body;
        }
    }

    // Create abort controller for timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
        const response = await fetch(url, {
            method,
            headers: {
                ...defaultHeaders,
                ...headers,
            },
            body: requestBody,
            signal: controller.signal,
            ...restOptions,
        });

        clearTimeout(timeoutId);

        // Handle non-JSON responses
        const contentType = response.headers.get('content-type');
        let responseData: unknown;

        if (contentType?.includes('application/json')) {
            responseData = await response.json();
        } else {
            responseData = await response.text();
        }

        if (!response.ok) {
            const errorMessage = (responseData && typeof responseData === 'object' && 'message' in responseData) 
                ? String((responseData as { message: unknown }).message) 
                : `HTTP error! status: ${response.status}`;
            throw new ApiError(
                response.status,
                errorMessage,
                responseData
            );
        }

        return responseData as T;
    } catch (error) {
        clearTimeout(timeoutId);

        if (error instanceof ApiError) {
            throw error;
        }

        if (error instanceof DOMException && error.name === 'AbortError') {
            throw new ApiError(408, 'Request timeout');
        }

        if (error instanceof TypeError && error.message === 'Failed to fetch') {
            throw new ApiError(0, 'Network error - please check your internet connection');
        }

        throw new ApiError(0, error instanceof Error ? error.message : 'Unknown error occurred');
    }
}

/**
 * Convenience methods for common HTTP verbs
 */
export const api = {
    get: <T = unknown>(endpoint: string, params?: Record<string, unknown>, options?: Omit<ApiRequestOptions, 'method' | 'params'>) =>
        apiClient<T>(endpoint, { ...options, method: 'GET', params }),

    post: <T = unknown>(endpoint: string, body?: unknown, options?: Omit<ApiRequestOptions, 'method' | 'body'>) =>
        apiClient<T>(endpoint, { ...options, method: 'POST', body }),

    put: <T = unknown>(endpoint: string, body?: unknown, options?: Omit<ApiRequestOptions, 'method' | 'body'>) =>
        apiClient<T>(endpoint, { ...options, method: 'PUT', body }),

    patch: <T = unknown>(endpoint: string, body?: unknown, options?: Omit<ApiRequestOptions, 'method' | 'body'>) =>
        apiClient<T>(endpoint, { ...options, method: 'PATCH', body }),

    delete: <T = unknown>(endpoint: string, options?: Omit<ApiRequestOptions, 'method'>) =>
        apiClient<T>(endpoint, { ...options, method: 'DELETE' }),
};

/**
 * Request interceptor - runs before every request
 */
// eslint-disable-next-line @typescript-eslint/no-unused-vars
export function addRequestInterceptor(_interceptor: (options: ApiRequestOptions) => ApiRequestOptions | Promise<ApiRequestOptions>) {
    // Implementation would go here if needed
    // This is a placeholder for future enhancement
}

/**
 * Response interceptor - runs after every response
 */
// eslint-disable-next-line @typescript-eslint/no-unused-vars
export function addResponseInterceptor(_interceptor: (response: unknown) => unknown | Promise<unknown>) {
    // Implementation would go here if needed
    // This is a placeholder for future enhancement
}

export default api;