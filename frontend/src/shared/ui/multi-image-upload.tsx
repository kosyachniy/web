'use client';

import React, { useState, useCallback, useRef } from 'react';
import { useTranslations } from 'next-intl';
import { ImageUpload } from './image-upload';
import { Button } from './button';
import { IconButton } from './icon-button';
import { Label } from './label';
import { PlusIcon, TrashIcon } from './icons';
import { cn } from '@/shared/lib/utils';

export interface ImageData {
  id: string;
  file?: File;
  url?: string;
  preview?: string;
}

export interface MultiImageUploadProps {
  /**
   * Array of image data objects
   */
  value?: ImageData[];

  /**
   * Callback when images change
   */
  onImagesChange?: (images: ImageData[]) => void;

  /**
   * Maximum number of images allowed
   */
  maxImages?: number;

  /**
   * Custom label for the gallery
   */
  label?: string;

  /**
   * Whether the component is disabled
   */
  disabled?: boolean;


  /**
   * Accepted file types
   */
  accept?: string;

  /**
   * Maximum file size in MB
   */
  maxSize?: number;

  /**
   * Custom class name
   */
  className?: string;

  /**
   * Number of columns in grid (responsive)
   */
  columns?: {
    sm?: number;
    md?: number;
    lg?: number;
    xl?: number;
  };

  /**
   * Whether to show hints and info
   */
  showHints?: boolean;

  /**
   * Error message to display
   */
  error?: string;
}

