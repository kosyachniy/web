import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "../globals.css";
import "../../styles/sonner.css";
import "@fortawesome/fontawesome-free/css/all.css";
import { ReduxProvider } from "@/providers";
import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';
import { notFound } from 'next/navigation';
import { routing, type Locale } from '@/i18n/routing';
import { UserSettingsInitializer } from '@/features/user';
import { ThemeProvider } from '@/providers';
import { PopupProvider } from '@/widgets/feedback-system';
import { ToastProvider } from '@/widgets/feedback-system';
import { StructuredData } from '@/shared/components/layout';
import { ThemeAwareContent } from '@/shared/components/layout';

const geistSans = Geist({
    variable: "--font-geist-sans",
    subsets: ["latin"],
});

const geistMono = Geist_Mono({
    variable: "--font-geist-mono",
    subsets: ["latin"],
});

export const metadata: Metadata = {
    title: {
        default: "web",
        template: "%s | web"
    },
    description: "Template web app",
    keywords: ["web development"],
    authors: [{ name: "Alex Poloz <alexypoloz@gmail.com>" }],
    creator: "Alex Poloz <alexypoloz@gmail.com>",
    publisher: "Alex Poloz <alexypoloz@gmail.com>",
    formatDetection: {
        email: false,
        address: false,
        telephone: false,
    },
    metadataBase: new URL(process.env.NEXT_PUBLIC_WEB || 'http://localhost:3000'),
    alternates: {
        canonical: '/',
        languages: {
            'en': '/en',
            'ru': '/ru',
            'zh': '/zh',
            'es': '/es',
            'ar': '/ar',
        },
    },
    openGraph: {
        title: "web",
        description: "Template web app",
        url: '/',
        siteName: 'web',
        images: [
            {
                url: '/logo.svg',
                width: 1200,
                height: 630,
                alt: 'web Logo',
            },
        ],
        locale: 'en_US',
        type: 'website',
    },
    twitter: {
        card: 'summary_large_image',
        title: "web",
        description: "Template web app",
        images: ['/logo.svg'],
    },
    robots: {
        index: true,
        follow: true,
        googleBot: {
            index: true,
            follow: true,
            'max-video-preview': -1,
            'max-image-preview': 'large',
            'max-snippet': -1,
        },
    },
    manifest: '/manifest.json',
    icons: {
        icon: '/icon.svg',
        shortcut: '/icon.svg',
        apple: '/logo.svg',
    },
};

export const viewport = {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 1,
};

export function generateStaticParams() {
    return routing.locales.map((locale) => ({ locale }));
}

export default async function LocaleLayout({
    children,
    params,
}: {
    children: React.ReactNode;
    params: Promise<{ locale: string }>;
}) {
    const { locale } = await params;

    // Ensure that the incoming `locale` is valid
    if (!routing.locales.includes(locale as Locale)) {
        notFound();
    }

    // Providing all messages to the client
    // side is the easiest way to get started
    const messages = await getMessages();

    return (
        <html lang={locale} dir={locale === 'ar' ? 'rtl' : 'ltr'}>
            <head>
                <StructuredData />
                <link rel="manifest" href="/manifest.json" />
                <meta name="theme-color" content="#708E6C" />
                <meta name="apple-mobile-web-app-capable" content="yes" />
                <meta name="apple-mobile-web-app-status-bar-style" content="default" />
                <meta name="apple-mobile-web-app-title" content="Web" />
                <link rel="icon" type="image/svg+xml" href="/icon.svg" />
                <link rel="apple-touch-icon" href="/logo.svg" />
            </head>
            <body
                className={`${geistSans.variable} ${geistMono.variable} antialiased`}
            >
                <NextIntlClientProvider messages={messages}>
                    <ReduxProvider>
                        <ThemeProvider>
                            <PopupProvider>
                                <ToastProvider />
                                <UserSettingsInitializer />
                                <ThemeAwareContent>
                                    {children}
                                </ThemeAwareContent>
                            </PopupProvider>
                        </ThemeProvider>
                    </ReduxProvider>
                </NextIntlClientProvider>
            </body>
        </html>
    );
}
