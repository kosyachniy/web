'use client';

import React, { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { useTranslations } from 'next-intl';
import { IconButton } from '@/shared/ui/icon-button';
import { ButtonGroup } from '@/shared/ui/button-group';
import { Badge } from '@/shared/ui/badge';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/shared/ui/collapsible';
import { iconContainerVariants } from '@/shared/ui/page-header';
import { cn } from '@/shared/lib/utils';
import {
  EditIcon,
  DeleteIcon,
  ChevronRightIcon,
  ChevronDownIcon,
  AddIcon,
  ImageIcon
} from '@/shared/ui/icons';
import type { Category } from '@/entities/category/model/category';

interface CategoryTreeItemProps {
  category: Category;
  level: number;
  onEdit: (category: Category) => void;
  onDelete: (category: Category) => void;
  onAddSubcategory?: (parentCategory: Category) => void;
  allCategories: Category[];
  isLast?: boolean;
}

interface CategoryMetadata {
  icon?: string;
  color?: string;
  [key: string]: string | number | boolean | undefined;
}

export function CategoryTreeItem({
  category,
  level,
  onEdit,
  onDelete,
  onAddSubcategory,
  allCategories,
  isLast = false
}: CategoryTreeItemProps) {
  const t = useTranslations('admin.categories');
  const [isExpanded, setIsExpanded] = useState(true); // Expand all categories by default

  // Parse metadata from the data field
  let metadata: CategoryMetadata = {};
  try {
    if (category.data) {
      metadata = JSON.parse(category.data);
    }
  } catch {
    // Invalid JSON, use empty object
  }

  const hasSubcategories = category.categories && category.categories.length > 0;
  const paddingLeft = level * 24; // 24px per level for indentation

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
      // Generate background and text colors from the hex color
      const color = metadata.color;
      // Convert hex to rgba with opacity for background
      const hexToRgba = (hex: string, opacity: number) => {
        const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);
        return `rgba(${r}, ${g}, ${b}, ${opacity})`;
      };

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

  const formatDate = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleDateString();
  };

  return (
    <div>
      <div className="hover:bg-muted/30 transition-colors duration-200">
        <div className="flex items-center justify-between p-2 py-3" style={{ marginLeft: `${paddingLeft}px` }}>
          <div className="flex items-center space-x-3 flex-1">
            {/* Expand/Collapse Button - Fixed Width Container */}
            <div className="w-8 flex items-center justify-center">
              {hasSubcategories && (
                <Collapsible open={isExpanded} onOpenChange={setIsExpanded}>
                  <CollapsibleTrigger asChild>
                    <IconButton variant="ghost" size="sm">
                      {isExpanded ? (
                        <ChevronDownIcon size={12} />
                      ) : (
                        <ChevronRightIcon size={12} />
                      )}
                    </IconButton>
                  </CollapsibleTrigger>
                </Collapsible>
              )}
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
                className="w-4 h-4 rounded-full border border-border"
                style={{ backgroundColor: metadata.color }}
              />
            ) : null}

            {/* Category Image */}
            {category.image ? (
              <div className="w-10 h-10 rounded-[0.75rem] overflow-hidden bg-muted">
                <Image
                  src={category.image}
                  alt={category.title}
                  width={40}
                  height={40}
                  className="w-full h-full object-cover"
                />
              </div>
            ) : (
              <div className="w-10 h-10 rounded-[0.75rem] bg-muted flex items-center justify-center">
                <ImageIcon size={16} className="text-muted-foreground" />
              </div>
            )}

            {/* Category Info */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center space-x-2">
                <span className="font-bold text-muted-foreground">#{category.id}</span>
                <h3 className="font-medium truncate">{category.title}</h3>
                <Link 
                  href={`/posts/${category.url}`}
                  className="text-xs text-muted-foreground hover:text-primary transition-colors underline decoration-dashed underline-offset-2"
                >
                  /{category.url}
                </Link>
                {getStatusBadge(category.status || 1)}
              </div>

              <div className="flex items-center text-sm text-muted-foreground mt-1">
                <span>{t('created')}: {formatDate(category.created || 0)}</span>
                {hasSubcategories && (
                  <>
                    <span className="mx-1">•</span>
                    <span>{t('subcategoriesCount', { count: category.categories!.length })}</span>
                  </>
                )}
              </div>
            </div>
          </div>

          {/* Actions */}
          <ButtonGroup>
            {onAddSubcategory && (
              <IconButton
                variant="outline"
                size="sm"
                icon={<AddIcon size={12} />}
                onClick={() => onAddSubcategory(category)}
                responsive
              >
                {t('addSub')}
              </IconButton>
            )}
            <IconButton
              variant="outline"
              size="sm"
              icon={<EditIcon size={12} />}
              onClick={() => onEdit(category)}
              responsive
            >
              {t('edit')}
            </IconButton>
            <IconButton
              variant="destructive"
              size="sm"
              icon={<DeleteIcon size={12} />}
              onClick={() => onDelete(category)}
              responsive
            >
              {t('delete')}
            </IconButton>
          </ButtonGroup>
        </div>
        
        {/* Nested Separator Line */}
        {!(isLast && level === 0) && (
          <div 
            className="h-px bg-border/50" 
            style={{ marginLeft: `${paddingLeft + 8}px` }}
          />
        )}
      </div>

      {/* Subcategories */}
      {hasSubcategories && (
        <Collapsible open={isExpanded} onOpenChange={setIsExpanded}>
          <CollapsibleContent className="space-y-2">
            {category.categories!.map((subcategory, index) => (
              <CategoryTreeItem
                key={subcategory.id}
                category={subcategory}
                level={level + 1}
                onEdit={onEdit}
                onDelete={onDelete}
                onAddSubcategory={onAddSubcategory}
                allCategories={allCategories}
                isLast={index === category.categories!.length - 1}
              />
            ))}
          </CollapsibleContent>
        </Collapsible>
      )}
    </div>
  );
}
