'use client'

import { Button } from '@/shared/ui/button'
import { Box } from '@/shared/ui/box'
import { PageHeader } from '@/shared/ui/page-header'
import { CalculatorIcon } from '@/shared/ui/icons'
import { useAppDispatch, useAppSelector } from '@/shared/stores/store'
import { increment, decrement, incrementByAmount, reset } from '../stores/counterSlice'
import { useTranslations } from 'next-intl'

export function CounterDemo() {
    const t = useTranslations('counter')
    const count = useAppSelector((state) => state.counter.value)
    const dispatch = useAppDispatch()

    return (
        <div className="max-w-2xl mx-auto">
            <PageHeader
                icon={<CalculatorIcon size={24} />}
                iconClassName="bg-indigo-500/15 text-indigo-600 dark:bg-indigo-500/20 dark:text-indigo-400"
                title={t('title')}
                description={t('description')}
            />

            <Box size="lg">
                <div className="space-y-6">
                    <div className="text-center">
                        <div className="text-6xl font-bold text-primary mb-6">
                            {count}
                        </div>
                    </div>

                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                        <Button
                            onClick={() => dispatch(increment())}
                            variant="default"
                            className="w-full"
                        >
                            {t('increment')}
                        </Button>

                        <Button
                            onClick={() => dispatch(decrement())}
                            variant="outline"
                            className="w-full"
                        >
                            {t('decrement')}
                        </Button>

                        <Button
                            onClick={() => dispatch(incrementByAmount(5))}
                            variant="secondary"
                            className="w-full"
                        >
                            {t('incrementBy5')}
                        </Button>

                        <Button
                            onClick={() => dispatch(reset())}
                            variant="destructive"
                            className="w-full"
                        >
                            {t('reset')}
                        </Button>
                    </div>
                </div>
            </Box>
        </div>
    )
}
