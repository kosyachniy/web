'use client';

import { useLocale } from 'next-intl';
import { useRouter, usePathname } from '@/i18n/routing';
import { Button } from '@/shared/ui/button';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from '@/shared/ui/dropdown-menu';
import { useAppDispatch, useAppSelector } from '@/shared/stores/store';
import { setLanguage } from '@/features/user/stores/userSettingsSlice';
import type { Locale } from '@/i18n/routing';

const languages = [
    { code: 'en' as Locale, name: 'English', flag: '🇺🇸' },
    { code: 'ru' as Locale, name: 'Русский', flag: '🇷🇺' },
    { code: 'zh' as Locale, name: '中文', flag: '🇨🇳' },
    { code: 'es' as Locale, name: 'Español', flag: '🇪🇸' },
    { code: 'ar' as Locale, name: 'العربية', flag: '🇸🇦' },
];

interface LanguageSwitcherProps {
    className?: string;
}

export default function LanguageSwitcher({ className }: LanguageSwitcherProps = {}) {
    const locale = useLocale();
    const router = useRouter();
    const pathname = usePathname();
    const dispatch = useAppDispatch();

    // Get current language from Redux store
    const userLanguage = useAppSelector((state) => state.userSettings.language);

    const currentLanguage = languages.find(lang => lang.code === locale);

    const handleLanguageChange = (newLocale: Locale) => {
        // Update Redux store
        dispatch(setLanguage(newLocale));

        // Update URL and next-intl routing
        router.replace(pathname, { locale: newLocale });
    };

    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button
                    variant="outline"
                    size={className ? "default" : "sm"}
                    className={className ? `justify-start gap-3 h-12 ${className}` : "flex items-center gap-2"}
                >
                    <span className="text-lg">{currentLanguage?.flag}</span>
                    <span className={className ? "" : "hidden lg:inline"}>{currentLanguage?.name}</span>
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
                {languages.map((language) => (
                    <DropdownMenuItem
                        key={language.code}
                        onClick={() => handleLanguageChange(language.code)}
                        className={`flex items-center gap-2 cursor-pointer ${locale === language.code ? 'bg-accent' : ''
                            }`}
                    >
                        <span className="text-lg">{language.flag}</span>
                        <span>{language.name}</span>
                        {userLanguage === language.code && (
                            <span className="ml-auto text-xs text-muted-foreground">✓</span>
                        )}
                    </DropdownMenuItem>
                ))}
            </DropdownMenuContent>
        </DropdownMenu>
    );
}
