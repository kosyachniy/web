'use client';

import { CounterDemo, UserDemo } from '@/features/demo';
import { PopupDemo, ToastDemo } from '@/widgets/feedback-system';

export default function Home() {
    return (
        <div className="bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
            <div className="container mx-auto px-4 py-8">
                <div className="grid gap-8 md:grid-cols-1 lg:grid-cols-1 max-w-2xl mx-auto">
                    <CounterDemo />
                    <UserDemo />
                    <PopupDemo />
                    <ToastDemo />
                </div>
            </div>
        </div>
    );
}
