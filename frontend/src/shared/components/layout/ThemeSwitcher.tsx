'use client';

import { useTheme } from '@/providers/ThemeProvider';
import { Button } from '@/shared/ui/button';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from '@/shared/ui/dropdown-menu';
import { ComputerIcon, SunIcon, MoonIcon } from '@/shared/ui/icons';
import { useTranslations } from 'next-intl';

const themes = [
    {
        value: 'system' as const,
        icon: ComputerIcon,
        labelKey: 'system'
    },
    {
        value: 'light' as const,
        icon: SunIcon,
        labelKey: 'light'
    },
    {
        value: 'dark' as const,
        icon: MoonIcon,
        labelKey: 'dark'
    },
] as const;

interface ThemeSwitcherProps {
    className?: string;
}

export default function ThemeSwitcher({ className }: ThemeSwitcherProps = {}) {
    const { theme, resolvedTheme, setTheme } = useTheme();
    const t = useTranslations('theme');

    const currentTheme = themes.find(t => t.value === theme);

    // Get the right icon to display in the button
    const getDisplayIcon = () => {
        if (theme === 'system') {
            const IconComponent = resolvedTheme === 'dark' ? MoonIcon : SunIcon;
            return <IconComponent size={18} />;
        }
        const IconComponent = currentTheme?.icon || SunIcon;
        return <IconComponent size={18} />;
    };

    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button
                    variant="outline"
                    size={className ? "default" : "sm"}
                    className={className ? `justify-start gap-3 h-12 ${className}` : "flex items-center gap-2"}
                >
                    <span>{getDisplayIcon()}</span>
                    <span className={className ? "" : "hidden lg:inline"}>
                        {t(theme)}
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
                        <span><themeOption.icon size={18} /></span>
                        <span>{t(themeOption.labelKey)}</span>
                        {theme === themeOption.value && (
                            <span className="ml-auto text-xs text-muted-foreground">✓</span>
                        )}
                    </DropdownMenuItem>
                ))}
            </DropdownMenuContent>
        </DropdownMenu>
    );
}
