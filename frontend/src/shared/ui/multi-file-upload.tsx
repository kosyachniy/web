'use client';

import React, { useState, useCallback, useRef } from 'react';
import { useTranslations } from 'next-intl';
import { FileUpload, FileData, FileTypeFilter } from './file-upload';

// Re-export types
export type { FileData, FileTypeFilter };
import { Label } from './label';
import { IconButton } from './icon-button';
import { TrashIcon, PlusIcon, ImageIcon, PdfIcon, WordIcon, ExcelIcon, PowerpointIcon, FileVideoIcon, FileAudioIcon, ArchiveIcon, CodeIcon, FileIcon } from './icons';
import { cn } from '@/shared/lib/utils';

export interface MultiFileUploadProps {
  /**
   * Array of file data objects
   */
  value?: FileData[];

  /**
   * Callback when files change
   */
  onFilesChange?: (files: FileData[]) => void;

  /**
   * Maximum number of files allowed
   */
  maxFiles?: number;

  /**
   * Custom label for the gallery
   */
  label?: string;

  /**
   * Whether the component is disabled
   */
  disabled?: boolean;

  /**
   * File type filter
   */
  fileTypes?: FileTypeFilter;

  /**
   * Maximum file size in MB
   */
  maxSize?: number;

  /**
   * Custom class name
   */
  className?: string;

  /**
   * Grid layout configuration
   */
  columns?: {
    sm?: number;
    md?: number;
    lg?: number;
    xl?: number;
  };

  /**
   * Whether to show format and size hints
   */
  showHints?: boolean;

  /**
   * Error message to display
   */
  error?: string;
}

