import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/shared/lib/utils"

const boxVariants = cva(
  "bg-background shadow-box",
  {
    variants: {
      size: {
        sm: "rounded-[1rem] p-3",
        default: "rounded-[1rem] p-4", 
        lg: "rounded-[1rem] p-6"
      },
      variant: {
        default: "bg-card text-card-foreground",
        muted: "bg-muted/50 text-muted-foreground",
        accent: "bg-accent/50 text-accent-foreground"
      }
    },
    defaultVariants: {
      size: "default",
      variant: "default",
    },
  }
)

interface BoxProps 
  extends React.ComponentProps<"div">, 
         VariantProps<typeof boxVariants> {
}

function Box({
  className,
  size,
  variant,
  ...props
}: BoxProps) {
  return (
    <div
      data-slot="box"
      className={cn(boxVariants({ size, variant }), className)}
      {...props}
    />
  )
}

export { Box, boxVariants }
export type { BoxProps }