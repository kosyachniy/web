"use client"

import * as React from "react"
import * as SliderPrimitive from "@radix-ui/react-slider"
import { cn } from "@/shared/lib/utils"

interface RangeSliderProps extends React.ComponentPropsWithoutRef<typeof SliderPrimitive.Root> {
  controlPoints?: number[]
  formatValue?: (value: number) => string
  showValues?: boolean
}

const RangeSlider = React.forwardRef<
  React.ElementRef<typeof SliderPrimitive.Root>,
  RangeSliderProps
>(({ className, controlPoints = [], formatValue = (v) => v.toString(), showValues = true, ...props }, ref) => {
  const { min = 0, max = 100 } = props
  
  // Calculate positions for control points
  const getPointPosition = (value: number) => {
    return ((value - min) / (max - min)) * 100
  }

  return (
    <div className="space-y-2">
      <div className="relative">
        <SliderPrimitive.Root
          ref={ref}
          className={cn(
            "relative flex w-full touch-none select-none items-center py-2",
            className
          )}
          {...props}
        >
          <SliderPrimitive.Track className="relative h-2 w-full grow overflow-hidden rounded-full bg-secondary">
            <SliderPrimitive.Range className="absolute h-full bg-primary" />
          </SliderPrimitive.Track>
          
          {/* Render control points */}
          {controlPoints.map((point) => (
            <div
              key={point}
              className="absolute top-1/2 w-3 h-3 bg-primary/70 border-2 border-background rounded-full shadow-sm transform -translate-y-1/2 -translate-x-1/2 z-10"
              style={{ left: `${getPointPosition(point)}%` }}
            />
          ))}
          
          {/* Multiple thumbs for range selection */}
          {props.value?.map((_, index) => (
            <SliderPrimitive.Thumb
              key={index}
              className="block h-5 w-5 rounded-full border-2 border-primary bg-background ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 z-20"
            />
          )) || (
            <SliderPrimitive.Thumb className="block h-5 w-5 rounded-full border-2 border-primary bg-background ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 z-20" />
          )}
        </SliderPrimitive.Root>
      </div>
      
      {/* Control points labels */}
      {showValues && controlPoints.length > 0 && (
        <div className="relative">
          {controlPoints.map((point) => (
            <div
              key={point}
              className="absolute text-xs text-muted-foreground transform -translate-x-1/2"
              style={{ left: `${getPointPosition(point)}%` }}
            >
              {formatValue(point)}
            </div>
          ))}
        </div>
      )}
    </div>
  )
})
RangeSlider.displayName = "RangeSlider"

export { RangeSlider }