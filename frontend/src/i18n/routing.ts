import { defineRouting } from 'next-intl/routing';
import { createNavigation } from 'next-intl/navigation';

export type Locale = 'en' | 'ru' | 'zh' | 'es' | 'ar';

export const routing = defineRouting({
    // A list of all locales that are supported
    locales: ['en', 'ru', 'zh', 'es', 'ar'] as const,

    // Used when no locale matches
    defaultLocale: 'en',

    // The `pathnames` object maps the internal pathnames
    pathnames: {
        '/': '/',
        '/posts': '/posts',
        '/space': '/space', 
        '/hub': '/hub',
        '/catalog': '/catalog',
        '/admin': '/admin',
        '/admin/categories': '/admin/categories',
        '/admin/posts': '/admin/posts',
        '/admin/users': '/admin/users'
        // You can add more custom pathnames here if needed
    },

    // Enable locale detection from various sources
    localeDetection: true
});

// Lightweight wrappers around Next.js' navigation APIs
// that will consider the routing configuration
export const { Link, redirect, usePathname, useRouter } =
    createNavigation(routing);
