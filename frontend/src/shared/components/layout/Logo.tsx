'use client';

import { useTheme } from '@/providers/ThemeProvider';
import { useTranslations } from 'next-intl';
import Image from 'next/image';

interface LogoProps {
    className?: string;
    width?: number;
    height?: number;
    showText?: boolean;
}

export default function Logo({
    className = '',
    width = 120,
    height = 48,
    showText = false
}: LogoProps) {
    const { resolvedTheme } = useTheme();
    const t = useTranslations();

    // Use light logo for dark theme, dark logo for light theme
    const logoSrc = resolvedTheme === 'dark' ? '/logo-light.svg' : '/logo.svg';

    return (
        <div className={`flex items-center space-x-2 ${className}`}>
            <Image
                src={logoSrc}
                alt={t('brand.name')}
                width={width}
                height={height}
                className="h-8 w-auto"
                priority
            />
            {showText && (
                <span className="hidden sm:inline-block font-bold text-lg">
                    {t('brand.name')}
                </span>
            )}
        </div>
    );
}
