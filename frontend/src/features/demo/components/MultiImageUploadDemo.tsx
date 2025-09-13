'use client';

import React, { useState } from 'react';
import { useTranslations } from 'next-intl';
import { MultiImageUpload, ImageData } from '@/shared/ui/multi-image-upload';
import { Box } from '@/shared/ui/box';
import { Button } from '@/shared/ui/button';
import { PageHeader } from '@/shared/ui/page-header';
import { ImageIcon } from '@/shared/ui/icons';

export function MultiImageUploadDemo() {
  const t = useTranslations('multiImageUploadDemo');
  const tMultiUpload = useTranslations('multiImageUpload');
  const [images, setImages] = useState<ImageData[]>([]);

  const handleImagesChange = (newImages: ImageData[]) => {
    setImages(newImages);
    console.log('Images changed:', newImages);
  };

  const handleClearAll = () => {
    setImages([]);
  };

  const getSelectedImagesText = () => {
    const plural = images.length === 1 ? '' : 's';
    return t('selectedImages', { count: images.length, plural });
  };

  return (
    <div className="max-w-4xl mx-auto">
      <PageHeader
        icon={<ImageIcon size={24} />}
        iconClassName="bg-purple-500/15 text-purple-600 dark:bg-purple-500/20 dark:text-purple-400"
        title={t('title')}
        description={t('description')}
      />

      <Box size="lg">
        <div className="space-y-6">
          <MultiImageUpload
            label={tMultiUpload('title')}
            value={images}
            onImagesChange={handleImagesChange}
            maxImages={8}
            maxSize={5}
            columns={{ sm: 2, md: 3, lg: 4, xl: 4 }}
            className="w-full"
          />

          {images.length > 0 && (
            <div className="pt-4 border-t">
              <div className="flex items-center justify-between">
                <p className="text-sm text-muted-foreground">
                  {getSelectedImagesText()}
                </p>
                <Button variant="outline" onClick={handleClearAll}>
                  {t('clearAll')}
                </Button>
              </div>
            </div>
          )}

          {/* Debug Section */}
          {images.length > 0 && (
            <>
              <hr className="border-border" />
              <div className="space-y-3">
                <h3 className="font-semibold text-sm text-muted-foreground">{t('debugTitle')}</h3>
                <pre className="text-xs bg-muted p-3 rounded-[0.75rem] overflow-auto">
                  {JSON.stringify(
                    images.map(img => ({
                      id: img.id,
                      fileName: img.file?.name,
                      fileSize: img.file?.size,
                      hasPreview: !!img.preview,
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
  );
}