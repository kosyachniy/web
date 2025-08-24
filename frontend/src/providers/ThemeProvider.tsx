'use client';

import { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { useAppDispatch, useAppSelector } from '@/shared/stores/store';
import { setTheme } from '@/features/user/stores/userSettingsSlice';

type Theme = 'light' | 'dark' | 'system';

interface ThemeContextType {
    theme: Theme;
    resolvedTheme: 'light' | 'dark';
    setTheme: (theme: Theme) => void;
    isInitialized: boolean;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
    const dispatch = useAppDispatch();
    const userTheme = useAppSelector((state) => state.userSettings.theme);
    const isInitialized = useAppSelector((state) => state.userSettings.isInitialized);
    const [resolvedTheme, setResolvedTheme] = useState<'light' | 'dark'>('light');

    // Function to get system preference
    const getSystemTheme = (): 'light' | 'dark' => {
        if (typeof window !== 'undefined') {
            return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        }
        return 'light';
    };

    // Function to resolve theme (system -> actual light/dark)
    const resolveTheme = useCallback((theme: Theme): 'light' | 'dark' => {
        if (theme === 'system') {
            return getSystemTheme();
        }
        return theme;
    }, []);

    // Update theme handler
    const handleSetTheme = (newTheme: Theme) => {
        dispatch(setTheme(newTheme));
    };

    // Effect to apply theme to document
    useEffect(() => {
        // Only apply theme after settings are initialized to prevent flickering
        if (!isInitialized) return;

        const resolved = resolveTheme(userTheme);
        setResolvedTheme(resolved);

        // Apply theme to document
        if (typeof window !== 'undefined') {
            const root = window.document.documentElement;
            root.classList.remove('light', 'dark');
            root.classList.add(resolved);

            // Also set data attribute for compatibility
            root.setAttribute('data-theme', resolved);
        }
    }, [userTheme, isInitialized, resolveTheme]);

    // Effect to listen for system theme changes
    useEffect(() => {
        if (typeof window !== 'undefined' && userTheme === 'system' && isInitialized) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

            const handleChange = () => {
                const resolved = resolveTheme(userTheme);
                setResolvedTheme(resolved);

                const root = window.document.documentElement;
                root.classList.remove('light', 'dark');
                root.classList.add(resolved);
                root.setAttribute('data-theme', resolved);
            };

            mediaQuery.addEventListener('change', handleChange);
            return () => mediaQuery.removeEventListener('change', handleChange);
        }
    }, [userTheme, isInitialized, resolveTheme]);

    return (
        <ThemeContext.Provider
            value={{
                theme: userTheme,
                resolvedTheme,
                setTheme: handleSetTheme,
                isInitialized,
            }}
        >
            {children}
        </ThemeContext.Provider>
    );
}

export const useTheme = () => {
    const context = useContext(ThemeContext);
    if (context === undefined) {
        throw new Error('useTheme must be used within a ThemeProvider');
    }
    return context;
};
