'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useTranslations } from 'next-intl';
import { Popover, PopoverContent, PopoverTrigger } from '@/shared/ui/popover';
import { Box } from '@/shared/ui/box';
import { Badge } from '@/shared/ui/badge';
import { iconContainerVariants } from '@/shared/ui/page-header';
import { cn } from '@/shared/lib/utils';
import type { Category } from '@/entities/category';
import { getCategories } from '@/entities/category';

interface CategoryMetadata {
  icon?: string;
  color?: string;
  [key: string]: string | number | boolean | undefined;
}

interface CategoriesHoverPopupProps {
  children: React.ReactNode;
  locale: string;
  className?: string;
}


export function CategoriesHoverPopup({
  children,
  locale,
  className = ''
}: CategoriesHoverPopupProps) {
  const t = useTranslations('categories.popup');
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  // Helper function to convert hex to rgba
  const hexToRgba = (hex: string, opacity: number) => {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r}, ${g}, ${b}, ${opacity})`;
  };

  // Get category color styling
  const getCategoryColorStyle = (metadata: CategoryMetadata) => {
    if (metadata.color) {
      return {
        backgroundColor: hexToRgba(metadata.color, 0.15),
        color: metadata.color,
      };
    }
    return {};
  };

  // Get category icon and color from direct fields
  const getCategoryIconAndColor = (category: Category): CategoryMetadata => {
    return {
      icon: category.icon,
      color: category.color
    };
  };

  // Load categories when popup opens
  useEffect(() => {
    if (isOpen && categories.length === 0) {
      setIsLoading(true);
      getCategories({ parent: 0, locale, status: 1, include_tree: true })
        .then(setCategories)
        .catch((error) => {
          console.warn('Failed to load categories for hover popup:', error);
          setCategories([]);
        })
        .finally(() => setIsLoading(false));
    }
  }, [isOpen, locale, categories.length]);

  return (
    <Popover
      open={isOpen}
      onOpenChange={setIsOpen}
    >
      <PopoverTrigger
        asChild
        className={className}
        onMouseEnter={() => setIsOpen(true)}
        onMouseLeave={() => setIsOpen(false)}
      >
        {children}
      </PopoverTrigger>
      <PopoverContent
        className="w-[calc(100vw-2rem)] sm:w-80 max-w-80 p-0"
        side="bottom"
        align="start"
        onMouseEnter={() => setIsOpen(true)}
        onMouseLeave={() => setIsOpen(false)}
      >
        <Box size="sm" className="rounded-[0.75rem]">
          {/* Content - No header */}
          {isLoading ? (
            <div className="text-muted-foreground text-sm py-4 text-center">
              {t('loading')}
            </div>
          ) : categories.length > 0 ? (
            <div className="space-y-2">
              {categories.slice(0, 8).map((category) => {
                const metadata = getCategoryIconAndColor(category);

                return (
                  <Link
                    key={category.id}
                    href={`/posts/${category.url}`}
                    className="flex items-center gap-2 p-2 rounded-[0.75rem] hover:bg-muted/50 transition-colors cursor-pointer group"
                  >
                    {/* Category Icon - Just the icon without colored background */}
                    {metadata.icon ? (
                      <i className={`fas fa-${metadata.icon} text-muted-foreground text-sm flex-shrink-0`}></i>
                    ) : null}

                    <span className="text-sm truncate flex-1">
                      {category.title}
                    </span>

                    <div className="flex items-center gap-1 flex-shrink-0">
                      {/* Post count */}
                      {category.post_count !== undefined && category.post_count > 0 && (
                        <Badge variant="outline" className="text-xs">
                          {category.post_count}
                        </Badge>
                      )}
                      
                      {/* Subcategory count - only show when greater than 0 */}
                      {category.categories && category.categories.length > 0 && (
                        <Badge variant="secondary" className="text-xs">
                          {category.categories.length}
                        </Badge>
                      )}
                    </div>
                  </Link>
                );
              })}

              {categories.length > 8 && (
                <Link
                  href="/posts"
                  className="block p-2 text-center text-sm text-muted-foreground hover:text-foreground hover:bg-muted/50 rounded-[0.75rem] transition-colors cursor-pointer"
                >
                  {t('viewAll', { count: categories.length })}
                </Link>
              )}
            </div>
          ) : (
            <div className="text-muted-foreground text-sm py-4 text-center">
              {t('empty')}
            </div>
          )}
        </Box>
      </PopoverContent>
    </Popover>
  );
}
