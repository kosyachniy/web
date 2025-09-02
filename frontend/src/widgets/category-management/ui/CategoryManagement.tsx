'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { Box } from '@/shared/ui/box';
import { IconButton } from '@/shared/ui/icon-button';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/shared/ui/dialog';
import { Alert, AlertDescription } from '@/shared/ui/alert';
import { AddIcon, RefreshIcon } from '@/shared/ui/icons';
import { useToast } from '@/widgets/feedback-system';
import { getCategories, deleteCategory } from '@/entities/category/api/categoryApi';
import type { Category } from '@/entities/category/model/category';
import { CategoryForm } from './CategoryForm';
import { CategoryTreeItem } from './CategoryTreeItem';

export function CategoryManagement() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
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

  const handleDeleteCategory = async (category: Category) => {
    if (!confirm(`Are you sure you want to delete "${category.title}"? This will also delete all subcategories.`)) {
      return;
    }

    try {
      await deleteCategory(category.id);
      await loadCategories(); // Refresh the list
      toast({
        title: 'Success',
        description: `Category "${category.title}" deleted successfully`,
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
    setIsCreateModalOpen(false);
    setEditingCategory(null);
    await loadCategories();
  };

  const handleFormCancel = () => {
    setIsCreateModalOpen(false);
    setEditingCategory(null);
  };

  if (loading) {
    return (
      <Box>
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          <span className="ml-2">Loading categories...</span>
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
      {/* Action Bar */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <IconButton
            icon={<RefreshIcon size={16} />}
            variant="outline"
            onClick={loadCategories}
            disabled={loading}
          >
            Refresh
          </IconButton>
        </div>

        <Dialog open={isCreateModalOpen} onOpenChange={setIsCreateModalOpen}>
          <DialogTrigger asChild>
            <IconButton
              icon={<AddIcon size={16} />}
              variant="success"
              responsive
            >
              Add Category
            </IconButton>
          </DialogTrigger>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>Create New Category</DialogTitle>
            </DialogHeader>
            <CategoryForm
              onSuccess={handleFormSuccess}
              onCancel={handleFormCancel}
              allCategories={categories}
            />
          </DialogContent>
        </Dialog>
      </div>

      {/* Categories Tree */}
      <Box>
        {categories.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">
            <p>No categories found. Create your first category to get started.</p>
          </div>
        ) : (
          <div className="space-y-2">
            {categories.map((category) => (
              <CategoryTreeItem
                key={category.id}
                category={category}
                level={0}
                onEdit={handleEditCategory}
                onDelete={handleDeleteCategory}
                allCategories={categories}
              />
            ))}
          </div>
        )}
      </Box>

      {/* Edit Category Modal */}
      {editingCategory && (
        <Dialog open={!!editingCategory} onOpenChange={() => setEditingCategory(null)}>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>Edit Category: {editingCategory.title}</DialogTitle>
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