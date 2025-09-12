'use client';

import { useState } from 'react';
import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import { Box } from '@/shared/ui/box';
import { PageHeader } from '@/shared/ui/page-header';
import { WindowIcon } from '@/shared/ui/icons';
import { usePopupActions } from '@/widgets/feedback-system';

export default function PopupDemo() {
    const [customInput, setCustomInput] = useState('');
    const { alert, confirm, confirmDelete, success, error, show, close } = usePopupActions();

    const handleAlert = async () => {
        await alert({
            title: 'Information',
            message: 'This is a simple alert popup with an OK button.'
        });
        console.log('Alert closed');
    };

    const handleConfirm = async () => {
        const result = await confirm({
            title: 'Confirmation Required',
            message: 'Do you want to proceed with this action?',
            confirmText: 'Yes, Proceed',
            cancelText: 'Cancel'
        });

        if (result) {
            success('Action confirmed successfully!');
        } else {
            console.log('Action cancelled');
        }
    };

    const handleDelete = async () => {
        const result = await confirmDelete('This action cannot be undone. Are you sure?');

        if (result) {
            success('Item deleted successfully!');
        }
    };

    const handleCustomPopup = () => {
        show({
            title: 'Custom Popup',
            size: 'lg',
            children: (
                <div className="space-y-4">
                    <p className="text-sm text-muted-foreground">
                        This is a custom popup with interactive content.
                    </p>
                    <Input
                        placeholder="Enter some text..."
                        value={customInput}
                        onChange={(e) => setCustomInput(e.target.value)}
                    />
                    <div className="flex gap-2">
                        <Button
                            onClick={() => {
                                if (customInput.trim()) {
                                    success(`You entered: "${customInput}"`);
                                    setCustomInput('');
                                    close();
                                } else {
                                    error('Please enter some text first!');
                                }
                            }}
                        >
                            Submit
                        </Button>
                        <Button variant="outline" onClick={close}>
                            Cancel
                        </Button>
                    </div>
                </div>
            )
        });
    };

    const handleTransparentPopup = () => {
        show({
            title: 'Transparent Background',
            overlay: 'transparent',
            children: (
                <div className="space-y-4">
                    <p className="text-sm text-muted-foreground">
                        This popup has a transparent background. Click outside to close.
                    </p>
                    <Button onClick={close} className="w-full">
                        Close
                    </Button>
                </div>
            )
        });
    };

    const handleFullScreenPopup = () => {
        show({
            title: 'Full Screen Content',
            size: 'full',
            children: (
                <div className="space-y-6">
                    <p className="text-sm text-muted-foreground">
                        This popup takes up most of the screen space, perfect for forms or detailed content.
                    </p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <Input placeholder="Field 1" />
                        <Input placeholder="Field 2" />
                        <Input placeholder="Field 3" />
                        <Input placeholder="Field 4" />
                    </div>
                    <div className="flex justify-end gap-2">
                        <Button variant="outline" onClick={close}>Cancel</Button>
                        <Button onClick={() => { success('Form submitted!'); close(); }}>
                            Save Changes
                        </Button>
                    </div>
                </div>
            )
        });
    };

    return (
        <div className="max-w-2xl mx-auto">
            <PageHeader
                icon={<WindowIcon size={24} />}
                iconClassName="bg-orange-500/15 text-orange-600 dark:bg-orange-500/20 dark:text-orange-400"
                title="Popup System Demo"
                description="Interactive modal dialogs and popup components"
            />

            <Box size="lg">
                <div className="space-y-6">

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <Button onClick={handleAlert} variant="outline">
                            Show Alert
                        </Button>

                        <Button onClick={handleConfirm} variant="outline">
                            Show Confirmation
                        </Button>

                        <Button onClick={handleDelete} variant="destructive">
                            Delete Confirmation
                        </Button>

                        <Button onClick={() => success('This is a success message!')} variant="outline">
                            Success Message
                        </Button>

                        <Button onClick={() => error('This is an error message!')} variant="outline">
                            Error Message
                        </Button>

                        <Button onClick={handleCustomPopup} variant="outline">
                            Custom Popup
                        </Button>

                        <Button onClick={handleTransparentPopup} variant="outline">
                            Transparent Background
                        </Button>

                        <Button onClick={handleFullScreenPopup} variant="outline">
                            Full Screen Popup
                        </Button>
                    </div>
                </div>
            </Box>
        </div>
    );
}
