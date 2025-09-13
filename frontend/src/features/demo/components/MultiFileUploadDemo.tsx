'use client';

import React, { useState } from 'react';
import { useTranslations } from 'next-intl';
import { MultiFileUpload, FileData } from '@/shared/ui/multi-file-upload';
import { FileUpload } from '@/shared/ui/file-upload';
import { Box } from '@/shared/ui/box';
import { Button } from '@/shared/ui/button';
import { ButtonGroup } from '@/shared/ui/button-group';
import { PageHeader } from '@/shared/ui/page-header';
import { ImageIcon, FilterIcon } from '@/shared/ui/icons';

type FilterType = 'any' | 'images' | 'documents';

export function MultiFileUploadDemo() {
  const t = useTranslations('multiFileUploadDemo');
  const tMultiUpload = useTranslations('multiFileUpload');
  const [files, setFiles] = useState<FileData[]>([]);
  const [singleFile, setSingleFile] = useState<FileData | null>(null);
  const [currentFilter, setCurrentFilter] = useState<FilterType>('any');

  const handleFilesChange = (newFiles: FileData[]) => {
    setFiles(newFiles);
    console.log('Files changed:', newFiles);
  };

  const handleClearAll = () => {
    setFiles([]);
  };

  const handleSingleFileChange = (file: File | null, preview: string | null, fileData: FileData | null) => {
    setSingleFile(fileData);
    console.log('Single file changed:', fileData);
  };

  const getSelectedFilesText = () => {
    const plural = files.length === 1 ? '' : 's';
    return t('selectedFiles', { count: files.length, plural });
  };

  const getFilterButtonVariant = (filter: FilterType) => {
    return currentFilter === filter ? 'default' : 'outline';
  };

  return (
    <div className="max-w-6xl mx-auto">
      <PageHeader
        icon={<ImageIcon size={24} />}
        iconClassName="bg-purple-500/15 text-purple-600 dark:bg-purple-500/20 dark:text-purple-400"
        title={t('title')}
        description={t('description')}
      />

      <div className="space-y-8">
        {/* Filter Selection */}
        <Box size="default">
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <FilterIcon size={16} />
              <h3 className="font-semibold">{t('currentFilter')}</h3>
            </div>
            <ButtonGroup>
              <Button
                variant={getFilterButtonVariant('any')}
                onClick={() => setCurrentFilter('any')}
              >
                {t('anyFileType')}
              </Button>
              <Button
                variant={getFilterButtonVariant('images')}
                onClick={() => setCurrentFilter('images')}
              >
                {t('imagesOnly')}
              </Button>
              <Button
                variant={getFilterButtonVariant('documents')}
                onClick={() => setCurrentFilter('documents')}
              >
                {t('documentsOnly')}
              </Button>
            </ButtonGroup>
          </div>
        </Box>

        {/* Single File Upload Example */}
        <Box size="lg">
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Single File Upload Example</h3>
            <p className="text-sm text-muted-foreground">
              Example of single file upload with current filter: <strong>{currentFilter}</strong>
            </p>

            <FileUpload
              label="Single File Upload"
              fileData={singleFile}
              onFileChange={handleSingleFileChange}
              fileTypes={currentFilter}
              maxSize={5}
            />

            {singleFile && (
              <div className="mt-4 p-3 bg-muted rounded-[0.75rem]">
                <p className="text-sm"><strong>File:</strong> {singleFile.file.name}</p>
                <p className="text-sm"><strong>Type:</strong> {singleFile.type}</p>
                <p className="text-sm"><strong>Size:</strong> {(singleFile.file.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
            )}
          </div>
        </Box>

        {/* Multi File Upload Example */}
        <Box size="lg">
          <div className="space-y-6">
            <MultiFileUpload
              label={tMultiUpload('title')}
              value={files}
              onFilesChange={handleFilesChange}
              maxFiles={8}
              fileTypes={currentFilter}
              maxSize={5}
              columns={{ sm: 2, md: 3, lg: 4, xl: 4 }}
              className="w-full"
            />

            {files.length > 0 && (
              <div className="pt-4 border-t">
                <div className="flex items-center justify-between">
                  <p className="text-sm text-muted-foreground">
                    {getSelectedFilesText()}
                  </p>
                  <Button variant="outline" onClick={handleClearAll}>
                    {t('clearAll')}
                  </Button>
                </div>
              </div>
            )}

            {/* Debug Section */}
            {files.length > 0 && (
              <>
                <hr className="border-border" />
                <div className="space-y-3">
                  <h3 className="font-semibold text-sm text-muted-foreground">{t('debugTitle')}</h3>
                  <pre className="text-xs bg-muted p-3 rounded-[0.75rem] overflow-auto">
                    {JSON.stringify(
                      files.map(file => ({
                        fileName: file.file?.name,
                        fileSize: file.file?.size,
                        fileType: file.type,
                        hasPreview: !!file.preview,
                      })),
                      null,
                      2
                    )}
                  </pre>
                </div>
              </>
            )}
          </div>
        </Box>
      </div>
    </div>
  );
}
