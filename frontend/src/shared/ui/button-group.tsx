import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/shared/lib/utils"

const buttonGroupVariants = cva(
  "inline-flex items-center",
  {
    variants: {
      orientation: {
        horizontal: "flex-row [&>*]:rounded-none [&>*:first-child]:rounded-l-[0.75rem] [&>*:last-child]:rounded-r-[0.75rem]",
        vertical: "flex-col [&>*]:rounded-none [&>*:first-child]:rounded-t-[0.75rem] [&>*:last-child]:rounded-b-[0.75rem]"
      },
      size: {
        sm: "[&>*]:h-8 [&>*]:px-3 [&>*]:text-xs",
        default: "[&>*]:h-9 [&>*]:px-4 [&>*]:text-sm",
        lg: "[&>*]:h-10 [&>*]:px-6 [&>*]:text-sm"
      }
    },
    defaultVariants: {
      orientation: "horizontal",
      size: "default",
    },
  }
)

interface ButtonGroupProps 
  extends React.ComponentProps<"div">, 
         VariantProps<typeof buttonGroupVariants> {
}

function ButtonGroup({
  className,
  orientation,
  size,
  children,
  ...props
}: ButtonGroupProps) {
  return (
    <div
      data-slot="button-group"
      className={cn(buttonGroupVariants({ orientation, size }), className)}
      role="group"
      {...props}
    >
      {children}
    </div>
  )
}

export { ButtonGroup, buttonGroupVariants }
export type { ButtonGroupProps }