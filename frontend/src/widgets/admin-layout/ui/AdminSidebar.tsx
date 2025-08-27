'use client';

import { useTranslations } from 'next-intl';
import { useRouter, usePathname } from '@/i18n/routing';
import { Card } from '@/shared/ui/card';
import { Button } from '@/shared/ui/button';

interface AdminSidebarProps {
  className?: string;
}

export default function AdminSidebar({ className }: AdminSidebarProps) {
  const t = useTranslations('system');
  const tNav = useTranslations('navigation');
  const router = useRouter();
  const pathname = usePathname();

  const menuItems = [
    {
      key: 'categories',
      label: t('categories'),
      href: '/admin/categories' as const,
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14-7H5a2 2 0 00-2 2v12a2 2 0 002 2h14a2 2 0 002-2V6a2 2 0 00-2-2z" />
        </svg>
      )
    },
    {
      key: 'posts',
      label: tNav('posts'),
      href: '/admin/posts' as const, 
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      )
    },
    {
      key: 'users',
      label: t('users'),
      href: '/admin/users' as const,
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z" />
        </svg>
      )
    }
  ] as const;

  const handleNavigation = (href: '/admin/categories' | '/admin/posts' | '/admin/users') => {
    router.push(href);
  };

  const isActive = (href: string) => {
    return pathname === href;
  };

  return (
    <Card className={`p-4 h-fit ${className}`}>
      <div className="space-y-2">
        <h3 className="font-medium text-lg mb-4">{t('admin_panel')}</h3>
        {menuItems.map((item) => (
          <Button
            key={item.key}
            variant={isActive(item.href) ? 'default' : 'ghost'}
            className={`w-full justify-start gap-3 ${
              isActive(item.href) 
                ? 'bg-primary text-primary-foreground' 
                : 'hover:bg-muted'
            }`}
            onClick={() => handleNavigation(item.href)}
          >
            {item.icon}
            {item.label}
          </Button>
        ))}
      </div>
    </Card>
  );
}