'use client';

import { useState } from 'react';
import { Input } from '@/shared/ui/input';
import { useTranslations } from 'next-intl';
import { ThemeSwitcher } from '@/shared/components/layout';
import LanguageSwitcher from '@/features/navigation/components/LanguageSwitcher';
import { UserProfileDropdown } from '@/widgets/user-profile';
import MobileNavigation from './MobileNavigation';
import MobileMenuContent from './MobileMenuContent';
import DesktopNavigation from './DesktopNavigation';
import { Logo } from '@/shared/components/layout';
import { useRouter } from '@/i18n/routing';
import { SearchIcon } from '@/shared/ui/icons';

export default function Header() {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const t = useTranslations('system');
    const router = useRouter();

    const handleLogoClick = () => {
        router.push('/');
    };

    const handleSearchSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        const query = formData.get('search') as string;
        if (query.trim()) {
            // Handle search logic
            console.log('Search query:', query);
        }
    };

    return (
        <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="w-full px-4 flex h-16 items-center">
                {/* Logo */}
                <div className="mr-6 flex items-center space-x-2 flex-shrink-0 w-24">
                    <button
                        onClick={handleLogoClick}
                        className="flex items-center space-x-2 hover:opacity-80 transition-opacity cursor-pointer"
                    >
                        <Logo />
                    </button>
                </div>

                {/* Desktop Navigation - Visible from small screens up */}
                <div className="hidden sm:flex mr-6">
                    <DesktopNavigation />
                </div>

                {/* Right Section - Full width distribution */}
                <div className="flex flex-1 items-center justify-end space-x-4">
                    {/* Adaptive Search - Hidden on mobile, responsive width */}
                    <div className="hidden sm:flex items-center">
                        <form onSubmit={handleSearchSubmit} className="relative">
                            <Input
                                name="search"
                                placeholder={`${t('search')}...`}
                                className="w-40 xl:w-80 pr-10"
                                title=""
                                autoComplete="off"
                            />
                            <button
                                type="submit"
                                className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                            >
                                <SearchIcon size={16} />
                            </button>
                        </form>
                    </div>

                    {/* Adaptive Controls - Hidden on mobile */}
                    <div className="hidden sm:flex items-center space-x-2">
                        <ThemeSwitcher />
                        <LanguageSwitcher />
                        <UserProfileDropdown />
                    </div>
                </div>

                {/* Mobile Navigation - Visible only on mobile */}
                <div className="sm:hidden">
                    <MobileNavigation
                        isOpen={isMobileMenuOpen}
                        onToggle={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                    />
                </div>
            </div>

            {/* Mobile Menu Content - Only visible on small screens when open */}
            <div className="sm:hidden">
                <MobileMenuContent
                    isOpen={isMobileMenuOpen}
                    onSearchSubmit={handleSearchSubmit}
                    onClose={() => setIsMobileMenuOpen(false)}
                />
            </div>
        </header>
    );
}