export function MultiImageUpload({
  value = [],
  onImagesChange,
  maxImages = 10,
  label,
  disabled = false,
  accept = 'image/*',
  maxSize = 5,
  className,
  columns = { sm: 2, md: 3, lg: 4, xl: 5 },
  showHints = true,
  error,
}: MultiImageUploadProps) {
  const t = useTranslations('multiImageUpload');
  const tImageUpload = useTranslations('imageUpload');
  const [isDragOver, setIsDragOver] = useState(false);
  const multiFileInputRef = useRef<HTMLInputElement>(null);

  const generateImageId = useCallback(() => {
    return `img_${Date.now()}_${Math.random().toString(36).slice(2, 11)}`;
  }, []);

  const hasReachedMax = value.length >= maxImages;
  const canAddMore = !hasReachedMax && !disabled;

  const gridCols = cn(
    'grid gap-4',
    {
      [`grid-cols-${columns.sm}`]: columns.sm,
      [`sm:grid-cols-${columns.sm}`]: columns.sm,
      [`md:grid-cols-${columns.md}`]: columns.md,
      [`lg:grid-cols-${columns.lg}`]: columns.lg,
      [`xl:grid-cols-${columns.xl}`]: columns.xl,
    }
  );

  const handleFileValidation = useCallback((file: File): string | null => {
    if (!file.type.startsWith('image/')) {
      return 'Please select a valid image file';
    }

    const maxSizeBytes = maxSize * 1024 * 1024;
    if (file.size > maxSizeBytes) {
      return `File size must be less than ${maxSize}MB`;
    }

    return null;
  }, [maxSize]);

  const processFiles = useCallback((files: FileList) => {
    if (!canAddMore) return;

    const validFiles: ImageData[] = [];
    const remainingSlots = maxImages - value.length;
    const filesToProcess = Math.min(files.length, remainingSlots);

    for (let i = 0; i < filesToProcess; i++) {
      const file = files[i];
      const validationError = handleFileValidation(file);

      if (!validationError) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const preview = e.target?.result as string;
          const imageData: ImageData = {
            id: generateImageId(),
            file,
            preview,
          };

          validFiles.push(imageData);

          // Only call onImagesChange when all files are processed
          if (validFiles.length === filesToProcess) {
            const newImages = [...value, ...validFiles];
            onImagesChange?.(newImages);
          }
        };
        reader.readAsDataURL(file);
      }
    }
  }, [canAddMore, maxImages, value, handleFileValidation, generateImageId, onImagesChange]);

  const handleSingleImageChange = useCallback((index: number, file: File | null, preview: string | null) => {
    if (!file || !preview) return;

    const imageData: ImageData = {
      id: value[index]?.id || generateImageId(),
      file,
      preview,
    };

    const newImages = [...value];
    newImages[index] = imageData;
    onImagesChange?.(newImages);
  }, [value, generateImageId, onImagesChange]);

  const handleAddImageSlot = useCallback((file: File | null, preview: string | null) => {
    if (!file || !preview || !canAddMore) return;

    const imageData: ImageData = {
      id: generateImageId(),
      file,
      preview,
    };

    const newImages = [...value, imageData];
    onImagesChange?.(newImages);
  }, [canAddMore, value, generateImageId, onImagesChange]);

  const handleRemoveImage = useCallback((index: number) => {
    const newImages = value.filter((_, i) => i !== index);
    onImagesChange?.(newImages);
  }, [value, onImagesChange]);

  const handleRemoveAllImages = useCallback(() => {
    onImagesChange?.([]);
  }, [onImagesChange]);

  const handleMultiFileSelect = useCallback(() => {
    if (!canAddMore) return;
    multiFileInputRef.current?.click();
  }, [canAddMore]);

  const handleMultiFileChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      processFiles(files);
    }
    // Reset input value to allow selecting the same files again
    event.target.value = '';
  }, [processFiles]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    if (canAddMore) {
      setIsDragOver(true);
    }
  }, [canAddMore]);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);

    if (!canAddMore) return;

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      processFiles(files);
    }
  }, [canAddMore, processFiles]);

  return (
    <div className={cn('space-y-4', className)}>
      {/* Header */}
      <div className="flex items-center justify-between">
        {label && <Label className="text-base font-medium">{label}</Label>}

        {value.length > 0 && (
          <div className="flex items-center gap-2">
            <span className="text-sm text-muted-foreground">
              {t('imagesSelected', { count: value.length })}
            </span>
            {!disabled && (
              <IconButton
                type="button"
                variant="outline"
                size="sm"
                onClick={handleRemoveAllImages}
                icon={<TrashIcon size={12} />}
                title={t('removeAll')}
              />
            )}
          </div>
        )}
      </div>

      {/* Multi-file input (hidden) */}
      <input
        ref={multiFileInputRef}
        type="file"
        accept={accept}
        multiple
        onChange={handleMultiFileChange}
        className="hidden"
        disabled={disabled}
      />

      {/* Gallery Grid */}
      <div
        className={cn(
          gridCols,
          'min-h-[120px] transition-all duration-200',
          {
            'border-2 border-dashed border-primary rounded-[0.75rem] p-4': isDragOver,
          }
        )}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {/* Existing Images */}
        {value.map((image, index) => (
          <div key={image.id} className="relative group aspect-square">
            <ImageUpload
              value={image.preview || image.url}
              onImageChange={(file, preview) => handleSingleImageChange(index, file, preview)}
              onImageRemove={() => handleRemoveImage(index)}
              disabled={disabled}
              height={120}
              width="w-full h-full"
              accept={accept}
              maxSize={maxSize}
              showHints={false}
              id={`imageUpload_${image.id}`}
              className="h-full"
            />
          </div>
        ))}

        {/* Add More Slot */}
        {canAddMore && (
          <div className="relative aspect-square">
            <ImageUpload
              onImageChange={handleAddImageSlot}
              disabled={disabled}
              height={120}
              width="w-full h-full"
              accept={accept}
              maxSize={maxSize}
              showHints={false}
              id="addMoreImageUpload"
              className="h-full"
            />
          </div>
        )}

        {/* Empty State / Drop Zone */}
        {value.length === 0 && (
          <div className="col-span-full">
            <div
              className={cn(
                'border-2 border-dashed border-border rounded-[0.75rem] p-8',
                'flex flex-col items-center justify-center text-center',
                'transition-colors duration-200',
                {
                  'border-primary bg-primary/5': isDragOver,
                  'cursor-pointer hover:border-primary/50': canAddMore,
                  'opacity-50 cursor-not-allowed': disabled,
                }
              )}
              onClick={canAddMore ? handleMultiFileSelect : undefined}
            >
              <PlusIcon size={48} className="text-muted-foreground mb-4" />
              <div className="space-y-2">
                <p className="text-lg font-medium text-foreground">
                  {t('clickToAddMore')}
                </p>
                <p className="text-sm text-muted-foreground">
                  {t('dropMultipleImages')}
                </p>
                {showHints && (
                  <div className="text-xs text-muted-foreground mt-4 space-y-1">
                    <div>{tImageUpload('supportedFormats')}</div>
                    <div>{tImageUpload('maxSize').replace('5MB', `${maxSize}MB`)}</div>
                    <div>{t('maxImagesReached', { max: maxImages })}</div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Controls */}
      {value.length > 0 && canAddMore && (
        <div className="flex items-center gap-2 pt-2">
          <Button
            type="button"
            variant="outline"
            onClick={handleMultiFileSelect}
            disabled={disabled}
            className="cursor-pointer"
          >
            <PlusIcon size={16} className="mr-2" />
            {t('addMoreRemaining', { remaining: maxImages - value.length })}
          </Button>
        </div>
      )}

      {/* Max Images Warning */}
      {hasReachedMax && (
        <div className="text-sm text-amber-600 bg-amber-50 dark:bg-amber-900/20 dark:text-amber-400 p-3 rounded-[0.75rem]">
          {t('maxImagesReached', { max: maxImages })}
        </div>
      )}

      {/* Error Message */}
      {error && (
        <p className="text-sm text-destructive">{error}</p>
      )}
    </div>
  );
}