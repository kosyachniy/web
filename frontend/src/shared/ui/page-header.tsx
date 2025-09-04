import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/shared/lib/utils"

const pageHeaderVariants = cva(
  "w-full flex items-start justify-between gap-4 mb-6",
  {
    variants: {
      size: {
        sm: "mb-4",
        default: "mb-6",
        lg: "mb-8"
      }
    },
    defaultVariants: {
      size: "default",
    },
  }
)

const iconContainerVariants = cva(
  "flex items-center justify-center shrink-0 rounded-[0.75rem] mt-1",
  {
    variants: {
      size: {
        sm: "w-10 h-10 text-sm",
        default: "w-12 h-12 text-base", 
        lg: "w-14 h-14 text-lg"
      }
    },
    defaultVariants: {
      size: "default",
    },
  }
)

interface PageHeaderProps 
  extends React.ComponentProps<"div">, 
         VariantProps<typeof pageHeaderVariants> {
  icon?: React.ReactNode
  iconClassName?: string
  title: string
  description?: React.ReactNode
  actions?: React.ReactNode
}

function PageHeader({
  className,
  size,
  icon,
  iconClassName,
  title,
  description,
  actions,
  ...props
}: PageHeaderProps) {
  return (
    <header
      data-slot="page-header"
      className={cn(pageHeaderVariants({ size }), className)}
      {...props}
    >
      <div className="flex items-start gap-4 flex-1 min-w-0">
        {icon && (
          <div className={cn(iconContainerVariants({ size }), iconClassName)}>
            {icon}
          </div>
        )}
        <div className="flex-1 min-w-0">
          <h1 className="text-2xl font-bold text-foreground mb-0.5 truncate">
            {title}
          </h1>
          {description && (
            <p className="text-muted-foreground text-sm leading-relaxed">
              {description}
            </p>
          )}
        </div>
      </div>
      {actions && (
        <div className="flex items-center gap-2 shrink-0 mt-2.5">
          {actions}
        </div>
      )}
    </header>
  )
}

export { PageHeader, pageHeaderVariants, iconContainerVariants }
export type { PageHeaderProps }