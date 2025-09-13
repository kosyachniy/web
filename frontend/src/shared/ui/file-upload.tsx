'use client';

import React, { useState, useCallback } from 'react';
import { useTranslations } from 'next-intl';
import Image from 'next/image';
import { Label } from './label';
import { IconButton } from './icon-button';
import {
  UploadIcon,
  XIcon,
  ImageIcon,
  PdfIcon,
  WordIcon,
  ExcelIcon,
  PowerpointIcon,
  CodeIcon,
  ArchiveIcon,
  FileVideoIcon,
  FileAudioIcon,
  FileIcon
} from './icons';
import { cn } from '@/shared/lib/utils';

// File type definitions
export type FileTypeFilter = 'any' | 'images' | 'documents' | 'media' | 'archives' | string[];

export interface FileData {
  file: File;
  preview?: string;
  type: 'image' | 'pdf' | 'document' | 'excel' | 'powerpoint' | 'video' | 'audio' | 'archive' | 'code' | 'other';
  icon: React.ReactNode;
}

export interface FileUploadProps {
  /**
   * Current file URL or data URL for preview
   */
  value?: string | null;

  /**
   * Current file data object
   */
  fileData?: FileData | null;

  /**
   * Callback when file is selected
   */
  onFileChange?: (file: File | null, preview: string | null, fileData: FileData | null) => void;

