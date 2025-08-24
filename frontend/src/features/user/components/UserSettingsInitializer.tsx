'use client';

import { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '@/shared/stores/store';
import { loadSettings, setLanguage } from '../stores/userSettingsSlice';
import { useLocale } from 'next-intl';
import type { Locale } from '@/i18n/routing';

export default function UserSettingsInitializer() {
    const dispatch = useAppDispatch();
    const currentLocale = useLocale() as Locale;
    const userLanguage = useAppSelector((state) => state.userSettings.language);
    const userTheme = useAppSelector((state) => state.userSettings.theme);

    useEffect(() => {
        // Load user settings from localStorage on app initialization
        dispatch(loadSettings());
    }, [dispatch]);

    useEffect(() => {
        // Sync current URL locale with Redux store
        // This handles cases where user navigates directly to a locale URL
        if (currentLocale !== userLanguage) {
            dispatch(setLanguage(currentLocale));
        }
    }, [currentLocale, userLanguage, dispatch]);

    useEffect(() => {
        // Auto-detect system theme if not set or if set to system
        if (userTheme === 'system' && typeof window !== 'undefined') {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

            // Initial check
            const handleSystemThemeChange = () => {
                // Theme provider will handle the actual theme application
                // We just need to trigger a re-render if theme is 'system'
            };

            mediaQuery.addEventListener('change', handleSystemThemeChange);
            return () => mediaQuery.removeEventListener('change', handleSystemThemeChange);
        }
    }, [userTheme]);

    // This component doesn't render anything visible
    return null;
}
