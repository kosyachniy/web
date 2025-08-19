'use client';

import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useTranslations } from 'next-intl';

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

    const handleProfileClick = () => {
        // Navigate to profile page
        console.log('Navigate to profile');
    };

    const handleSettingsClick = () => {
        // Navigate to settings page
        console.log('Navigate to settings');
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
                    className={className ? `justify-start gap-3 h-12 ${className}` : "relative h-8 w-8 rounded-full"}
                >
                    <Avatar className="h-8 w-8">
                        <AvatarImage src={userAvatar} alt={userName} />
                        <AvatarFallback className="bg-primary text-primary-foreground">
                            {getInitials(userName)}
                        </AvatarFallback>
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
                    <span>👤</span>
                    <span className="ml-2">{t('profile')}</span>
                </DropdownMenuItem>
                <DropdownMenuItem onClick={handleSettingsClick} className="cursor-pointer">
                    <span>⚙️</span>
                    <span className="ml-2">{t('settings')}</span>
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleSignOut} className="cursor-pointer text-red-600 dark:text-red-400">
                    <span>🚪</span>
                    <span className="ml-2">{t('sign_out')}</span>
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
    );
}
