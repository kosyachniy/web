'use client';

import { Avatar, AvatarFallback, AvatarImage } from '@/shared/ui/avatar';
import { Button } from '@/shared/ui/button';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/shared/ui/dropdown-menu';
import { UserIcon, SettingsIcon, CreditCardIcon, ChartIcon, ShieldIcon, LogoutIcon } from '@/shared/ui/icons';
import { useTranslations } from 'next-intl';
import { useRouter } from '@/i18n/routing';

interface UserProfileDropdownProps {
    userName?: string;
    userAvatar?: string;
    userEmail?: string;
    className?: string;
}

export default function UserProfileDropdown({
    userName = "John Doe",
    userAvatar,
    userEmail = "john@example.com",
    className
}: UserProfileDropdownProps) {
    const t = useTranslations('system');
    const router = useRouter();

    const handleProfileClick = () => {
        // Navigate to profile page
        console.log('Navigate to profile');
    };

    const handleSettingsClick = () => {
        // Navigate to settings page
        console.log('Navigate to settings');
    };

    const handleBillingClick = () => {
        // Navigate to billing page
        console.log('Navigate to billing');
    };

    const handleAnalyticsClick = () => {
        // Navigate to analytics page
        console.log('Navigate to analytics');
    };

    const handleAdminClick = () => {
        router.push('/admin');
    };

    const handleSignOut = () => {
        // Handle sign out logic
        console.log('Sign out');
    };

    // Get user initials for avatar fallback
    const getInitials = (name: string) => {
        return name
            .split(' ')
            .map(part => part.charAt(0))
            .join('')
            .toUpperCase()
            .slice(0, 2);
    };

    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button
                    variant="outline"
                    className={className ? `justify-start gap-3 h-12 ${className}` : "relative h-8 w-8 rounded-[0.75rem]"}
                >
                    <Avatar className="h-8 w-8">
                        {userAvatar && <AvatarImage src={userAvatar} alt={userName} />}
                        {userAvatar ? (
                            <AvatarFallback className="bg-primary text-primary-foreground">
                                {getInitials(userName)}
                            </AvatarFallback>
                        ) : (
                            <AvatarFallback />
                        )}
                    </Avatar>
                    {className && <span>{userName}</span>}
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="w-56" align="end" forceMount>
                <div className="flex items-center justify-start gap-2 p-2">
                    <div className="flex flex-col space-y-1 leading-none">
                        <p className="font-medium">{userName}</p>
                        <p className="w-[200px] truncate text-sm text-muted-foreground">
                            {userEmail}
                        </p>
                    </div>
                </div>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleProfileClick} className="cursor-pointer">
                    <UserIcon size={16} />
                    <span className="ml-2">{t('profile')}</span>
                </DropdownMenuItem>
                <DropdownMenuItem onClick={handleSettingsClick} className="cursor-pointer">
                    <SettingsIcon size={16} />
                    <span className="ml-2">{t('settings')}</span>
                </DropdownMenuItem>
                <DropdownMenuItem onClick={handleBillingClick} className="cursor-pointer">
                    <CreditCardIcon size={16} />
                    <span className="ml-2">{t('billing')}</span>
                </DropdownMenuItem>
                <DropdownMenuItem onClick={handleAnalyticsClick} className="cursor-pointer">
                    <ChartIcon size={16} />
                    <span className="ml-2">{t('analytics')}</span>
                </DropdownMenuItem>
                <DropdownMenuItem onClick={handleAdminClick} className="cursor-pointer">
                    <ShieldIcon size={16} />
                    <span className="ml-2">{t('admin_panel')}</span>
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleSignOut} className="cursor-pointer text-red-600 dark:text-red-400">
                    <LogoutIcon size={16} />
                    <span className="ml-2">{t('sign_out')}</span>
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
    );
}
