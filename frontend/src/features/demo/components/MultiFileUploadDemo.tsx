'use client';

import React, { useState } from 'react';
import { useTranslations } from 'next-intl';
import { MultiFileUpload, FileData } from '@/shared/ui/multi-file-upload';
import { Box } from '@/shared/ui/box';
import { Button } from '@/shared/ui/button';
import { PageHeader } from '@/shared/ui/page-header';
import { ImageIcon } from '@/shared/ui/icons';


export function MultiFileUploadDemo() {
  const t = useTranslations('multiFileUploadDemo');
  const tMultiUpload = useTranslations('multiFileUpload');
  const [files, setFiles] = useState<FileData[]>([]);

  const handleFilesChange = (newFiles: FileData[]) => {
    setFiles(newFiles);
    console.log('Files changed:', newFiles);
  };

  const handleClearAll = () => {
    setFiles([]);
  };


  const getSelectedFilesText = () => {
    const plural = files.length === 1 ? '' : 's';
    return t('selectedFiles', { count: files.length, plural });
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


        {/* Multi File Upload Example */}
        <Box size="lg">
          <div className="space-y-6">
            <MultiFileUpload
              label={tMultiUpload('title')}
              value={files}
              onFilesChange={handleFilesChange}
              maxFiles={8}
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
