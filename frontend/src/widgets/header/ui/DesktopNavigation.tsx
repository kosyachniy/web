'use client';

import { IconButton } from '@/shared/ui/icon-button';
import { useTranslations } from 'next-intl';
import { useRouter } from '@/i18n/routing';
import { PostsIcon, SpaceIcon, HubIcon, CatalogIcon } from '@/shared/ui/icons';

export default function DesktopNavigation() {
    const t = useTranslations('navigation');
    const router = useRouter();

    const navigationItems = [
        {
            key: 'posts',
            label: t('posts'),
            icon: <PostsIcon size={16} />,
            path: '/posts' as const
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
        {
            key: 'catalog',
            label: t('catalog'),
            icon: <CatalogIcon size={16} />,
            path: '/catalog' as const
        }
    ] as const;

    const handleNavigate = (path: "/" | "/posts" | "/space" | "/hub" | "/catalog") => {
        router.push(path);
    };

    return (
        <nav className="flex items-center space-x-1">
            {navigationItems.map((item) => (
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
            ))}
        </nav>
    );
}