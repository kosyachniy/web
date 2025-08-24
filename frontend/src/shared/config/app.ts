// Application configuration
export const APP_CONFIG = {
  name: 'Web App',
  version: '1.0.0',
  description: 'Modern web application',
  author: 'Alex Poloz',
  
  // API Configuration
  api: {
    baseUrl: process.env.NEXT_PUBLIC_API || 'http://api:5000/',
    timeout: 10000,
    retries: 3,
  },
  
  // Feature flags
  features: {
    analytics: process.env.NODE_ENV === 'production',
    darkMode: true,
    i18n: true,
    telemetry: process.env.NODE_ENV === 'production',
  },
  
  // UI Configuration
  ui: {
    defaultTheme: 'system' as const,
    toastPosition: 'bottom-right' as const,
    maxToasts: 5,
    defaultToastDuration: 4000,
  },
  
  // Pagination
  pagination: {
    defaultLimit: 12,
    maxLimit: 100,
  },
} as const;

export type AppConfig = typeof APP_CONFIG;