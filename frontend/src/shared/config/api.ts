/**
 * API configuration and feature flags
 */

// Environment-based configuration
export const API_CONFIG = {
  // Base URL for API requests
  baseUrl: process.env.NEXT_PUBLIC_API || 'http://api:5000/',
  
  // Timeout for API requests (in milliseconds)
  timeout: parseInt(process.env.NEXT_PUBLIC_API_TIMEOUT || '10000', 10),
  
  // Whether to use mock data as fallback when API fails
  useMockFallback: process.env.NEXT_PUBLIC_USE_MOCK_FALLBACK === 'true',
  
  // Whether to show API warnings in console
  showApiWarnings: process.env.NODE_ENV === 'development',
  
  // Mock data configuration
  mock: {
    // Number of mock posts to generate
    postsCount: 3,
    
    // Number of mock categories to generate
    categoriesCount: 3,
    
    // Delay for mock API responses (in milliseconds)
    delay: parseInt(process.env.NEXT_PUBLIC_MOCK_API_DELAY || '0', 10)
  }
} as const;

/**
 * Check if mock fallback should be used
 */
export function shouldUseMockFallback(): boolean {
  return API_CONFIG.useMockFallback;
}

/**
 * Log API warnings if enabled
 */
export function logApiWarning(message: string, error?: unknown): void {
  if (API_CONFIG.showApiWarnings) {
    console.warn(`[API] ${message}`, error);
  }
}

/**
 * Add artificial delay for mock responses (useful for testing loading states)
 */
export async function addMockDelay(): Promise<void> {
  if (API_CONFIG.mock.delay > 0) {
    await new Promise(resolve => setTimeout(resolve, API_CONFIG.mock.delay));
  }
}