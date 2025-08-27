'use client';

import { Button } from '@/shared/ui/button';
import { Card, CardContent } from '@/shared/ui/card';
import { PageHeader } from '@/shared/ui/page-header';
import { DemoIcon, ComputerIcon, SunIcon, MoonIcon, SaveIcon } from '@/shared/ui/icons';
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
        <div className="w-full max-w-md mx-auto">
            <Card>
                <CardContent>
                    <PageHeader
                        icon={<DemoIcon size={24} />}
                        iconClassName="bg-cyan-500/15 text-cyan-600 dark:bg-cyan-500/20 dark:text-cyan-400"
                        title={t('title')}
                        description={t('description')}
                    />
                    
                    <div className="space-y-6">
                {/* Current Settings Display */}
                <div className="space-y-3">
                    <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
                        <span className="text-sm font-medium">Language:</span>
                        <div className="flex items-center gap-2">
                            <span className="text-lg">{getCurrentLanguage()?.flag}</span>
                            <span className="text-sm font-medium">
                                {getCurrentLanguage()?.name}
                            </span>
                        </div>
                    </div>
                    <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
                        <span className="text-sm font-medium">Theme:</span>
                        <div className="flex items-center gap-2">
                            {(() => {
                                const currentTheme = getCurrentTheme();
                                const IconComponent = currentTheme?.icon;
                                return IconComponent && <IconComponent size={18} />;
                            })()}
                            <span className="text-sm font-medium">
                                {getCurrentTheme()?.name}
                                {userSettings.theme === 'system' && ` (${resolvedTheme})`}
                            </span>
                        </div>
                    </div>
                </div>

                {/* Language Controls */}
                <div className="space-y-2">
                    <h4 className="text-sm font-semibold">Change Language:</h4>
                    <div className="grid grid-cols-2 gap-2">
                        {languages.map((lang) => (
                            <Button
                                key={lang.code}
                                onClick={() => handleLanguageChange(lang.code)}
                                variant={userSettings.language === lang.code ? "default" : "outline"}
                                size="sm"
                                className="text-xs"
                            >
                                {lang.flag} {lang.code.toUpperCase()}
                            </Button>
                        ))}
                    </div>
                </div>

                {/* Theme Controls */}
                <div className="space-y-2">
                    <h4 className="text-sm font-semibold">Change Theme:</h4>
                    <div className="grid grid-cols-3 gap-2">
                        {themes.map((theme) => (
                            <Button
                                key={theme.value}
                                onClick={() => dispatch(setTheme(theme.value as 'system' | 'light' | 'dark'))}
                                variant={userSettings.theme === theme.value ? "default" : "outline"}
                                size="sm"
                                className="text-xs"
                            >
                                {<theme.icon size={16} />}
                            </Button>
                        ))}
                    </div>
                </div>

                {/* Usage Examples */}
                <div className="mt-6 p-3 bg-muted rounded-lg">
                    <h4 className="font-semibold mb-2 text-sm">Redux Integration:</h4>
                    <div className="text-xs text-muted-foreground space-y-1">
                        <p><code>useAppSelector(state =&gt; state.userSettings)</code> - Read state</p>
                        <p><code>dispatch(setLanguage(&apos;en&apos;))</code> - Update language</p>
                        <p><code>dispatch(setTheme(&apos;dark&apos;))</code> - Update theme</p>
                        <p className="mt-2 text-muted-foreground">
                            <SaveIcon size={16} className="inline" /> <strong>Persistent:</strong> Settings automatically save to localStorage
                        </p>
                    </div>
                </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
