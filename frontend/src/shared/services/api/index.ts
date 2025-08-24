/**
 * API module exports
 * Centralized exports for all API functions
 */

// Export the main API client
export { api, apiClient, ApiError } from './client';
export type { ApiRequestOptions, ApiResponse } from './client';

// Export authentication functions
export * from './auth';

// Common API utilities
export const API_BASE_URL = process.env.NEXT_PUBLIC_API || 'http://api:5000/';

/**
 * Health check endpoint
 */
export async function healthCheck(): Promise<{ status: string; timestamp: string }> {
    const { api } = await import('./client');
    return api.get('/health/');
}