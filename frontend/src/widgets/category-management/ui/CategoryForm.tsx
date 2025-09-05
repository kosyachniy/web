'use client';

import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/shared/ui/button';
import { IconButton } from '@/shared/ui/icon-button';
import { Input } from '@/shared/ui/input';
import { Textarea } from '@/shared/ui/textarea';
import { Label } from '@/shared/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/shared/ui/select';
import { Box } from '@/shared/ui/box';
import { SaveIcon, CancelIcon, UploadIcon, XIcon } from '@/shared/ui/icons';
import { useToast } from '@/widgets/feedback-system';
import { createCategory, updateCategory } from '@/entities/category/api/categoryApi';
import type { Category } from '@/entities/category/model/category';
import Image from 'next/image';

const categorySchema = z.object({
  title: z.string().min(1, 'Title is required').max(100, 'Title must be less than 100 characters'),
  url: z.string().min(1, 'URL is required').max(100, 'URL must be less than 100 characters')
    .regex(/^[a-z0-9-_]+$/, 'URL can only contain lowercase letters, numbers, hyphens, and underscores'),
  description: z.string().max(500, 'Description must be less than 500 characters').optional(),
  parent: z.number().optional(),
  status: z.number().min(0).max(1),
  locale: z.string().optional(),
  icon: z.string().optional(),
  color: z.string().optional(),
  imageFile: z.instanceof(File).optional(),
});

type CategoryFormData = z.infer<typeof categorySchema>;

interface CategoryFormProps {
  category?: Category;
  parentCategory?: Category;
  onSuccess: () => void;
  onCancel: () => void;
  allCategories: Category[];
}

interface CategoryMetadata {
  icon?: string;
  color?: string;
  [key: string]: string | number | boolean | undefined;
}

const DEFAULT_COLORS = [
  '#3b82f6', // blue
  '#10b981', // emerald
  '#f59e0b', // amber
  '#ef4444', // red
  '#8b5cf6', // violet
  '#06b6d4', // cyan
  '#84cc16', // lime
  '#f97316', // orange
  '#ec4899', // pink
  '#6b7280', // gray
];


