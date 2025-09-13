'use client';

import { Button } from '@/shared/ui/button';
import { Box } from '@/shared/ui/box';
import { PageHeader } from '@/shared/ui/page-header';
import { UserIcon, ComputerIcon, SunIcon, MoonIcon, SaveIcon } from '@/shared/ui/icons';
import { useAppDispatch, useAppSelector } from '@/shared/stores/store';
import { setLanguage, setTheme } from '../../../features/user/stores/userSettingsSlice';
import { useTheme } from '@/providers/ThemeProvider';
import { useTranslations } from 'next-intl';
import { useRouter, usePathname } from '@/i18n/routing';
import type { Locale } from '@/i18n/routing';

export function UserDemo() {
    const t = useTranslations('userSettings');
    const userSettings = useAppSelector((state) => state.userSettings);
    const dispatch = useAppDispatch();
    const { resolvedTheme } = useTheme();
    const router = useRouter();
    const pathname = usePathname();

    const languages: Array<{ code: Locale; name: string; flag: string }> = [
        { code: 'en', name: 'English', flag: '🇺🇸' },
        { code: 'ru', name: 'Русский', flag: '🇷🇺' },
        { code: 'zh', name: '中文', flag: '🇨🇳' },
        { code: 'es', name: 'Español', flag: '🇪🇸' },
        { code: 'ar', name: 'العربية', flag: '🇸🇦' }
    ];

    const themes = [
        { value: 'system', name: 'System', icon: ComputerIcon },
        { value: 'light', name: 'Light', icon: SunIcon },
        { value: 'dark', name: 'Dark', icon: MoonIcon }
    ];

    const getCurrentLanguage = () => languages.find(lang => lang.code === userSettings.language);
    const getCurrentTheme = () => themes.find(theme => theme.value === userSettings.theme);

    const handleLanguageChange = (newLocale: Locale) => {
        // Update Redux store
        dispatch(setLanguage(newLocale));

        // Update URL and next-intl routing
        router.replace(pathname, { locale: newLocale });
    };

    return (
        <div className="max-w-2xl mx-auto">
            <PageHeader
                icon={<UserIcon size={24} />}
                iconClassName="bg-purple-500/15 text-purple-600 dark:bg-purple-500/20 dark:text-purple-400"
                title={t('title')}
                description={t('description')}
            />

            <Box size="lg">
                <div className="space-y-6">
                    {/* Language Controls */}
                    <div className="space-y-4">
                        <h4 className="font-semibold">Change Language:</h4>
                        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
                            {languages.map((lang) => (
                                <Button
                                    key={lang.code}
                                    onClick={() => handleLanguageChange(lang.code)}
                                    variant={userSettings.language === lang.code ? "default" : "outline"}
                                    className="w-full"
                                >
                                    <span className="mr-2">{lang.flag}</span>
                                    {lang.code.toUpperCase()}
                                </Button>
                            ))}
                        </div>
                    </div>

                    {/* Theme Controls */}
                    <div className="space-y-4">
                        <h4 className="font-semibold">Change Theme:</h4>
                        <div className="grid grid-cols-3 gap-3">
                            {themes.map((theme) => (
                                <Button
                                    key={theme.value}
                                    onClick={() => dispatch(setTheme(theme.value as 'system' | 'light' | 'dark'))}
                                    variant={userSettings.theme === theme.value ? "default" : "outline"}
                                    className="w-full"
                                >
                                    <theme.icon size={16} className="mr-2" />
                                    {theme.name}
                                </Button>
                            ))}
                        </div>
                    </div>
                </div>
            </Box>
        </div>
    );
}
