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
      },
      variant: {
        default: "bg-primary/10 text-primary",
        posts: "bg-green-500/15 text-green-600 dark:bg-green-500/20 dark:text-green-400",
        space: "bg-purple-500/15 text-purple-600 dark:bg-purple-500/20 dark:text-purple-400", 
        hub: "bg-orange-500/15 text-orange-600 dark:bg-orange-500/20 dark:text-orange-400",
        catalog: "bg-blue-500/15 text-blue-600 dark:bg-blue-500/20 dark:text-blue-400",
        categories: "bg-indigo-500/15 text-indigo-600 dark:bg-indigo-500/20 dark:text-indigo-400",
        demo: "bg-cyan-500/15 text-cyan-600 dark:bg-cyan-500/20 dark:text-cyan-400",
        admin: "bg-red-500/15 text-red-600 dark:bg-red-500/20 dark:text-red-400",
        success: "bg-green-500/15 text-green-600 dark:bg-green-500/20 dark:text-green-400",
        warning: "bg-yellow-500/15 text-yellow-600 dark:bg-yellow-500/20 dark:text-yellow-400",
        info: "bg-blue-500/15 text-blue-600 dark:bg-blue-500/20 dark:text-blue-400",
        destructive: "bg-red-500/15 text-red-600 dark:bg-red-500/20 dark:text-red-400"
      }
    },
    defaultVariants: {
      size: "default",
      variant: "default",
    },
  }
)

interface PageHeaderProps 
  extends React.ComponentProps<"div">, 
         VariantProps<typeof pageHeaderVariants> {
  icon?: React.ReactNode
  iconVariant?: VariantProps<typeof iconContainerVariants>['variant']
  title: string
  description?: string
  actions?: React.ReactNode
}

function PageHeader({
  className,
  size,
  icon,
  iconVariant = "default",
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
          <div className={cn(iconContainerVariants({ size, variant: iconVariant }))}>
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
        <div className="flex items-start gap-2 shrink-0 mt-1">
          {actions}
        </div>
      )}
    </header>
  )
}

export { PageHeader, pageHeaderVariants, iconContainerVariants }
export type { PageHeaderProps }