export function MultiFileUpload({
  value = [],
  onFilesChange,
  maxFiles = 10,
  label,
  disabled = false,
  fileTypes = 'any',
  maxSize = 5,
  className,
  columns = { sm: 2, md: 3, lg: 4, xl: 5 },
  showHints = true,
  error,
}: MultiFileUploadProps) {
  const t = useTranslations('multiFileUpload');
  const [isDragOver, setIsDragOver] = useState(false);
  const multiFileInputRef = useRef<HTMLInputElement>(null);


  const hasReachedMax = value.length >= maxFiles;
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

  const processFiles = useCallback((files: FileList) => {
    const newFiles: FileData[] = [];
    const remainingSlots = maxFiles - value.length;
    const filesToProcess = Math.min(files.length, remainingSlots);

    Array.from(files).slice(0, filesToProcess).forEach((file, index) => {
      // File type detection (reusing logic from FileUpload)
      const getFileType = (file: File): FileData['type'] => {
        const { type, name } = file;
        const extension = name.split('.').pop()?.toLowerCase() || '';

        if (type.startsWith('image/')) return 'image';
        if (type === 'application/pdf' || extension === 'pdf') return 'pdf';
        if (type.startsWith('video/') || ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm'].includes(extension)) return 'video';
        if (type.startsWith('audio/') || ['mp3', 'wav', 'ogg', 'aac', 'flac'].includes(extension)) return 'audio';
        if (['zip', 'rar', '7z', 'tar', 'gz', 'bz2'].includes(extension)) return 'archive';
        if (['js', 'ts', 'jsx', 'tsx', 'html', 'css', 'scss', 'json', 'xml', 'sql', 'py', 'java', 'cpp', 'c', 'php'].includes(extension)) return 'code';
        if (['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'rtf', 'odt'].includes(extension)) return 'document';
        return 'other';
      };

      const getFileIcon = (fileType: FileData['type']): React.ReactNode => {
        switch (fileType) {
          case 'image': return <ImageIcon size={24} />;
          case 'pdf': return <PdfIcon size={24} />;
          case 'document': return <WordIcon size={24} />;
          case 'excel': return <ExcelIcon size={24} />;
          case 'powerpoint': return <PowerpointIcon size={24} />;
          case 'video': return <FileVideoIcon size={24} />;
          case 'audio': return <FileAudioIcon size={24} />;
          case 'archive': return <ArchiveIcon size={24} />;
          case 'code': return <CodeIcon size={24} />;
          default: return <FileIcon size={24} />;
        }
      };

      const fileType = getFileType(file);
      const fileData: FileData = {
        file,
        type: fileType,
        icon: getFileIcon(fileType),
      };

      // For images, create preview
      if (fileType === 'image') {
        const reader = new FileReader();
        reader.onload = (e) => {
          fileData.preview = e.target?.result as string;
          newFiles.push(fileData);

          // Update state when all files are processed
          if (newFiles.length === filesToProcess) {
            const updatedFiles = [...value, ...newFiles];
            onFilesChange?.(updatedFiles);
          }
        };
        reader.readAsDataURL(file);
      } else {
        newFiles.push(fileData);

        // Update state when all files are processed (for non-images)
        if (index === filesToProcess - 1 || newFiles.length === filesToProcess) {
          setTimeout(() => {
            const updatedFiles = [...value, ...newFiles.filter(f => f.type !== 'image'), ...newFiles.filter(f => f.type === 'image')];
            onFilesChange?.(updatedFiles);
          }, 0);
        }
      }
    });
  }, [value, maxFiles, onFilesChange]);

  const handleSingleFileChange = useCallback((index: number, file: File | null, _preview: string | null, fileData: FileData | null) => {
    if (!file || !fileData) return;

    const newFiles = [...value];
    newFiles[index] = fileData;
    onFilesChange?.(newFiles);
  }, [value, onFilesChange]);

  const handleAddFileSlot = useCallback((file: File | null, _preview: string | null, fileData: FileData | null) => {
    if (!file || !fileData) return;

    const newFiles = [...value, fileData];
    onFilesChange?.(newFiles);
  }, [value, onFilesChange]);

  const handleRemoveFile = useCallback((index: number) => {
    const newFiles = value.filter((_, i) => i !== index);
    onFilesChange?.(newFiles);
  }, [value, onFilesChange]);

  const handleRemoveAllFiles = useCallback(() => {
    onFilesChange?.([]);
  }, [onFilesChange]);

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
              {t('filesSelected', { count: value.length })}
            </span>
            {!disabled && (
              <IconButton
                type="button"
                variant="outline"
                size="sm"
                onClick={handleRemoveAllFiles}
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
        accept={fileTypes === 'any' ? '*/*' : fileTypes === 'images' ? 'image/*' :
               fileTypes === 'documents' ? '.doc,.docx,.pdf,.txt,.rtf,.odt' :
               fileTypes === 'media' ? 'video/*,audio/*' : '*/*'}
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
        {/* Existing Files */}
        {value.map((fileData, index) => (
          <div key={`${fileData.file.name}_${index}`} className="relative group aspect-square">
            <FileUpload
              value={fileData.preview || null}
              fileData={fileData}
              onFileChange={(file, preview, newFileData) => handleSingleFileChange(index, file, preview, newFileData)}
              onFileRemove={() => handleRemoveFile(index)}
              disabled={disabled}
              height={120}
              width="w-full h-full"
              fileTypes={fileTypes}
              maxSize={maxSize}
              showHints={false}
              id={`fileUpload_${index}`}
              className="h-full"
            />
          </div>
        ))}

        {/* Add More Slot */}
        {canAddMore && (
          <div className="relative aspect-square">
            <FileUpload
              onFileChange={handleAddFileSlot}
              disabled={disabled}
              height={120}
              width="w-full h-full"
              fileTypes={fileTypes}
              maxSize={maxSize}
              showHints={false}
              id="addMoreFileUpload"
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
              <PlusIcon size={48} className={cn(
                "mb-4 transition-colors duration-200",
                canAddMore ? "text-muted-foreground hover:text-primary" : "text-muted-foreground"
              )} />
              <div className="space-y-2">
                <p className={cn(
                  "text-lg font-medium transition-colors duration-200",
                  canAddMore ? "text-foreground hover:text-primary" : "text-foreground"
                )}>
                  {t('clickToAddMore')}
                </p>
                <p className={cn(
                  "text-sm transition-colors duration-200",
                  canAddMore ? "text-muted-foreground hover:text-primary" : "text-muted-foreground"
                )}>
                  {t('dropMultipleFiles')}
                </p>
                {showHints && (
                  <div className="text-xs text-muted-foreground mt-2 space-y-1">
                    <div>{t('selectMultiple')}</div>
                    <div>
                      {hasReachedMax ?
                        t('maxFilesReached', { max: maxFiles }) :
                        t('addMoreRemaining', { remaining: maxFiles - value.length })
                      }
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Additional Upload Button for Non-Empty State */}
        {value.length > 0 && canAddMore && (
          <div className="col-span-full mt-4">
            <button
              onClick={handleMultiFileSelect}
              className={cn(
                'w-full px-4 py-2 border-2 border-dashed border-border rounded-[0.75rem]',
                'flex items-center justify-center gap-2 text-sm text-muted-foreground',
                'hover:border-primary hover:text-primary transition-colors',
                {
                  'opacity-50 cursor-not-allowed': disabled,
                }
              )}
              disabled={disabled}
            >
              <PlusIcon size={16} />
              {hasReachedMax ?
                t('maxFilesReached', { max: maxFiles }) :
                t('addMoreRemaining', { remaining: maxFiles - value.length })
              }
            </button>
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <p className="text-sm text-destructive">{error}</p>
      )}
    </div>
  );
}