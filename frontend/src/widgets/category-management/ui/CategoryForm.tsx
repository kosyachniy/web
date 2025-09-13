'use client';

import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useTranslations } from 'next-intl';
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
import { CategoryPreview } from './CategoryPreview';
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
  const t = useTranslations('admin.categories');
  const [isLoading, setIsLoading] = useState(false);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [selectedImageFile, setSelectedImageFile] = useState<File | null>(null);
  const { toast } = useToast();

  // Get icon and color from direct fields or fallback to parsing data field
  const getIconAndColor = () => {
    if (category?.icon || category?.color) {
      // Use new direct fields if available
      return { icon: category.icon || '', color: category.color || '' };
    }
    
    // Fallback to parsing data field for backward compatibility
    if (category?.data) {
      try {
        const parsed = JSON.parse(category.data);
        return { icon: parsed.icon || '', color: parsed.color || '' };
      } catch {
        return { icon: '', color: '' };
      }
    }
    
    return { icon: '', color: '' };
  };

  const { icon: initialIcon, color: initialColor } = getIconAndColor();

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    setValue,
    reset,
  } = useForm<CategoryFormData>({
    resolver: zodResolver(categorySchema),
    defaultValues: {
      title: category?.title || '',
      url: category?.url || '',
      description: category?.description || '',
      parent: category?.parent ?? parentCategory?.id ?? 0,
      status: category?.status ?? 1,
      locale: category?.locale || 'none',
      icon: initialIcon,
      color: initialColor,
    },
  });

  // Reset form values when category changes (for editing)
  useEffect(() => {
    if (category) {
      // Get icon and color using the same logic
      const getResetIconAndColor = () => {
        if (category.icon || category.color) {
          return { icon: category.icon || '', color: category.color || '' };
        }
        
        if (category.data) {
          try {
            const parsed = JSON.parse(category.data);
            return { icon: parsed.icon || '', color: parsed.color || '' };
          } catch {
            return { icon: '', color: '' };
          }
        }
        
        return { icon: '', color: '' };
      };

      const { icon, color } = getResetIconAndColor();

      reset({
        title: category.title || '',
        url: category.url || '',
        description: category.description || '',
        parent: category.parent ?? 0,
        status: category.status ?? 1,
        locale: category.locale || 'none',
        icon: icon,
        color: color,
      });
    } else if (parentCategory) {
      // When creating a subcategory
      setValue('parent', parentCategory.id);
    }
  }, [category, parentCategory, reset, setValue]);

  const watchedTitle = watch('title');
  const watchedIcon = watch('icon');
  const watchedColor = watch('color');
  const watchedUrl = watch('url');
  const watchedDescription = watch('description');
  const watchedStatus = watch('status');

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
      // Find all descendants of the current category
      const findDescendants = (parentCat: Category): number[] => {
        const descendants: number[] = [parentCat.id]; // Include the category itself
        if (parentCat.categories) {
          for (const child of parentCat.categories) {
            descendants.push(...findDescendants(child));
          }
        }
        return descendants;
      };

      // Get current category from the tree to find its descendants
      const findCategoryInTree = (cats: Category[], targetId: number): Category | null => {
        for (const cat of cats) {
          if (cat.id === targetId) return cat;
          if (cat.categories) {
            const found = findCategoryInTree(cat.categories, targetId);
            if (found) return found;
          }
        }
        return null;
      };

      const currentCategoryInTree = findCategoryInTree(allCategories, category.id);
      if (currentCategoryInTree) {
        const excludeIds = findDescendants(currentCategoryInTree);
        return allFlat.filter(cat => !excludeIds.includes(cat.id));
      }

      // Fallback: at least exclude the current category itself
      return allFlat.filter(cat => cat.id !== category.id);
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

      // Prepare request data with separate icon and color fields
      const requestData = {
        title: data.title,
        url: data.url,
        description: data.description || '',
        parent: data.parent || 0,
        status: data.status,
        locale: data.locale === 'none' ? undefined : data.locale,
        icon: data.icon || undefined,
        color: data.color || undefined,
        data: '', // Keep data field empty or for other metadata
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
        <h3 className="font-semibold mb-4">{t('form.basicInfo')}</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="title">{t('form.title')} *</Label>
            <Input
              id="title"
              {...register('title')}
              placeholder={t('form.titlePlaceholder')}
            />
            {errors.title && (
              <p className="text-sm text-destructive">{errors.title.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="url">{t('form.url')} *</Label>
            <Input
              id="url"
              {...register('url')}
              placeholder={t('form.urlPlaceholder')}
            />
            {errors.url && (
              <p className="text-sm text-destructive">{errors.url.message}</p>
            )}
          </div>

          <div className="space-y-2 md:col-span-2">
            <Label htmlFor="description">{t('form.description')}</Label>
            <Textarea
              id="description"
              {...register('description')}
              placeholder={t('form.descriptionPlaceholder')}
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
        <h3 className="font-semibold mb-4">{t('form.hierarchy')}</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="space-y-2">
            <Label htmlFor="parent">{t('form.parent')}</Label>
            <Select
              value={(watch('parent') ?? 0).toString()}
              onValueChange={(value) => setValue('parent', parseInt(value) || 0)}
            >
              <SelectTrigger>
                <SelectValue placeholder={t('form.parentPlaceholder')} />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="0">{t('form.topLevel')}</SelectItem>
                {availableParents.map((cat) => (
                  <SelectItem key={cat.id} value={cat.id.toString()}>
                    {cat.title} (ID: {cat.id})
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="status">{t('form.status')}</Label>
            <Select
              value={watch('status')?.toString() || '1'}
              onValueChange={(value) => setValue('status', parseInt(value))}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="1">{t('active')}</SelectItem>
                <SelectItem value="0">{t('inactive')}</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="locale">{t('form.locale')}</Label>
            <Select
              value={watch('locale') || 'none'}
              onValueChange={(value) => setValue('locale', value)}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="none">🌍 Worldwide (No Locale)</SelectItem>
                <SelectItem value="en">🇺🇸 English</SelectItem>
                <SelectItem value="ru">🇷🇺 Russian</SelectItem>
                <SelectItem value="zh">🇨🇳 Chinese</SelectItem>
                <SelectItem value="es">🇪🇸 Spanish</SelectItem>
                <SelectItem value="ar">🇸🇦 Arabic</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </Box>

      {/* Visual Customization */}
      <Box size="default">
        <h3 className="font-semibold mb-4">{t('form.customization')}</h3>
        <div className="space-y-4">
          {/* Color Selection */}
          <div className="space-y-2">
            <Label>{t('form.color')}</Label>
            <div className="flex flex-wrap gap-2">
              {/* No Color Option */}
              <button
                type="button"
                className={`w-8 h-8 rounded-full border-2 bg-muted flex items-center justify-center ${!watchedColor ? 'border-foreground' : 'border-border'
                  }`}
                onClick={() => setValue('color', '')}
                title={t('form.noColor')}
              >
                <span className="text-xs text-muted-foreground">×</span>
              </button>
              {DEFAULT_COLORS.map((color) => (
                <button
                  key={color}
                  type="button"
                  className={`w-8 h-8 rounded-full border-2 ${watchedColor === color ? 'border-foreground' : 'border-border'
                    }`}
                  style={{ backgroundColor: color }}
                  onClick={() => setValue('color', color)}
                />
              ))}
            </div>
            <Input
              {...register('color')}
              placeholder={t('form.colorPlaceholder')}
              className="w-32"
            />
          </div>

          {/* Icon Selection */}
          <div className="space-y-2">
            <Label>{t('form.icon')}</Label>
            <Input
              {...register('icon')}
              placeholder={t('form.iconPlaceholder')}
              className="w-48"
            />
            <p className="text-xs text-muted-foreground">
              {t('form.iconDescription')}
              <br />
              <a
                href="https://fontawesome.com/search?s=solid&ic=free&o=r"
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary hover:underline"
              >
                {t('form.browseIcons')} →
              </a>
            </p>
          </div>

          {/* Image Upload */}
          <div className="space-y-2">
            <Label>{t('form.image')}</Label>
            <div className={`rounded-[0.75rem] relative overflow-hidden w-full h-[120px] ${!imagePreview ? 'border-2 border-dashed border-border' : ''}`}>
              <input
                type="file"
                accept="image/*"
                onChange={handleImageChange}
                className="hidden"
                id="imageUpload"
              />
              <Label htmlFor="imageUpload" className="cursor-pointer block w-full h-full">
                {imagePreview ? (
                  <div className="relative w-full h-full">
                    <Image
                      src={imagePreview}
                      alt="Category preview"
                      width={400}
                      height={120}
                      className="w-full h-full object-cover object-center"
                    />
                    <div className="absolute inset-0 bg-black/50 opacity-0 hover:opacity-100 transition-opacity flex items-center justify-center">
                      <div className="text-white text-sm text-center">
                        <UploadIcon size={20} className="mx-auto mb-1" />
                        <div>{t('form.imageUpload')}</div>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="w-full h-full flex flex-col items-center justify-center text-center">
                    <UploadIcon size={24} className="text-muted-foreground mb-2" />
                    <span className="text-sm text-muted-foreground">{t('form.imageUpload')}</span>
                  </div>
                )}
              </Label>
              {imagePreview && (
                <IconButton
                  type="button"
                  variant="destructive"
                  size="sm"
                  className="absolute -top-2 -right-2 z-10"
                  onClick={removeImage}
                  icon={<XIcon size={12} />}
                >
                </IconButton>
              )}
            </div>
          </div>
        </div>
      </Box>

      {/* Preview */}
      {watchedTitle && (
        <Box size="default">
          <h3 className="font-semibold mb-4">{t('form.preview')}</h3>
          <div className="border rounded-[0.75rem] bg-background">
            <CategoryPreview
              category={{
                id: category?.id,
                title: watchedTitle || 'Category Title',
                url: watchedUrl || 'category-url',
                description: watchedDescription,
                image: imagePreview || category?.image,
                status: watchedStatus,
                icon: watchedIcon,
                color: watchedColor,
              }}
              showDescription={false}
              showCreated={false}
              showSubcategoriesCount={false}
            />
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
          {t('form.cancel')}
        </Button>
        <IconButton
          type="submit"
          variant="default"
          disabled={isLoading}
          icon={<SaveIcon size={16} />}
          responsive
        >
          {isLoading ? t('form.saving') : category ? t('form.updateCategory') : t('form.createCategory')}
        </IconButton>
      </div>
    </form>
  );
}
