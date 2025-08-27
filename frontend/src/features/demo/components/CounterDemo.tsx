'use client'

import { Button } from '@/shared/ui/button'
import { Card, CardContent } from '@/shared/ui/card'
import { PageHeader } from '@/shared/ui/page-header'
import { DemoIcon } from '@/shared/ui/icons'
import { useAppDispatch, useAppSelector } from '@/shared/stores/store'
import { increment, decrement, incrementByAmount, reset } from '../stores/counterSlice'
import { useTranslations } from 'next-intl'

export function CounterDemo() {
    const t = useTranslations('counter')
    const count = useAppSelector((state) => state.counter.value)
    const dispatch = useAppDispatch()

    return (
        <div className="w-full max-w-md mx-auto">
            <Card>
                <CardContent>
                    <PageHeader
                        icon={<DemoIcon size={24} />}
                        iconClassName="bg-cyan-500/15 text-cyan-600 dark:bg-cyan-500/20 dark:text-cyan-400"
                        title={t('title')}
                        description={t('description')}
                    />
                    
                    <div className="space-y-4">
                    <div className="text-center">
                        <div className="text-4xl font-bold text-blue-600 mb-4">
                            {count}
                        </div>
                    </div>

                    <div className="flex flex-wrap gap-2 justify-center">
                        <Button
                            onClick={() => dispatch(increment())}
                            variant="default"
                        >
                            {t('increment')}
                        </Button>

                        <Button
                            onClick={() => dispatch(decrement())}
                            variant="outline"
                        >
                            {t('decrement')}
                        </Button>

                        <Button
                            onClick={() => dispatch(incrementByAmount(5))}
                            variant="secondary"
                        >
                            {t('incrementBy5')}
                        </Button>

                        <Button
                            onClick={() => dispatch(reset())}
                            variant="destructive"
                        >
                            {t('reset')}
                        </Button>
                    </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
