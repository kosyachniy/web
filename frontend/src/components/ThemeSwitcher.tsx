'use client';

import { useTheme } from './ThemeProvider';
import { Button } from '@/components/ui/button';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useTranslations } from 'next-intl';

const themes = [
    {
        value: 'system' as const,
        icon: '💻',
        labelKey: 'system'
    },
    {
        value: 'light' as const,
        icon: '☀️',
        labelKey: 'light'
    },
    {
        value: 'dark' as const,
        icon: '🌙',
        labelKey: 'dark'
    },
] as const;

export default function ThemeSwitcher() {
    const { theme, resolvedTheme, setTheme } = useTheme();
    const t = useTranslations('theme');

    const currentTheme = themes.find(t => t.value === theme);

    // Get the right icon to display in the button
    const getDisplayIcon = () => {
        if (theme === 'system') {
            return resolvedTheme === 'dark' ? '🌙' : '☀️';
        }
        return currentTheme?.icon || '☀️';
    };

    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="outline" size="sm" className="flex items-center gap-2">
                    <span className="text-lg">{getDisplayIcon()}</span>
                    <span className="hidden sm:inline capitalize">
                        {theme === 'system' ? `${theme} (${resolvedTheme})` : theme}
                    </span>
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
                {themes.map((themeOption) => (
                    <DropdownMenuItem
                        key={themeOption.value}
                        onClick={() => setTheme(themeOption.value)}
                        className={`flex items-center gap-2 cursor-pointer ${theme === themeOption.value ? 'bg-accent' : ''
                            }`}
                    >
                        <span className="text-lg">{themeOption.icon}</span>
                        <span className="capitalize">{themeOption.value}</span>
                        {theme === themeOption.value && (
                            <span className="ml-auto text-xs text-muted-foreground">✓</span>
                        )}
                    </DropdownMenuItem>
                ))}
            </DropdownMenuContent>
        </DropdownMenu>
    );
}
