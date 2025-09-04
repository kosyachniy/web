'use client';

import { useTranslations } from 'next-intl';
import { SidebarCard } from '@/shared/ui/sidebar-card';
import { IconButton } from '@/shared/ui/icon-button';
import { ButtonGroup } from '@/shared/ui/button-group';
import { 
  AddIcon, 
  SearchIcon, 
  BookmarkIcon,
  ShareIcon,
  SettingsIcon,
  LightningIcon
} from '@/shared/ui/icons';

interface FastActionsSidebarProps {
  className?: string;
}

export default function FastActionsSidebar({ className }: FastActionsSidebarProps) {
  const t = useTranslations('actions');

  const primaryActions = [
    {
      key: 'create',
      label: t('createPost'),
      icon: <AddIcon size={16} />,
      variant: 'success' as const
    },
    {
      key: 'search',
      label: t('search'),
      icon: <SearchIcon size={16} />,
      variant: 'outline' as const
    }
  ];

  const quickActions = [
    {
      key: 'bookmark',
      label: t('bookmarks'),
      icon: <BookmarkIcon size={16} />,
      variant: 'ghost' as const
    },
    {
      key: 'share',
      label: t('share'),
      icon: <ShareIcon size={16} />,
      variant: 'ghost' as const
    },
    {
      key: 'settings',
      label: t('settings'),
      icon: <SettingsIcon size={16} />,
      variant: 'ghost' as const
    }
  ];

  return (
    <SidebarCard
      title={t('fastActions')}
      icon={<LightningIcon size={20} />}
      className={className}
    >
      <div className="space-y-6">

        {/* Primary Actions */}
        <div className="space-y-2">
          {primaryActions.map((action) => (
            <IconButton
              key={action.key}
              icon={action.icon}
              variant={action.variant}
              className="w-full"
              responsive
            >
              {action.label}
            </IconButton>
          ))}
        </div>

        {/* Quick Actions */}
        <div className="space-y-3">
          <h4 className="font-medium text-sm text-muted-foreground uppercase tracking-wide">
            {t('quickAccess')}
          </h4>
          <div className="space-y-1">
            {quickActions.map((action) => (
              <IconButton
                key={action.key}
                icon={action.icon}
                variant={action.variant}
                size="sm"
                className="w-full justify-start"
                responsive
              >
                {action.label}
              </IconButton>
            ))}
          </div>
        </div>

        {/* Action Buttons Group */}
        <div className="pt-4 border-t">
          <ButtonGroup className="w-full grid grid-cols-2 gap-2">
            <IconButton
              icon={<BookmarkIcon size={14} />}
              variant="outline"
              size="sm"
              responsive
            >
              {t('saved')}
            </IconButton>
            <IconButton
              icon={<ShareIcon size={14} />}
              variant="outline"
              size="sm"
              responsive
            >
              {t('shared')}
            </IconButton>
          </ButtonGroup>
        </div>
      </div>
    </SidebarCard>
  );
}