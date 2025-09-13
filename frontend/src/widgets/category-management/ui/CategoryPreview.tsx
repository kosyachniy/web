'use client';

import React from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { useTranslations } from 'next-intl';
import { Badge } from '@/shared/ui/badge';
import { iconContainerVariants } from '@/shared/ui/page-header';
import { cn } from '@/shared/lib/utils';
import { ImageIcon } from '@/shared/ui/icons';
import { formatDate } from '@/shared/lib/date';

interface CategoryMetadata {
  icon?: string;
  color?: string;
  [key: string]: string | number | boolean | undefined;
}

interface CategoryPreviewData {
  id?: number;
  title: string;
  url: string;
  description?: string;
  image?: string;
  status?: number;
  created?: number;
  locale?: string;
  categories?: CategoryPreviewData[];
  icon?: string;
  color?: string;
}

interface CategoryPreviewProps {
  category: CategoryPreviewData;
  level?: number;
  className?: string;
  leftActions?: React.ReactNode;
  rightActions?: React.ReactNode;
  showDescription?: boolean;
  showCreated?: boolean;
  showSubcategoriesCount?: boolean;
  containerClassName?: string;
}

export function CategoryPreview({
  category,
  level = 0,
  className = '',
  leftActions,
  rightActions,
  showDescription = true,
  showCreated = true,
  showSubcategoriesCount = true,
  containerClassName = ''
}: CategoryPreviewProps) {
  const t = useTranslations('admin.categories');
  const tSystem = useTranslations('system');

  // Get icon and color from direct fields only
  const getIconAndColor = (category: CategoryPreviewData): CategoryMetadata => {
    return {
      icon: category.icon,
      color: category.color,
    };
  };

  const metadata = getIconAndColor(category);

  // Helper function to convert hex to rgba
  const hexToRgba = (hex: string, opacity: number) => {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r}, ${g}, ${b}, ${opacity})`;
  };

  // Status badge styling
  const getStatusBadge = (status: number) => {
    switch (status) {
      case 1:
        return <Badge variant="success">{t('active')}</Badge>;
      case 0:
        return <Badge variant="secondary">{t('inactive')}</Badge>;
      default:
        return <Badge variant="outline">Unknown</Badge>;
    }
  };

  // Category color styling for icon container
  const getCategoryColorClass = (forceDefault = false) => {
    if (metadata.color && !forceDefault) {
      const color = metadata.color;
      
      return {
        backgroundColor: hexToRgba(color, 0.15),
        color: color,
        darkBackgroundColor: hexToRgba(color, 0.2),
        darkColor: color,
        style: {
          backgroundColor: hexToRgba(color, 0.15),
          color: color,
        }
      };
    }

    // Default muted color for icons without custom color
    if (forceDefault) {
      return {
        className: 'bg-muted text-muted-foreground',
        style: {}
      };
    }

    // Default colors based on level with proper Tailwind classes
    const colorClasses = [
      'bg-blue-500/15 text-blue-600 dark:bg-blue-500/20 dark:text-blue-400',
      'bg-green-500/15 text-green-600 dark:bg-green-500/20 dark:text-green-400',
      'bg-amber-500/15 text-amber-600 dark:bg-amber-500/20 dark:text-amber-400',
      'bg-red-500/15 text-red-600 dark:bg-red-500/20 dark:text-red-400',
      'bg-purple-500/15 text-purple-600 dark:bg-purple-500/20 dark:text-purple-400'
    ];
    return { className: colorClasses[level % colorClasses.length] };
  };

  const hasSubcategories = category.categories && category.categories.length > 0;
  const paddingLeft = level * 24; // 24px per level for indentation

  // No default right actions for preview mode
  const defaultRightActions = null;

  return (
    <div className={cn('hover:bg-muted/30 transition-colors duration-200', containerClassName)}>
      <div 
        className={cn('flex items-center justify-between p-2 py-3 min-w-0', className)} 
        style={{ marginLeft: `${paddingLeft}px` }}
      >
        <div className="flex items-center space-x-3 flex-1 min-w-0">
          {/* Left Actions Area (expand/collapse buttons, etc.) */}
          <div className="w-8 flex items-center justify-center">
            {leftActions}
          </div>

          {/* Category Colored Icon */}
          {metadata.icon ? (
            <div
              className={cn(
                iconContainerVariants({ size: 'sm' }),
                metadata.color ? getCategoryColorClass().className : getCategoryColorClass(true).className,
                "mt-0" // Override margin to align with category image
              )}
              style={metadata.color ? getCategoryColorClass().style : getCategoryColorClass(true).style}
            >
              <i className={`fas fa-${metadata.icon}`}></i>
            </div>
          ) : metadata.color ? (
            <div
              className="w-4 h-4 rounded-full"
              style={{ backgroundColor: metadata.color }}
            />
          ) : null}

          {/* Category Image - Hidden on mobile */}
          {category.image ? (
            <div className="w-10 h-10 rounded-[0.75rem] overflow-hidden bg-muted hidden md:flex">
              <Image
                src={category.image}
                alt={category.title}
                width={40}
                height={40}
                className="w-full h-full object-cover"
              />
            </div>
          ) : (
            <div className="w-10 h-10 rounded-[0.75rem] bg-muted flex items-center justify-center hidden md:flex">
              <ImageIcon size={16} className="text-muted-foreground" />
            </div>
          )}

          {/* Category Info */}
          {(() => {
            // Build array of content items that will actually be displayed in 2nd row
            const contentItems = [];
            
            // Add locale flag if it exists
            if (category.locale) {
              const getLocaleFlag = (locale: string) => {
                switch (locale) {
                  case 'en': return '🇺🇸';
                  case 'ru': return '🇷🇺';
                  case 'es': return '🇪🇸';
                  case 'ar': return '🇸🇦';
                  case 'zh': return '🇨🇳';
                  default: return '🌐';
                }
              };
              contentItems.push(`${tSystem('locale')}: ${getLocaleFlag(category.locale)}`);
            }
            
            if (showCreated && category.created) {
              contentItems.push(`${t('created')}: ${formatDate(category.created)}`);
            }
            
            if (showSubcategoriesCount && hasSubcategories) {
              contentItems.push(t('subcategoriesCount', { count: category.categories!.length }));
            }
            
            if (showDescription && category.description) {
              contentItems.push(category.description);
            }
            
            const hasSecondRow = contentItems.length > 0;
            
            return (
              <div className={cn(
                "flex-1 min-w-0 overflow-hidden",
                hasSecondRow ? "" : "flex items-center" // Center vertically when no 2nd row
              )}>
                <div className="flex items-center space-x-2">
                  <span className="font-bold text-muted-foreground hidden md:inline">#{category.id || 'NEW'}</span>
                  <h3 className="font-medium truncate">{category.title}</h3>
                  <Link 
                    href={`/posts/${category.url}`}
                    className="text-xs text-muted-foreground hover:text-primary transition-colors underline decoration-dashed underline-offset-2"
                  >
                    /{category.url}
                  </Link>
                  <div className="hidden md:block">
                    {getStatusBadge(category.status ?? 1)}
                  </div>
                </div>

                {hasSecondRow && (
                  <div className="flex items-center text-sm text-muted-foreground mt-1 hidden md:flex">
                    <span className="truncate">{contentItems.join(' • ')}</span>
                  </div>
                )}
              </div>
            );
          })()}
        </div>

        {/* Right Actions Area (edit/delete buttons, preview badge, etc.) */}
        <div className="flex-shrink-0">
          {rightActions || defaultRightActions}
        </div>
      </div>
    </div>
  );
}

// Export the interface for reuse
export type { CategoryPreviewData };