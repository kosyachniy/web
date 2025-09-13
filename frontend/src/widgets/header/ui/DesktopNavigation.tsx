'use client';

import { IconButton } from '@/shared/ui/icon-button';
import { useTranslations, useLocale } from 'next-intl';
import { useRouter } from '@/i18n/routing';
import { PostsIcon, SpaceIcon, HubIcon, CatalogIcon } from '@/shared/ui/icons';
import { CategoriesHoverPopup } from '@/widgets/category';

export default function DesktopNavigation() {
    const t = useTranslations('navigation');
    const locale = useLocale();
    const router = useRouter();

    const navigationItems = [
        {
            key: 'posts',
            label: t('posts'),
            icon: <PostsIcon size={16} />,
            path: '/posts' as const
        },
        {
            key: 'catalog',
            label: t('catalog'),
            icon: <CatalogIcon size={16} />,
            path: '/catalog' as const
        },
        {
            key: 'space',
            label: t('space'),
            icon: <SpaceIcon size={16} />,
            path: '/space' as const
        },
        {
            key: 'hub',
            label: t('hub'),
            icon: <HubIcon size={16} />,
            path: '/hub' as const
        },
    ] as const;

    const handleNavigate = (path: "/" | "/posts" | "/space" | "/hub" | "/catalog") => {
        router.push(path);
    };

    return (
        <nav className="flex items-center space-x-1">
            {navigationItems.map((item) => {
                const button = (
                    <IconButton
                        key={item.key}
                        variant="ghost"
                        size="sm"
                        icon={item.icon}
                        onClick={() => handleNavigate(item.path)}
                        responsive
                        className="text-muted-foreground hover:text-foreground transition-colors"
                    >
                        {item.label}
                    </IconButton>
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
        </nav>
    );
}
