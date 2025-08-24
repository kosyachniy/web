'use client';

import { PropsWithChildren } from 'react';
import { ReduxProvider } from './provider';
import { ThemeProvider } from './ThemeProvider';
import { ToastProvider } from '@/widgets/feedback-system';
import { PopupProvider } from '@/widgets/feedback-system';

export const AppProviders = ({ children }: PropsWithChildren) => (
  <ReduxProvider>
    <ThemeProvider>
      <PopupProvider>
        <ToastProvider />
        {children}
      </PopupProvider>
    </ThemeProvider>
  </ReduxProvider>
);

// Export individual providers for flexibility
export { ReduxProvider } from './provider';
export { ThemeProvider } from './ThemeProvider';