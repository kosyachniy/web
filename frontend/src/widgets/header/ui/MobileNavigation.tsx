'use client';

import { Button } from '@/shared/ui/button';
import { MenuIcon, CloseIcon } from '@/shared/ui/icons';

interface MobileNavigationProps {
    isOpen: boolean;
    onToggle: () => void;
}

export default function MobileNavigation({ isOpen, onToggle }: MobileNavigationProps) {
    return (
        <Button variant="ghost" size="sm" onClick={onToggle}>
            {isOpen ? <CloseIcon size={24} /> : <MenuIcon size={24} />}
            <span className="sr-only">{isOpen ? 'Close menu' : 'Open menu'}</span>
        </Button>
    );
}