export function CategoryForm({ 
  category, 
  parentCategory, 
  onSuccess, 
  onCancel, 
  allCategories 
}: CategoryFormProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [selectedImageFile, setSelectedImageFile] = useState<File | null>(null);
  const { toast } = useToast();

  // Parse existing metadata
  const existingMetadata: CategoryMetadata = category?.data ? 
    (() => {
      try {
        return JSON.parse(category.data);
      } catch {
        return {};
      }
    })() : {};

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    setValue,
  } = useForm<CategoryFormData>({
    resolver: zodResolver(categorySchema),
    defaultValues: {
      title: category?.title || '',
      url: category?.url || '',
      description: category?.description || '',
      parent: category?.parent || parentCategory?.id || 0,
      status: category?.status ?? 1,
      locale: category?.locale || 'en',
      icon: existingMetadata.icon || '',
      color: existingMetadata.color || '',
    },
  });

  const watchedTitle = watch('title');
  const watchedIcon = watch('icon');
  const watchedColor = watch('color');

  // Auto-generate URL from title
  useEffect(() => {
    if (!category && watchedTitle) {
      const autoUrl = watchedTitle
        .toLowerCase()
        .replace(/[^a-z0-9\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/--+/g, '-')
        .trim();
      setValue('url', autoUrl);
    }
  }, [watchedTitle, category, setValue]);

  // Set image preview
  useEffect(() => {
    if (category?.image) {
      setImagePreview(category.image);
    }
  }, [category]);

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedImageFile(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const removeImage = () => {
    setSelectedImageFile(null);
    setImagePreview(null);
  };

  // Get all possible parent categories (flatten the tree and exclude current category and its descendants)
  const getAvailableParents = (): Category[] => {
    const flatten = (cats: Category[]): Category[] => {
      const result: Category[] = [];
      for (const cat of cats) {
        result.push(cat);
        if (cat.categories) {
          result.push(...flatten(cat.categories));
        }
      }
      return result;
    };

    const allFlat = flatten(allCategories);
    
    // If editing, exclude current category and its descendants
    if (category) {
      const isDescendant = (cat: Category, ancestorId: number): boolean => {
        if (cat.id === ancestorId) return true;
        if (cat.categories) {
          return cat.categories.some(subcat => isDescendant(subcat, ancestorId));
        }
        return false;
      };

      return allFlat.filter(cat => !isDescendant(cat, category.id));
    }

    return allFlat;
  };

  const onSubmit = async (data: CategoryFormData) => {
    setIsLoading(true);

    try {
      // Prepare metadata
      const metadata: CategoryMetadata = {};
      if (data.icon) metadata.icon = data.icon;
      if (data.color) metadata.color = data.color;

      // Prepare request data
      const requestData = {
        title: data.title,
        url: data.url,
        description: data.description || '',
        parent: data.parent || 0,
        status: data.status,
        locale: data.locale || 'en',
        data: Object.keys(metadata).length > 0 ? JSON.stringify(metadata) : '',
      };

      // TODO: Handle image upload
      // For now, we'll skip image upload as it requires a separate endpoint
      if (selectedImageFile) {
        console.warn('Image upload not yet implemented');
        toast({
          title: 'Note',
          description: 'Image upload will be implemented in the next step',
          variant: 'default',
        });
      }

      if (category) {
        // Update existing category
        await updateCategory(category.id, requestData);
        toast({
          title: 'Success',
          description: `Category "${data.title}" updated successfully`,
          variant: 'default',
        });
      } else {
        // Create new category
        await createCategory(requestData);
        toast({
          title: 'Success',
          description: `Category "${data.title}" created successfully`,
          variant: 'default',
        });
      }

      onSuccess();
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An unexpected error occurred';
      toast({
        title: 'Error',
        description: errorMessage,
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const availableParents = getAvailableParents();

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      {/* Basic Information */}
      <Box size="default">
        <h3 className="font-semibold mb-4">Basic Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="title">Title *</Label>
            <Input 
              id="title"
              {...register('title')}
              placeholder="Enter category title"
            />
            {errors.title && (
              <p className="text-sm text-destructive">{errors.title.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="url">URL Slug *</Label>
            <Input 
              id="url"
              {...register('url')}
              placeholder="category-url-slug"
            />
            {errors.url && (
              <p className="text-sm text-destructive">{errors.url.message}</p>
            )}
          </div>

          <div className="space-y-2 md:col-span-2">
            <Label htmlFor="description">Description</Label>
            <Textarea 
              id="description"
              {...register('description')}
              placeholder="Enter category description (optional)"
              rows={3}
            />
            {errors.description && (
              <p className="text-sm text-destructive">{errors.description.message}</p>
            )}
          </div>
        </div>
      </Box>

      {/* Hierarchy & Settings */}
      <Box size="default">
        <h3 className="font-semibold mb-4">Hierarchy & Settings</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="space-y-2">
            <Label htmlFor="parent">Parent Category</Label>
            <Select
              value={watch('parent')?.toString() || '0'}
              onValueChange={(value) => setValue('parent', parseInt(value) || 0)}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select parent category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="0">Top Level (No Parent)</SelectItem>
                {availableParents.map((cat) => (
                  <SelectItem key={cat.id} value={cat.id.toString()}>
                    {cat.title} (ID: {cat.id})
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="status">Status</Label>
            <Select
              value={watch('status')?.toString() || '1'}
              onValueChange={(value) => setValue('status', parseInt(value))}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="1">Active</SelectItem>
                <SelectItem value="0">Inactive</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="locale">Locale</Label>
            <Select
              value={watch('locale') || 'en'}
              onValueChange={(value) => setValue('locale', value)}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="en">English</SelectItem>
                <SelectItem value="es">Spanish</SelectItem>
                <SelectItem value="fr">French</SelectItem>
                <SelectItem value="de">German</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </Box>

      {/* Visual Customization */}
      <Box size="default">
        <h3 className="font-semibold mb-4">Visual Customization</h3>
        <div className="space-y-4">
          {/* Color Selection */}
          <div className="space-y-2">
            <Label>Category Color</Label>
            <div className="flex flex-wrap gap-2">
              {/* No Color Option */}
              <button
                type="button"
                className={`w-8 h-8 rounded-full border-2 bg-muted flex items-center justify-center ${
                  !watchedColor ? 'border-foreground' : 'border-border'
                }`}
                onClick={() => setValue('color', '')}
                title="No color"
              >
                <span className="text-xs text-muted-foreground">×</span>
              </button>
              {DEFAULT_COLORS.map((color) => (
                <button
                  key={color}
                  type="button"
                  className={`w-8 h-8 rounded-full border-2 ${
                    watchedColor === color ? 'border-foreground' : 'border-border'
                  }`}
                  style={{ backgroundColor: color }}
                  onClick={() => setValue('color', color)}
                />
              ))}
            </div>
            <Input 
              {...register('color')}
              placeholder="Optional: #3b82f6"
              className="w-32"
            />
          </div>

          {/* Icon Selection */}
          <div className="space-y-2">
            <Label>Icon (FontAwesome Key)</Label>
            <Input 
              {...register('icon')}
              placeholder="e.g: user, home, star"
              className="w-48"
            />
            <p className="text-xs text-muted-foreground">
              Enter a FontAwesome icon key (without &apos;fa-&apos; prefix). Leave empty for no icon.
              <br />
              <a 
                href="https://fontawesome.com/search?s=solid&ic=free&o=r" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-primary hover:underline"
              >
                Browse FontAwesome icons →
              </a>
            </p>
          </div>

          {/* Image Upload */}
          <div className="space-y-2">
            <Label>Category Image</Label>
            {imagePreview ? (
              <div className="relative inline-block">
                <Image 
                  src={imagePreview} 
                  alt="Category preview"
                  width={120}
                  height={120}
                  className="rounded-[0.75rem] object-cover border"
                />
                <IconButton
                  type="button"
                  variant="destructive"
                  size="sm"
                  className="absolute -top-2 -right-2"
                  onClick={removeImage}
                  icon={<XIcon size={12} />}
                >
                </IconButton>
              </div>
            ) : (
              <div className="border-2 border-dashed border-border rounded-[0.75rem] p-4 text-center">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange}
                  className="hidden"
                  id="imageUpload"
                />
                <Label htmlFor="imageUpload" className="cursor-pointer">
                  <div className="flex flex-col items-center space-y-2">
                    <UploadIcon size={24} className="text-muted-foreground" />
                    <span className="text-sm text-muted-foreground">Click to upload image</span>
                  </div>
                </Label>
              </div>
            )}
          </div>
        </div>
      </Box>

      {/* Preview */}
      {(watchedTitle || watchedIcon || watchedColor) && (
        <Box size="default">
          <h3 className="font-semibold mb-4">Preview</h3>
          <div className="flex items-center space-x-3 p-3 border rounded-[0.75rem]">
            {watchedIcon ? (
              <div className="w-6 h-6 flex items-center justify-center text-sm">
                <i className={`fas fa-${watchedIcon}`} style={{ color: watchedColor || '#6b7280' }}></i>
              </div>
            ) : watchedColor ? (
              <div 
                className="w-4 h-4 rounded-full"
                style={{ backgroundColor: watchedColor }}
              />
            ) : null}
            <div>
              <h4 className="font-medium">{watchedTitle || 'Category Title'}</h4>
              <p className="text-sm text-muted-foreground">
                /{watch('url') || 'category-url'}
              </p>
            </div>
          </div>
        </Box>
      )}

      {/* Form Actions */}
      <div className="flex items-center justify-end space-x-2 pt-4 border-t">
        <Button 
          type="button" 
          variant="outline"
          onClick={onCancel}
          disabled={isLoading}
        >
          <CancelIcon size={16} className="mr-2" />
          Cancel
        </Button>
        <IconButton
          type="submit"
          variant="default"
          disabled={isLoading}
          icon={<SaveIcon size={16} />}
          responsive
        >
          {isLoading ? 'Saving...' : category ? 'Update Category' : 'Create Category'}
        </IconButton>
      </div>
    </form>
  );
}