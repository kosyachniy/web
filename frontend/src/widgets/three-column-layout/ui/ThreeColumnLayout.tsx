'use client';

import { ReactNode } from 'react';

interface ThreeColumnLayoutProps {
  leftSidebar?: ReactNode;
  rightSidebar?: ReactNode;
  children: ReactNode;
  className?: string;
  leftSidebarSticky?: boolean;
  rightSidebarSticky?: boolean;
}

export default function ThreeColumnLayout({
  leftSidebar,
  rightSidebar,
  children,
  className,
  leftSidebarSticky = true,
  rightSidebarSticky = true
}: ThreeColumnLayoutProps) {
  return (
    <div className={`min-h-screen bg-background ${className}`}>
      <div className="container mx-auto px-4 py-4">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Sidebar */}
          {leftSidebar && (
            <div className="lg:col-span-3">
              <div className={`${leftSidebarSticky ? 'sticky top-20' : ''} space-y-6`}>
                {leftSidebar}
              </div>
            </div>
          )}
          
          {/* Main Content */}
          <div className={`${
            leftSidebar && rightSidebar 
              ? 'lg:col-span-6' 
              : leftSidebar || rightSidebar 
                ? 'lg:col-span-9'
                : 'lg:col-span-12'
          }`}>
            {children}
          </div>
          
          {/* Right Sidebar */}
          {rightSidebar && (
            <div className="lg:col-span-3">
              <div className={`${rightSidebarSticky ? 'sticky top-20' : ''} space-y-6`}>
                {rightSidebar}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}