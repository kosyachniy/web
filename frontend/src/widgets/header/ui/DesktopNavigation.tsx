'use client';

import { Button } from '@/shared/ui/button';
import { useTranslations } from 'next-intl';
import { useRouter } from '@/i18n/routing';

export default function DesktopNavigation() {
    const t = useTranslations('navigation');
    const router = useRouter();

    const navigationItems = [
        {
            key: 'posts',
            label: t('posts'),
            icon: '📝',
            path: '/posts' as const
        },
        {
            key: 'space',
            label: t('space'),
            icon: '🚀',
            path: '/space' as const
        },
        {
            key: 'hub',
            label: t('hub'),
            icon: '🏛️',
            path: '/hub' as const
        },
        {
            key: 'catalog',
            label: t('catalog'),
            icon: '🛍️',
            path: '/catalog' as const
        }
    ] as const;

    const handleNavigate = (path: "/" | "/posts" | "/space" | "/hub" | "/catalog") => {
        router.push(path);
    };

    return (
        <nav className="flex items-center space-x-1">
            {navigationItems.map((item) => (
                <Button
                    key={item.key}
                    variant="ghost"
                    size="sm"
                    onClick={() => handleNavigate(item.path)}
                    className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
                >
                    <span className="text-base">{item.icon}</span>
                    <span className="hidden lg:inline">{item.label}</span>
                </Button>
            ))}
        </nav>
    );
}