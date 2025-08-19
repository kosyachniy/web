'use client';

import { Input } from '@/components/ui/input';
import { useTranslations } from 'next-intl';
import ThemeSwitcher from './ThemeSwitcher';
import LanguageSwitcher from './LanguageSwitcher';
import UserProfileDropdown from './UserProfileDropdown';
import MobileNavigation from './MobileNavigation';
import { useRouter } from '@/i18n/routing';

export default function Header() {
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
            <div className="container flex h-16 items-center">
                {/* Logo */}
                <div className="mr-6 flex items-center space-x-2">
                    <button
                        onClick={handleLogoClick}
                        className="flex items-center space-x-2 hover:opacity-80 transition-opacity"
                    >
                        <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
                            <span className="text-primary-foreground font-bold text-lg">F</span>
                        </div>
                        <span className="hidden sm:inline-block font-bold text-lg">
                            Frontend
                        </span>
                    </button>
                </div>

                {/* Desktop Navigation */}
                <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
                    {/* Search - Hidden on mobile */}
                    <div className="hidden md:flex w-full max-w-sm items-center space-x-2">
                        <form onSubmit={handleSearchSubmit} className="relative flex-1">
                            <Input
                                name="search"
                                placeholder={`${t('search')}...`}
                                className="pr-10"
                            />
                            <button
                                type="submit"
                                className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                            >
                                <svg
                                    className="h-4 w-4"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                                    />
                                </svg>
                            </button>
                        </form>
                    </div>

                    {/* Desktop Controls */}
                    <div className="hidden md:flex items-center space-x-2">
                        <ThemeSwitcher />
                        <LanguageSwitcher />
                        <UserProfileDropdown />
                    </div>

                    {/* Mobile Navigation */}
                    <MobileNavigation />
                </div>
            </div>
        </header>
    );
}
