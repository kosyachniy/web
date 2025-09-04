import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/shared/lib/utils"
import { Box, BoxProps } from "./box"

const sidebarCardVariants = cva(
  "",
  {
    variants: {
      contentSpacing: {
        sm: "space-y-4",
        default: "space-y-6", 
        lg: "space-y-8"
      }
    },
    defaultVariants: {
      contentSpacing: "default",
    },
  }
)

interface SidebarCardProps 
  extends Omit<BoxProps, 'children'>, 
         VariantProps<typeof sidebarCardVariants> {
  title?: string;
  icon?: React.ReactNode;
  children: React.ReactNode;
  contentSpacing?: "sm" | "default" | "lg";
}

function SidebarCard({
  title,
  icon,
  children,
  className,
  contentSpacing = "default",
  size = "default",
  ...props
}: SidebarCardProps) {
  const hasHeader = title || icon;
  
  return (
    <Box
      size={size}
      className={cn("h-fit", className)}
      {...props}
    >
      <div className={cn(sidebarCardVariants({ contentSpacing }))}>
        {hasHeader && (
          <div className="flex items-center gap-2 mb-4">
            {icon && (
              <div className="flex-shrink-0">
                {icon}
              </div>
            )}
            {title && (
              <h3 className="font-semibold text-lg">
                {title}
              </h3>
            )}
          </div>
        )}
        {children}
      </div>
    </Box>
  )
}

export { SidebarCard, sidebarCardVariants }
export type { SidebarCardProps }