  /**
   * Callback when file is removed
   */
  onFileRemove?: () => void;

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
   * File type filter
   */
  fileTypes?: FileTypeFilter;

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

// File type detection utilities
const getFileType = (file: File): FileData['type'] => {
  const { type, name } = file;
  const extension = name.split('.').pop()?.toLowerCase() || '';

  if (type.startsWith('image/')) return 'image';
  if (type === 'application/pdf' || extension === 'pdf') return 'pdf';
  if (type.startsWith('video/') || ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv'].includes(extension)) return 'video';
  if (type.startsWith('audio/') || ['mp3', 'wav', 'ogg', 'aac', 'flac', 'm4a'].includes(extension)) return 'audio';
  if (['zip', 'rar', '7z', 'tar', 'gz', 'bz2', 'xz'].includes(extension)) return 'archive';
  if (['js', 'ts', 'jsx', 'tsx', 'html', 'css', 'scss', 'json', 'xml', 'sql', 'py', 'java', 'cpp', 'c', 'php', 'rb', 'go', 'rs'].includes(extension)) return 'code';

  // Specific Microsoft Office types
  if (['xls', 'xlsx'].includes(extension) || type.includes('sheet')) return 'excel';
  if (['ppt', 'pptx'].includes(extension) || type.includes('presentation')) return 'powerpoint';

  // General document types
  if (['doc', 'docx', 'txt', 'rtf', 'odt'].includes(extension)) return 'document';

  return 'other';
};

const getFileIcon = (fileType: FileData['type'], size: number = 24): React.ReactNode => {
  switch (fileType) {
    case 'image': return <ImageIcon size={size} />;
    case 'pdf': return <PdfIcon size={size} />;
    case 'document': return <WordIcon size={size} />;
    case 'excel': return <ExcelIcon size={size} />;
    case 'powerpoint': return <PowerpointIcon size={size} />;
    case 'video': return <FileVideoIcon size={size} />;
    case 'audio': return <FileAudioIcon size={size} />;
    case 'archive': return <ArchiveIcon size={size} />;
    case 'code': return <CodeIcon size={size} />;
    default: return <FileIcon size={size} />;
  }
};

const getAcceptAttribute = (fileTypes: FileTypeFilter): string => {
  if (fileTypes === 'any') return '*/*';
  if (fileTypes === 'images') return 'image/*';
  if (fileTypes === 'documents') return '.doc,.docx,.pdf,.txt,.rtf,.odt';
  if (fileTypes === 'media') return 'video/*,audio/*';
  if (fileTypes === 'archives') return '.zip,.rar,.7z,.tar,.gz,.bz2';
  if (Array.isArray(fileTypes)) return fileTypes.join(',');
  return '*/*';
};

const getSupportedFormatsText = (fileTypes: FileTypeFilter, t: (key: string) => string): string => {
  if (fileTypes === 'images') return t('supportedFormats');
  if (fileTypes === 'documents') return 'Supported formats: PDF, DOC, DOCX, TXT';
  if (fileTypes === 'media') return 'Supported formats: MP4, AVI, MP3, WAV';
  if (fileTypes === 'archives') return 'Supported formats: ZIP, RAR, 7Z';
  return 'All file types supported';
};

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

export function FileUpload({
  value,
  fileData,
  onFileChange,
  onFileRemove,
  label,
  disabled = false,
  height = 120,
  width = 'w-full',
  fileTypes = 'any',
  maxSize = 5,
  showHints = true,
  className,
  id = 'fileUpload',
  error,
}: FileUploadProps) {
  const t = useTranslations('fileUpload');
  const [isDragOver, setIsDragOver] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileValidation = useCallback((file: File): string | null => {
    // Check file type restrictions
    if (fileTypes === 'images' && !file.type.startsWith('image/')) {
      return 'Please select an image file';
    }
    if (fileTypes === 'documents') {
      const validDocTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
      const validExtensions = ['pdf', 'doc', 'docx', 'txt'];
      const extension = file.name.split('.').pop()?.toLowerCase() || '';
      if (!validDocTypes.includes(file.type) && !validExtensions.includes(extension)) {
        return 'Please select a document file (PDF, DOC, DOCX, TXT)';
      }
    }

    // Check file size (convert MB to bytes)
    const maxSizeBytes = maxSize * 1024 * 1024;
    if (file.size > maxSizeBytes) {
      return `File size must be less than ${maxSize}MB`;
    }

    return null;
  }, [fileTypes, maxSize]);

  const processFile = useCallback((file: File) => {
    const validationError = handleFileValidation(file);
    if (validationError) {
      console.error(validationError);
      return;
    }

    setIsLoading(true);

    const fileType = getFileType(file);
    const icon = getFileIcon(fileType);

    const newFileData: FileData = {
      file,
      type: fileType,
      icon,
    };

    // For images, create preview
    if (fileType === 'image') {
      const reader = new FileReader();
      reader.onload = (e) => {
        const preview = e.target?.result as string;
        newFileData.preview = preview;
        onFileChange?.(file, preview, newFileData);
        setIsLoading(false);
      };
      reader.onerror = () => {
        console.error('Failed to read file');
        setIsLoading(false);
      };
      reader.readAsDataURL(file);
    } else {
      // For non-images, no preview needed
      onFileChange?.(file, null, newFileData);
      setIsLoading(false);
    }
  }, [handleFileValidation, onFileChange]);

  const handleFileChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      processFile(file);
    }
  }, [processFile]);

  const handleRemoveFile = useCallback((e: React.MouseEvent) => {
    e.stopPropagation();
    onFileRemove?.();
    onFileChange?.(null, null, null);
  }, [onFileChange, onFileRemove]);

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

  const hasFile = Boolean(value || fileData);
  const useFullHeight = width.includes('h-full');
  const containerHeight = useFullHeight ? '' : `h-[${height}px]`;
  const accept = getAcceptAttribute(fileTypes);

  return (
    <div className={cn('space-y-2', className)}>
      {/* Label */}
      {label && <Label>{label}</Label>}

      {/* Upload Area */}
      <div
        className={cn(
          'rounded-[0.75rem] relative overflow-hidden transition-all duration-200 group',
          width,
          containerHeight,
          {
            'border-2 border-dashed border-border hover:border-primary/50': !hasFile && !disabled,
            'border-2 border-dashed border-border': !hasFile && disabled,
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
            'block w-full h-full group',
            disabled ? 'cursor-not-allowed' : 'cursor-pointer'
          )}
        >
          {hasFile ? (
            // File Preview
            <div className="relative w-full h-full">
              {fileData?.type === 'image' && (value || fileData?.preview) ? (
                // Image Preview
                <>
                  <Image
                    src={value || fileData.preview!}
                    alt={t('preview')}
                    width={400}
                    height={useFullHeight ? 400 : height}
                    className="w-full h-full object-cover object-center"
                  />
                  {/* Hover Overlay */}
                  <div className="absolute inset-0 bg-black/50 opacity-0 hover:opacity-100 transition-opacity flex items-center justify-center">
                    <div className="text-white text-sm text-center">
                      <UploadIcon size={20} className="mx-auto mb-1" />
                      <div>{t('changeFile')}</div>
                    </div>
                  </div>
                </>
              ) : (
                // Non-Image File Display
                <div className="w-full h-full flex flex-col items-center justify-center text-center p-3">
                  <div className="bg-muted text-muted-foreground w-16 h-16 rounded-[0.75rem] flex items-center justify-center mb-3">
                    {fileData?.icon || <FileIcon size={32} />}
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm font-medium text-foreground truncate w-20">
                      {fileData?.file.name || 'Unknown file'}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {fileData?.file.size ? formatFileSize(fileData.file.size) : ''}
                    </p>
                  </div>
                  {/* Hover Overlay for non-images */}
                  <div className="absolute inset-0 bg-black/50 opacity-0 hover:opacity-100 transition-opacity flex items-center justify-center">
                    <div className="text-white text-sm text-center">
                      <UploadIcon size={20} className="mx-auto mb-1" />
                      <div>{t('changeFile')}</div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ) : (
            // Upload Placeholder
            <div className={cn(
              'w-full h-full flex flex-col items-center justify-center text-center p-3 transition-colors duration-200',
              isDragOver && 'bg-primary/5',
              !disabled && 'hover:bg-muted/50'
            )}>
              {isLoading ? (
                <div className="flex items-center gap-2">
                  <UploadIcon size={24} className="text-primary animate-pulse" />
                  <span className="text-sm text-primary">{t('uploading')}</span>
                </div>
              ) : (
                <>
                  <UploadIcon size={24} className={cn(
                    "mb-2 transition-colors duration-200",
                    !disabled && "text-muted-foreground group-hover:text-primary"
                  )} />
                  <span className={cn(
                    "text-sm transition-colors duration-200",
                    !disabled && "text-muted-foreground group-hover:text-primary"
                  )}>
                    {t('clickToUpload')}
                  </span>
                  {showHints && (
                    <>
                      <span className="text-xs text-muted-foreground mt-1">
                        {t('dragAndDrop')}
                      </span>
                      <div className="text-xs text-muted-foreground mt-2 space-y-1">
                        <div>{getSupportedFormatsText(fileTypes, t)}</div>
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
        {hasFile && !disabled && (
          <IconButton
            type="button"
            variant="destructive"
            size="sm"
            className="absolute top-1 right-1 z-10 shadow-lg"
            onClick={handleRemoveFile}
            icon={<XIcon size={12} />}
            title={t('removeFile')}
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