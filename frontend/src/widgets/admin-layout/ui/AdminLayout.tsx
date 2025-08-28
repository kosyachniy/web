'use client';

import { ReactNode } from 'react';
import AdminSidebar from './AdminSidebar';

interface AdminLayoutProps {
  children: ReactNode;
  className?: string;
}

export default function AdminLayout({ children, className }: AdminLayoutProps) {
  return (
    <div className={`min-h-screen bg-background ${className}`}>
      <div className="container mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-20">
              <AdminSidebar />
            </div>
          </div>
          
          {/* Main Content */}
          <div className="lg:col-span-3">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}