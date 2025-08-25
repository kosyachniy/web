import createMiddleware from 'next-intl/middleware';
import { routing } from './i18n/routing';

export default createMiddleware({
    ...routing,

    // Enhanced locale detection
    localeDetection: true,

    // Optional: Alternative locales (e.g., 'en-US' -> 'en')
    alternateLinks: false,
});

export const config = {
    // Match only internationalized pathnames
    matcher: [
        // Enable a redirect to a matching locale at the root
        '/',

        // Set a cookie to remember the previous locale for
        // all requests that have a locale prefix
        '/(en|ru|zh|es|ar)/:path*',

        // Match all paths that should be internationalized
        // This will redirect /posts/articles to /en/posts/articles
        '/((?!api|_next|_vercel|.*\\.).*)'
    ]
};
