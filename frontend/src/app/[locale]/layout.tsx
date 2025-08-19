import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "../globals.css";
import { ReduxProvider } from "@/lib/redux/provider";
import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';
import { notFound } from 'next/navigation';
import { routing, type Locale } from '@/i18n/routing';
import UserSettingsInitializer from '@/components/UserSettingsInitializer';
import { ThemeProvider } from '@/components/ThemeProvider';
import Header from '@/components/Header';

const geistSans = Geist({
    variable: "--font-geist-sans",
    subsets: ["latin"],
});

const geistMono = Geist_Mono({
    variable: "--font-geist-mono",
    subsets: ["latin"],
});

export const metadata: Metadata = {
    title: "Frontend Stack Demo",
    description: "Next.js 15 + React 19 + shadcn/ui + Redux Toolkit",
};

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
            <body
                className={`${geistSans.variable} ${geistMono.variable} antialiased`}
            >
                <NextIntlClientProvider messages={messages}>
                    <ReduxProvider>
                        <ThemeProvider>
                            <UserSettingsInitializer />
                            <Header />
                            <main className="min-h-screen pt-16">
                                {children}
                            </main>
                        </ThemeProvider>
                    </ReduxProvider>
                </NextIntlClientProvider>
            </body>
        </html>
    );
}
