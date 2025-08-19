'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import {
    Sheet,
    SheetContent,
    SheetHeader,
    SheetTitle,
    SheetTrigger,
} from '@/components/ui/sheet';
import { Input } from '@/components/ui/input';
import { useTranslations } from 'next-intl';
import ThemeSwitcher from './ThemeSwitcher';
import LanguageSwitcher from './LanguageSwitcher';
import UserProfileDropdown from './UserProfileDropdown';

export default function MobileNavigation() {
    const [isOpen, setIsOpen] = useState(false);
    const t = useTranslations('system');

    return (
        <Sheet open={isOpen} onOpenChange={setIsOpen}>
            <SheetTrigger asChild>
                <Button variant="ghost" size="sm" className="md:hidden">
                    <svg
                        className="h-6 w-6"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M4 6h16M4 12h16M4 18h16"
                        />
                    </svg>
                    <span className="sr-only">Open menu</span>
                </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-80">
                <SheetHeader>
                    <SheetTitle>{t('menu')}</SheetTitle>
                </SheetHeader>
                <div className="flex flex-col space-y-6 mt-6">
                    {/* Search */}
                    <div className="space-y-2">
                        <label className="text-sm font-medium">{t('search')}</label>
                        <Input
                            placeholder={`${t('search')}...`}
                            className="w-full"
                        />
                    </div>

                    {/* User Profile */}
                    <div className="space-y-2">
                        <label className="text-sm font-medium">{t('profile')}</label>
                        <div className="flex justify-start">
                            <UserProfileDropdown />
                        </div>
                    </div>

                    {/* Theme */}
                    <div className="space-y-2">
                        <label className="text-sm font-medium">Theme</label>
                        <div className="flex justify-start">
                            <ThemeSwitcher />
                        </div>
                    </div>

                    {/* Language */}
                    <div className="space-y-2">
                        <label className="text-sm font-medium">{t('locale')}</label>
                        <div className="flex justify-start">
                            <LanguageSwitcher />
                        </div>
                    </div>

                    {/* Quick Actions */}
                    <div className="space-y-2 pt-4 border-t">
                        <Button variant="outline" className="w-full justify-start">
                            <span>🏠</span>
                            <span className="ml-2">{t('main')}</span>
                        </Button>
                        <Button variant="outline" className="w-full justify-start">
                            <span>📊</span>
                            <span className="ml-2">{t('analytics')}</span>
                        </Button>
                        <Button variant="outline" className="w-full justify-start">
                            <span>📁</span>
                            <span className="ml-2">{t('categories')}</span>
                        </Button>
                    </div>
                </div>
            </SheetContent>
        </Sheet>
    );
}
