'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { useTranslations } from 'next-intl';
import { Box } from '@/shared/ui/box';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/shared/ui/dialog';
import { Alert, AlertDescription } from '@/shared/ui/alert';
import { useToast } from '@/widgets/feedback-system';
import { getCategories, deleteCategory } from '@/entities/category/api/categoryApi';
import type { Category } from '@/entities/category/model/category';
import { CategoryForm } from './CategoryForm';
import { CategoryTreeItem } from './CategoryTreeItem';

interface CategoryManagementProps {
  isCreateModalOpen?: boolean;
  onCreateModalChange?: (open: boolean) => void;
  triggerRefresh?: number; // Used to trigger refresh from parent
}

export function CategoryManagement({ 
  isCreateModalOpen = false, 
  onCreateModalChange,
  triggerRefresh 
}: CategoryManagementProps = {}) {
  const t = useTranslations('admin.categories');
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingCategory, setEditingCategory] = useState<Category | null>(null);
  const { toast } = useToast();

  const loadCategories = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      // Get all categories including nested structure
      const data = await getCategories({ parent: 0 });
      setCategories(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load categories';
      setError(errorMessage);
      toast({
        title: 'Error',
        description: errorMessage,
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  }, [toast]);

  useEffect(() => {
    loadCategories();
  }, [loadCategories]);

  // Trigger refresh from parent
  useEffect(() => {
    if (triggerRefresh) {
      loadCategories();
    }
  }, [triggerRefresh, loadCategories]);

  const handleDeleteCategory = async (category: Category) => {
    if (!confirm(t('deleteConfirm', { title: category.title }))) {
      return;
    }

    try {
      await deleteCategory(category.id);
      await loadCategories(); // Refresh the list
      toast({
        title: 'Success',
        description: t('deleteSuccess', { title: category.title }),
        variant: 'default',
      });
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete category';
      toast({
        title: 'Error',
        description: errorMessage,
        variant: 'destructive',
      });
    }
  };

  const handleEditCategory = (category: Category) => {
    setEditingCategory(category);
  };

  const handleFormSuccess = async () => {
    if (onCreateModalChange) onCreateModalChange(false);
    setEditingCategory(null);
    await loadCategories();
  };

  const handleFormCancel = () => {
    if (onCreateModalChange) onCreateModalChange(false);
    setEditingCategory(null);
  };

  if (loading) {
    return (
      <Box>
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          <span className="ml-2">{t('loading')}</span>
        </div>
      </Box>
    );
  }

  if (error) {
    return (
      <Box>
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      </Box>
    );
  }

  return (
    <div className="space-y-6">

      {/* Categories Tree */}
      <Box>
        {categories.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">
            <p>{t('noCategories')}</p>
          </div>
        ) : (
          <div className="space-y-2">
            {categories.map((category, index) => (
              <CategoryTreeItem
                key={category.id}
                category={category}
                level={0}
                onEdit={handleEditCategory}
                onDelete={handleDeleteCategory}
                allCategories={categories}
                isLast={index === categories.length - 1}
              />
            ))}
          </div>
        )}
      </Box>

      {/* Create Category Modal - controlled by parent */}
      {onCreateModalChange && (
        <Dialog open={isCreateModalOpen} onOpenChange={onCreateModalChange}>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>{t('createTitle')}</DialogTitle>
            </DialogHeader>
            <CategoryForm
              onSuccess={handleFormSuccess}
              onCancel={handleFormCancel}
              allCategories={categories}
            />
          </DialogContent>
        </Dialog>
      )}

      {/* Edit Category Modal */}
      {editingCategory && (
        <Dialog open={!!editingCategory} onOpenChange={() => setEditingCategory(null)}>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>{t('editTitle', { title: editingCategory.title })}</DialogTitle>
            </DialogHeader>
            <CategoryForm
              category={editingCategory}
              onSuccess={handleFormSuccess}
              onCancel={handleFormCancel}
              allCategories={categories}
            />
          </DialogContent>
        </Dialog>
      )}
    </div>
  );
}