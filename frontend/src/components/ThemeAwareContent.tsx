'use client';

import { useTheme } from '@/components/ThemeProvider';
import LoadingScreen from '@/components/LoadingScreen';
import Header from '@/components/Header';

interface ThemeAwareContentProps {
    children: React.ReactNode;
}

export default function ThemeAwareContent({ children }: ThemeAwareContentProps) {
    const { isInitialized } = useTheme();

    return (
        <LoadingScreen isLoading={!isInitialized}>
            <Header />
            <main className="min-h-screen">
                {children}
            </main>
        </LoadingScreen>
    );
}
