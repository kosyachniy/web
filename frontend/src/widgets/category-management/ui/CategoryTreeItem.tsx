'use client';

import React, { useState } from 'react';
import Image from 'next/image';
import { Card } from '@/shared/ui/card';
import { IconButton } from '@/shared/ui/icon-button';
import { ButtonGroup } from '@/shared/ui/button-group';
import { Badge } from '@/shared/ui/badge';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/shared/ui/collapsible';
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
  allCategories
}: CategoryTreeItemProps) {
  const [isExpanded, setIsExpanded] = useState(level === 0); // Expand top-level by default

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
        return <Badge variant="success">Active</Badge>;
      case 0:
        return <Badge variant="secondary">Inactive</Badge>;
      default:
        return <Badge variant="outline">Unknown</Badge>;
    }
  };

  // Category color indicator
  const getCategoryColor = () => {
    if (metadata.color) {
      return metadata.color;
    }
    // Default colors based on level
    const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];
    return colors[level % colors.length];
  };

  const formatDate = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleDateString();
  };

  return (
    <div>
      <Card className="mb-2">
        <div className="flex items-center justify-between p-3" style={{ marginLeft: `${paddingLeft}px` }}>
          <div className="flex items-center space-x-3 flex-1">
            {/* Expand/Collapse Button */}
            {hasSubcategories ? (
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
            ) : (
              <div className="w-8" /> // Spacer for alignment
            )}

            {/* Category Color Indicator */}
            <div
              className="w-4 h-4 rounded-full border border-border"
              style={{ backgroundColor: getCategoryColor() }}
            />

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
                <h3 className="font-medium truncate">{category.title}</h3>
                {getStatusBadge(category.status || 1)}
                {metadata.icon && (
                  <Badge variant="outline" className="text-xs">
                    {metadata.icon}
                  </Badge>
                )}
              </div>

              <div className="flex items-center space-x-4 text-sm text-muted-foreground mt-1">
                <span>#{category.id}</span>
                <span>/{category.url}</span>
                {category.description && (
                  <span className="truncate max-w-[200px]">{category.description}</span>
                )}
                <span>Created: {formatDate(category.created || 0)}</span>
                {hasSubcategories && (
                  <span>{category.categories!.length} subcategories</span>
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
                Add Sub
              </IconButton>
            )}
            <IconButton
              variant="outline"
              size="sm"
              icon={<EditIcon size={12} />}
              onClick={() => onEdit(category)}
              responsive
            >
              Edit
            </IconButton>
            <IconButton
              variant="destructive"
              size="sm"
              icon={<DeleteIcon size={12} />}
              onClick={() => onDelete(category)}
              responsive
            >
              Delete
            </IconButton>
          </ButtonGroup>
        </div>
      </Card>

      {/* Subcategories */}
      {hasSubcategories && (
        <Collapsible open={isExpanded} onOpenChange={setIsExpanded}>
          <CollapsibleContent className="space-y-2">
            {category.categories!.map((subcategory) => (
              <CategoryTreeItem
                key={subcategory.id}
                category={subcategory}
                level={level + 1}
                onEdit={onEdit}
                onDelete={onDelete}
                onAddSubcategory={onAddSubcategory}
                allCategories={allCategories}
              />
            ))}
          </CollapsibleContent>
        </Collapsible>
      )}
    </div>
  );
}
