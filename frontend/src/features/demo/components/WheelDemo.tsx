'use client'

import React, { useState, useRef, useCallback, useMemo } from 'react'
import { useTranslations } from 'next-intl'
import { Box } from '@/shared/ui/box'
import { Button } from '@/shared/ui/button'
import { IconButton } from '@/shared/ui/icon-button'
import { PageHeader } from '@/shared/ui/page-header'
import {
  SpinIcon,
  PrizeIcon,
  RefreshIcon,
  BitcoinIcon,
  EthereumIcon,
  CoinsIcon,
  TrophyIcon,
  GemIcon
} from '@/shared/ui/icons'

interface WheelSegment {
  id: string
  text: string
  color: string
  icon?: React.ReactNode
}

export function WheelDemo() {
  const t = useTranslations('wheelDemo')
  const [isSpinning, setIsSpinning] = useState(false)
  const [result, setResult] = useState<WheelSegment | null>(null)
  const [spinsLeft, setSpinsLeft] = useState(2)
  const [rotation, setRotation] = useState(0)
  const wheelRef = useRef<HTMLDivElement>(null)

  const segments: WheelSegment[] = useMemo(() => [
    { id: 'bitcoin', text: t('segments.bitcoin'), color: '#f7931e', icon: <BitcoinIcon size={14} /> },
    { id: 'ethereum', text: t('segments.ethereum'), color: '#627eea', icon: <EthereumIcon size={14} /> },
    { id: 'shik', text: t('segments.shik'), color: '#ff6b9d', icon: <GemIcon size={14} /> },
    { id: 'limoni', text: t('segments.limoni'), color: '#c77dff', icon: <TrophyIcon size={14} /> },
    { id: 'dizzy', text: t('segments.dizzy'), color: '#90e0ef', icon: <CoinsIcon size={14} /> },
    { id: 'ruble1000', text: t('segments.ruble1000'), color: '#06ffa5', icon: <CoinsIcon size={14} /> },
    { id: 'aravia', text: t('segments.aravia'), color: '#ff9f1c', icon: <GemIcon size={14} /> },
    { id: 'send', text: t('segments.send'), color: '#fb8500', icon: <TrophyIcon size={14} /> },
    { id: 'desy', text: t('segments.desy'), color: '#8ecae6', icon: <CoinsIcon size={14} /> },
    { id: 'ruble500', text: t('segments.ruble500'), color: '#ffbe0b', icon: <CoinsIcon size={14} /> },
    { id: 'shik2', text: t('segments.shik2'), color: '#ff006e', icon: <GemIcon size={14} /> },
    { id: 'desy2', text: t('segments.desy2'), color: '#8338ec', icon: <CoinsIcon size={14} /> }
  ], [t])

  const spinWheel = useCallback(() => {
    if (isSpinning || spinsLeft <= 0) return

    setIsSpinning(true)
    setResult(null)

    // Calculate random rotation (5-8 full rotations plus random segment)
    const fullRotations = Math.floor(Math.random() * 4) + 5 // 5-8 rotations
    const segmentAngle = 360 / segments.length
    const randomSegmentIndex = Math.floor(Math.random() * segments.length)
    const finalRotation = rotation + (fullRotations * 360) + (randomSegmentIndex * segmentAngle) + Math.random() * segmentAngle

    setRotation(finalRotation)

    // Stop spinning after animation
    setTimeout(() => {
      setIsSpinning(false)
      setSpinsLeft(prev => prev - 1)
      setResult(segments[randomSegmentIndex])
    }, 3000)
  }, [isSpinning, spinsLeft, rotation, segments])

  const resetWheel = useCallback(() => {
    setIsSpinning(false)
    setResult(null)
    setSpinsLeft(2)
    setRotation(0)
  }, [])

  const segmentAngle = 360 / segments.length

  return (
    <div className="max-w-4xl mx-auto">
      <PageHeader
        icon={<PrizeIcon size={24} />}
        iconClassName="bg-orange-500/15 text-orange-600 dark:bg-orange-500/20 dark:text-orange-400"
        title={t('title')}
        description={t('description')}
      />

      <div className="space-y-8">
        {/* Main Content */}
        <Box size="lg">
          <div className="space-y-8">
            {/* Header Text */}
            <div className="text-center space-y-4">
              <h2 className="text-2xl md:text-3xl font-bold bg-gradient-to-r from-purple-600 via-pink-600 to-orange-600 bg-clip-text text-transparent">
                {t('subtitle')}
              </h2>
              <p className="text-lg text-muted-foreground">
                {t('firstSpinsText')}
              </p>
              <p className="text-sm text-muted-foreground max-w-2xl mx-auto">
                {t('instructions')}
              </p>
            </div>

            {/* Wheel Container */}
            <div className="flex flex-col lg:flex-row items-center gap-8">
              {/* Spinning Wheel */}
              <div className="flex-1 flex justify-center">
                <div className="relative">
                  {/* Wheel */}
                  <div
                    ref={wheelRef}
                    className={`relative w-80 h-80 rounded-full border-8 border-blue-600 overflow-hidden transition-transform duration-3000 ease-out ${
                      isSpinning ? 'animate-spin' : ''
                    }`}
                    style={{
                      transform: `rotate(${rotation}deg)`,
                      background: 'conic-gradient(from 0deg, #ff6b9d 0deg 30deg, #c77dff 30deg 60deg, #90e0ef 60deg 90deg, #06ffa5 90deg 120deg, #ff9f1c 120deg 150deg, #fb8500 150deg 180deg, #8ecae6 180deg 210deg, #ffbe0b 210deg 240deg, #ff006e 240deg 270deg, #8338ec 270deg 300deg, #f7931e 300deg 330deg, #627eea 330deg 360deg)'
                    }}
                  >
                    {/* Segments */}
                    {segments.map((segment, index) => {
                      const angle = segmentAngle * index
                      return (
                        <div
                          key={segment.id}
                          className="absolute inset-0 flex items-center justify-center text-white font-bold text-xs"
                          style={{
                            transform: `rotate(${angle + segmentAngle / 2}deg)`,
                            transformOrigin: 'center',
                          }}
                        >
                          <div
                            className="flex flex-col items-center gap-1"
                            style={{ transform: 'translateY(-120px) rotate(0deg)' }}
                          >
                            {segment.icon}
                            <span className="text-[10px] drop-shadow-md">{segment.text}</span>
                          </div>
                        </div>
                      )
                    })}
                  </div>

                  {/* Center Circle */}
                  <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-16 h-16 bg-gradient-to-br from-pink-500 to-purple-600 rounded-full shadow-lg flex items-center justify-center">
                    <div className="w-8 h-8 bg-white rounded-full"></div>
                  </div>

                  {/* Pointer */}
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <div className="w-0 h-0 border-l-4 border-r-4 border-b-8 border-l-transparent border-r-transparent border-b-yellow-400"></div>
                  </div>
                </div>
              </div>

              {/* Controls and Results */}
              <div className="flex-1 space-y-6">
                {/* Spin Controls */}
                <div className="text-center space-y-4">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">
                      {spinsLeft > 0 ? t('spinsLeft', { count: spinsLeft }) : t('noSpinsLeft')}
                    </p>
                  </div>

                  <div className="flex flex-col sm:flex-row gap-3 justify-center">
                    <IconButton
                      icon={<SpinIcon size={16} />}
                      onClick={spinWheel}
                      disabled={isSpinning || spinsLeft <= 0}
                      variant="default"
                      size="lg"
                      className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white border-0"
                    >
                      {isSpinning ? t('spinning') : t('spinButton')}
                    </IconButton>

                    <IconButton
                      icon={<RefreshIcon size={16} />}
                      onClick={resetWheel}
                      variant="outline"
                      size="lg"
                      disabled={isSpinning}
                    >
                      {t('reset')}
                    </IconButton>
                  </div>
                </div>

                {/* Result Display */}
                {result && (
                  <Box variant="accent" size="default" className="text-center">
                    <div className="space-y-3">
                      <h3 className="text-lg font-bold text-green-600 dark:text-green-400">
                        {t('congratulations')}
                      </h3>
                      <div className="flex items-center justify-center gap-2">
                        {result.icon}
                        <span className="font-semibold">
                          {t('youWon')} <span style={{ color: result.color }}>{result.text}</span>
                        </span>
                      </div>
                      {spinsLeft > 0 && (
                        <Button
                          onClick={spinWheel}
                          variant="outline"
                          size="sm"
                          disabled={isSpinning}
                        >
                          {t('tryAgain')}
                        </Button>
                      )}
                    </div>
                  </Box>
                )}

                {/* Footer Info */}
                <div className="text-center space-y-2">
                  <p className="text-xs text-muted-foreground">
                    {t('footerText')}
                  </p>
                  <p className="text-xs font-mono text-muted-foreground bg-muted px-2 py-1 rounded-[0.75rem]">
                    {t('footerUrl')}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </Box>
      </div>
    </div>
  )
}