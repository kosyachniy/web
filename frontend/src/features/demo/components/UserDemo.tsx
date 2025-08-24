'use client';

import { Button } from '@/shared/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/ui/card';
import { useAppDispatch, useAppSelector } from '@/shared/stores/store';
import { setLanguage, setTheme } from '../../../features/user/stores/userSettingsSlice';
import { useTheme } from '@/providers/ThemeProvider';
import { useTranslations } from 'next-intl';
import type { Locale } from '@/i18n/routing';

export function UserDemo() {
    const t = useTranslations('userSettings');
    const userSettings = useAppSelector((state) => state.userSettings);
    const dispatch = useAppDispatch();
    const { resolvedTheme } = useTheme();

    const languages: Array<{ code: Locale; name: string; flag: string }> = [
        { code: 'en', name: 'English', flag: '🇺🇸' },
        { code: 'ru', name: 'Русский', flag: '🇷🇺' },
        { code: 'zh', name: '中文', flag: '🇨🇳' },
        { code: 'es', name: 'Español', flag: '🇪🇸' },
        { code: 'ar', name: 'العربية', flag: '🇸🇦' }
    ];

    const themes = [
        { value: 'system', name: 'System', icon: '💻' },
        { value: 'light', name: 'Light', icon: '☀️' },
        { value: 'dark', name: 'Dark', icon: '🌙' }
    ];

    const getCurrentLanguage = () => languages.find(lang => lang.code === userSettings.language);
    const getCurrentTheme = () => themes.find(theme => theme.value === userSettings.theme);

    return (
        <Card className="w-full max-w-md mx-auto">
            <CardHeader>
                <CardTitle>{t('title')}</CardTitle>
                <CardDescription>
                    {t('description')}
                </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
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
                            <span className="text-lg">{getCurrentTheme()?.icon}</span>
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
                                onClick={() => dispatch(setLanguage(lang.code))}
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
                                {theme.icon}
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
                            💾 <strong>Persistent:</strong> Settings automatically save to localStorage
                        </p>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}