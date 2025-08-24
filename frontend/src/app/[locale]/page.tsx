'use client';

import { CounterDemo, UserDemo } from '@/features/demo';
import { PopupDemo, ToastDemo } from '@/widgets/feedback-system';
import { useTranslations } from 'next-intl';

export default function Home() {
    const t = useTranslations('home');

    return (
        <div className="bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
            <div className="container mx-auto px-4 py-8">
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-bold text-slate-900 dark:text-slate-100 mb-4">
                        {t('title')}
                    </h1>
                    <p className="text-lg text-slate-600 dark:text-slate-400 mb-8">
                        {t('subtitle')}
                    </p>
                </div>

                {/* Demo Components Section */}
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
