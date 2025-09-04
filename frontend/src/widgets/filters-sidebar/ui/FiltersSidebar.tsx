'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import { SidebarCard } from '@/shared/ui/sidebar-card';
import { IconButton } from '@/shared/ui/icon-button';
import { ButtonGroup } from '@/shared/ui/button-group';
import { 
  FilterIcon, 
  CalendarIcon, 
  TagIcon,
  TrendingIcon,
  ClockIcon
} from '@/shared/ui/icons';

interface FiltersSidebarProps {
  className?: string;
}

export default function FiltersSidebar({ className }: FiltersSidebarProps) {
  const t = useTranslations('filters');
  const [activeTimeFilter, setActiveTimeFilter] = useState<string>('all');
  const [activeSortFilter, setActiveSortFilter] = useState<string>('recent');

  const timeFilters = [
    { key: 'today', label: t('today'), icon: <CalendarIcon size={16} /> },
    { key: 'week', label: t('thisWeek'), icon: <CalendarIcon size={16} /> },
    { key: 'month', label: t('thisMonth'), icon: <CalendarIcon size={16} /> },
    { key: 'all', label: t('allTime'), icon: <ClockIcon size={16} /> }
  ];

  const sortFilters = [
    { key: 'recent', label: t('mostRecent'), icon: <ClockIcon size={16} /> },
    { key: 'popular', label: t('mostPopular'), icon: <TrendingIcon size={16} /> },
    { key: 'trending', label: t('trending'), icon: <TrendingIcon size={16} /> }
  ];

  return (
    <SidebarCard 
      title={t('filters')}
      icon={<FilterIcon size={20} />}
      className={className}
    >
      <div className="space-y-6">
        {/* Time Filters */}
        <div className="space-y-3">
          <h4 className="font-medium text-sm text-muted-foreground uppercase tracking-wide">
            {t('timeRange')}
          </h4>
          <div className="space-y-1">
            {timeFilters.map((filter) => (
              <IconButton
                key={filter.key}
                icon={filter.icon}
                variant={activeTimeFilter === filter.key ? 'default' : 'ghost'}
                size="sm"
                className="w-full justify-start"
                onClick={() => setActiveTimeFilter(filter.key)}
                responsive
              >
                {filter.label}
              </IconButton>
            ))}
          </div>
        </div>

        {/* Sort Filters */}
        <div className="space-y-3">
          <h4 className="font-medium text-sm text-muted-foreground uppercase tracking-wide">
            {t('sortBy')}
          </h4>
          <div className="space-y-1">
            {sortFilters.map((filter) => (
              <IconButton
                key={filter.key}
                icon={filter.icon}
                variant={activeSortFilter === filter.key ? 'default' : 'ghost'}
                size="sm"
                className="w-full justify-start"
                onClick={() => setActiveSortFilter(filter.key)}
                responsive
              >
                {filter.label}
              </IconButton>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="pt-4 border-t">
          <ButtonGroup className="w-full">
            <IconButton
              icon={<TagIcon size={14} />}
              variant="outline"
              size="sm"
              className="flex-1"
              responsive
            >
              {t('clearFilters')}
            </IconButton>
          </ButtonGroup>
        </div>
      </div>
    </SidebarCard>
  );
}