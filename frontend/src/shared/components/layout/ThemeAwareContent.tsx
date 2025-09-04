'use client';

import { useTheme } from '@/providers/ThemeProvider';
import LoadingScreen from './LoadingScreen';
import { Header } from '@/widgets/header';
import { Footer } from '@/widgets/footer';

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
            <Footer />
        </LoadingScreen>
    );
}
