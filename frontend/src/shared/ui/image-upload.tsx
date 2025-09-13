'use client';

import React, { useState, useCallback } from 'react';
import { useTranslations } from 'next-intl';
import Image from 'next/image';
import { Label } from './label';
import { IconButton } from './icon-button';
import { UploadIcon, XIcon } from './icons';
import { cn } from '@/shared/lib/utils';

export interface ImageUploadProps {
  /**
   * Current image URL or data URL for preview
   */
  value?: string | null;

  /**
   * Callback when image is selected
   */
  onImageChange?: (file: File | null, preview: string | null) => void;

  /**
   * Callback when image is removed
   */
  onImageRemove?: () => void;

  /**
   * Custom label for the upload area
   */
  label?: string;

  /**
   * Whether the component is disabled
   */
  disabled?: boolean;

  /**
   * Custom height for the upload area
   */
  height?: number;

  /**
   * Custom width for the upload area
   */
  width?: string;

  /**
   * Accepted file types
   */
  accept?: string;

  /**
   * Maximum file size in MB
   */
  maxSize?: number;

  /**
   * Whether to show format and size hints
   */
  showHints?: boolean;

  /**
   * Custom class name
   */
  className?: string;

  /**
   * Unique ID for the input element
   */
  id?: string;

  /**
   * Error message to display
   */
  error?: string;
}

export function ImageUpload({
  value,
  onImageChange,
  onImageRemove,
  label,
  disabled = false,
  height = 120,
  width = 'w-full',
  accept = 'image/*',
  maxSize = 5,
  showHints = true,
  className,
  id = 'imageUpload',
  error,
}: ImageUploadProps) {
  const t = useTranslations('imageUpload');
  const [isDragOver, setIsDragOver] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileValidation = useCallback((file: File): string | null => {
    // Check file type
    if (!file.type.startsWith('image/')) {
      return 'Please select a valid image file';
    }

    // Check file size (convert MB to bytes)
    const maxSizeBytes = maxSize * 1024 * 1024;
    if (file.size > maxSizeBytes) {
      return `File size must be less than ${maxSize}MB`;
    }

    return null;
  }, [maxSize]);

  const processFile = useCallback((file: File) => {
    const validationError = handleFileValidation(file);
    if (validationError) {
      console.error(validationError);
      return;
    }

    setIsLoading(true);

    const reader = new FileReader();
    reader.onload = (e) => {
      const preview = e.target?.result as string;
      onImageChange?.(file, preview);
      setIsLoading(false);
    };
    reader.onerror = () => {
      console.error('Failed to read file');
      setIsLoading(false);
    };
    reader.readAsDataURL(file);
  }, [handleFileValidation, onImageChange]);

  const handleFileChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      processFile(file);
    }
  }, [processFile]);

  const handleRemoveImage = useCallback((e: React.MouseEvent) => {
    e.stopPropagation();
    onImageRemove?.();
    onImageChange?.(null, null);
  }, [onImageChange, onImageRemove]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    if (!disabled) {
      setIsDragOver(true);
    }
  }, [disabled]);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);

    if (disabled) return;

    const file = e.dataTransfer.files?.[0];
    if (file) {
      processFile(file);
    }
  }, [disabled, processFile]);

  const hasImage = Boolean(value);
  // Use h-full if width contains h-full, otherwise use fixed height
  const useFullHeight = width.includes('h-full');
  const containerHeight = useFullHeight ? '' : `h-[${height}px]`;

  return (
    <div className={cn('space-y-2', className)}>
      {/* Label */}
      {label && <Label>{label}</Label>}

      {/* Upload Area */}
      <div
        className={cn(
          'rounded-[0.75rem] relative overflow-hidden transition-all duration-200',
          width,
          containerHeight,
          {
            'border-2 border-dashed border-border': !hasImage,
            'border-2 border-dashed border-primary': isDragOver,
            'opacity-50 cursor-not-allowed': disabled,
          }
        )}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {/* Hidden File Input */}
        <input
          type="file"
          accept={accept}
          onChange={handleFileChange}
          className="hidden"
          id={id}
          disabled={disabled}
        />

        {/* Upload Label/Trigger */}
        <Label
          htmlFor={id}
          className={cn(
            'block w-full h-full',
            disabled ? 'cursor-not-allowed' : 'cursor-pointer'
          )}
        >
          {hasImage ? (
            // Image Preview
            <div className="relative w-full h-full">
              <Image
                src={value!}
                alt={t('preview')}
                width={400}
                height={useFullHeight ? 400 : height}
                className="w-full h-full object-cover object-center"
              />
              {/* Hover Overlay */}
              <div className="absolute inset-0 bg-black/50 opacity-0 hover:opacity-100 transition-opacity flex items-center justify-center">
                <div className="text-white text-sm text-center">
                  <UploadIcon size={20} className="mx-auto mb-1" />
                  <div>{t('changeImage')}</div>
                </div>
              </div>
            </div>
          ) : (
            // Upload Placeholder
            <div className={cn(
              'w-full h-full flex flex-col items-center justify-center text-center p-3',
              isDragOver && 'bg-primary/5'
            )}>
              {isLoading ? (
                <div className="flex items-center gap-2">
                  <UploadIcon size={24} className="text-primary animate-pulse" />
                  <span className="text-sm text-primary">{t('uploading')}</span>
                </div>
              ) : (
                <>
                  <UploadIcon size={24} className="text-muted-foreground mb-2" />
                  <span className="text-sm text-muted-foreground">
                    {t('clickToUpload')}
                  </span>
                  {showHints && (
                    <>
                      <span className="text-xs text-muted-foreground mt-1">
                        {t('dragAndDrop')}
                      </span>
                      <div className="text-xs text-muted-foreground mt-2 space-y-1">
                        <div>{t('supportedFormats')}</div>
                        <div>{t('maxSize').replace('5MB', `${maxSize}MB`)}</div>
                      </div>
                    </>
                  )}
                </>
              )}
            </div>
          )}
        </Label>

        {/* Remove Button */}
        {hasImage && !disabled && (
          <IconButton
            type="button"
            variant="destructive"
            size="sm"
            className="absolute top-1 right-1 z-10 shadow-lg"
            onClick={handleRemoveImage}
            icon={<XIcon size={12} />}
            title={t('removeImage')}
          />
        )}
      </div>

      {/* Error Message */}
      {error && (
        <p className="text-sm text-destructive">{error}</p>
      )}
    </div>
  );
}