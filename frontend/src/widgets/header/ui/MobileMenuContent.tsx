'use client';

import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import { useTranslations, useLocale } from 'next-intl';
import { ThemeSwitcher } from '@/shared/components/layout';
import LanguageSwitcher from '@/features/navigation/components/LanguageSwitcher';
import { UserProfileDropdown } from '@/widgets/user-profile';
import { PostsIcon, SpaceIcon, HubIcon, CatalogIcon, HomeIcon, SearchIcon } from '@/shared/ui/icons';
import { useRouter } from '@/i18n/routing';
import { CategoriesHoverPopup } from '@/widgets/category';

interface MobileMenuContentProps {
    isOpen: boolean;
    onSearchSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
    onClose?: () => void;
}

export default function MobileMenuContent({ isOpen, onSearchSubmit, onClose }: MobileMenuContentProps) {
    const t = useTranslations('system');
    const tNav = useTranslations('navigation');
    const locale = useLocale();
    const router = useRouter();

    const navigationItems = [
        {
            key: 'posts',
            label: tNav('posts'),
            icon: PostsIcon,
            path: '/posts' as const
        },
        {
            key: 'catalog',
            label: tNav('catalog'),
            icon: CatalogIcon,
            path: '/catalog' as const
        },
        {
            key: 'space',
            label: tNav('space'),
            icon: SpaceIcon,
            path: '/space' as const
        },
        {
            key: 'hub',
            label: tNav('hub'),
            icon: HubIcon,
            path: '/hub' as const
        },
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
                        <form onSubmit={onSearchSubmit} className="relative">
                            <Input
                                name="search"
                                placeholder={`${t('search')}...`}
                                className="w-full pr-10"
                                title=""
                                autoComplete="off"
                            />
                            <button
                                type="submit"
                                className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                            >
                                <SearchIcon size={16} />
                            </button>
                        </form>
                    </div>

                    {/* Navigation Sections */}
                    <div className="space-y-3 pb-4 border-b">
                        <h3 className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Navigation</h3>
                        {navigationItems.map((item) => {
                            const button = (
                                <Button
                                    key={item.key}
                                    variant="outline"
                                    className="w-full justify-start gap-3 h-12"
                                    onClick={() => handleNavigate(item.path)}
                                >
                                    <item.icon size={18} />
                                    <span>{item.label}</span>
                                </Button>
                            );

                            // Wrap Posts navigation item with CategoriesHoverPopup
                            if (item.key === 'posts') {
                                return (
                                    <CategoriesHoverPopup key={item.key} locale={locale}>
                                        {button}
                                    </CategoriesHoverPopup>
                                );
                            }

                            return button;
                        })}
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
                            <HomeIcon size={18} />
                            <span>{t('main')}</span>
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    );
}
