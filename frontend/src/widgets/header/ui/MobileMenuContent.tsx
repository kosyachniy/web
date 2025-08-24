'use client';

import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import { useTranslations } from 'next-intl';
import { ThemeSwitcher } from '@/shared/components/layout';
import LanguageSwitcher from '@/features/navigation/components/LanguageSwitcher';
import { UserProfileDropdown } from '@/widgets/user-profile';
import { useRouter } from '@/i18n/routing';

interface MobileMenuContentProps {
    isOpen: boolean;
    onSearchSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
    onClose?: () => void;
}

export default function MobileMenuContent({ isOpen, onSearchSubmit, onClose }: MobileMenuContentProps) {
    const t = useTranslations('system');
    const tNav = useTranslations('navigation');
    const router = useRouter();

    const navigationItems = [
        {
            key: 'posts',
            label: tNav('posts'),
            icon: '📝',
            path: '/posts' as const
        },
        {
            key: 'space',
            label: tNav('space'),
            icon: '🚀',
            path: '/space' as const
        },
        {
            key: 'hub',
            label: tNav('hub'),
            icon: '🏛️',
            path: '/hub' as const
        },
        {
            key: 'catalog',
            label: tNav('catalog'),
            icon: '🛍️',
            path: '/catalog' as const
        }
    ] as const;

    const handleNavigate = (path: "/" | "/posts" | "/space" | "/hub" | "/catalog") => {
        router.push(path);
        onClose?.();
    };

    if (!isOpen) return null;

    return (
        <div className="border-t bg-background w-full">
            <div className="w-full px-4 py-6">
                <div className="flex flex-col space-y-6">
                    {/* Search */}
                    <div className="space-y-2">
                        <label className="text-sm font-medium">{t('search')}</label>
                        <form onSubmit={onSearchSubmit} className="relative">
                            <Input
                                name="search"
                                placeholder={`${t('search')}...`}
                                className="w-full pr-10"
                            />
                            <button
                                type="submit"
                                className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                            >
                                <svg
                                    className="h-4 w-4"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                                    />
                                </svg>
                            </button>
                        </form>
                    </div>

                    {/* Navigation Sections */}
                    <div className="space-y-3 pb-4 border-b">
                        <h3 className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Navigation</h3>
                        {navigationItems.map((item) => (
                            <Button
                                key={item.key}
                                variant="outline"
                                className="w-full justify-start gap-3 h-12"
                                onClick={() => handleNavigate(item.path)}
                            >
                                <span className="text-lg">{item.icon}</span>
                                <span>{item.label}</span>
                            </Button>
                        ))}
                    </div>

                    {/* User Profile */}
                    <UserProfileDropdown className="w-full" />

                    {/* Theme */}
                    <ThemeSwitcher className="w-full" />

                    {/* Language */}
                    <LanguageSwitcher className="w-full" />

                    {/* Quick Actions */}
                    <div className="space-y-3 pt-4 border-t">
                        <Button
                            variant="outline"
                            className="w-full justify-start gap-3 h-12"
                            onClick={() => handleNavigate('/')}
                        >
                            <span className="text-lg">🏠</span>
                            <span>{t('main')}</span>
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    );
}
