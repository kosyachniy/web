'use client';

import React, { useState } from 'react';
import { useTranslations } from 'next-intl';
import { IconButton } from '@/shared/ui/icon-button';
import { ButtonGroup } from '@/shared/ui/button-group';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/shared/ui/collapsible';
import {
  EditIcon,
  DeleteIcon,
  ChevronRightIcon,
  ChevronDownIcon,
  AddIcon
} from '@/shared/ui/icons';
import type { Category } from '@/entities/category/model/category';
import { CategoryPreview, type CategoryPreviewData } from './CategoryPreview';

interface CategoryTreeItemProps {
  category: Category;
  level: number;
  onEdit: (category: Category) => void;
  onDelete: (category: Category) => void;
  onAddSubcategory?: (parentCategory: Category) => void;
  allCategories: Category[];
  isFirst?: boolean;
}

export function CategoryTreeItem({
  category,
  level,
  onEdit,
  onDelete,
  onAddSubcategory,
  allCategories,
  isFirst = false,
}: CategoryTreeItemProps) {
  const t = useTranslations('admin.categories');
  const [isExpanded, setIsExpanded] = useState(true); // Expand all categories by default

  const hasSubcategories = category.categories && category.categories.length > 0;

  // Convert Category to CategoryPreviewData
  const categoryData: CategoryPreviewData = {
    id: category.id,
    title: category.title,
    url: category.url,
    description: category.description,
    image: category.image,
    status: category.status,
    created: category.created,
    locale: category.locale,
    icon: category.icon,
    color: category.color,
    categories: category.categories
  };

  // Left actions: expand/collapse button
  const leftActions = hasSubcategories ? (
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
  ) : null;

  // Right actions: edit/delete buttons
  const rightActions = (
    <ButtonGroup>
      {onAddSubcategory && (
        <div className="hidden md:block">
          <IconButton
            variant="outline"
            size="sm"
            icon={<AddIcon size={12} />}
            onClick={() => onAddSubcategory(category)}
            responsive
          >
            {t('addSub')}
          </IconButton>
        </div>
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
  );


  return (
    <div>
      {/* Separator Line BEFORE category - shorter for deeper levels */}
      {!(level === 0 && isFirst) && (
        <div
          className="h-px bg-border/50"
          style={{
            marginLeft: `${level * 24 + 8}px`,
            width: `calc(100% - ${level * 32 + 16}px)`
          }}
        />
      )}

      {/* Use CategoryPreview as the base component with custom actions */}
      <CategoryPreview
        category={categoryData}
        level={level}
        leftActions={leftActions}
        rightActions={rightActions}
        showDescription={false}
        showCreated={true}
        showSubcategoriesCount={true}
      />

      {/* Subcategories */}
      {hasSubcategories && (
        <Collapsible open={isExpanded} onOpenChange={setIsExpanded}>
          <CollapsibleContent>
            {category.categories!.map((subcategory) => (
              <CategoryTreeItem
                key={subcategory.id}
                category={subcategory}
                level={level + 1}
                onEdit={onEdit}
                onDelete={onDelete}
                onAddSubcategory={onAddSubcategory}
                allCategories={allCategories}
                isFirst={false}
              />
            ))}
          </CollapsibleContent>
        </Collapsible>
      )}
    </div>
  );
}
