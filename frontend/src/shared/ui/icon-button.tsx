import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/shared/lib/utils"

const iconButtonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium transition-all disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 cursor-pointer",
  {
    variants: {
      variant: {
        default:
          "bg-primary text-primary-foreground shadow-xs hover:bg-primary/90",
        destructive:
          "bg-destructive text-white shadow-xs hover:bg-destructive/90 focus-visible:ring-destructive/20 dark:focus-visible:ring-destructive/40 dark:bg-destructive/60",
        outline:
          "bg-muted/50 dark:bg-input/30 shadow-xs hover:bg-accent hover:text-accent-foreground dark:hover:bg-input/50",
        secondary:
          "bg-secondary text-secondary-foreground shadow-xs hover:bg-secondary/80",
        ghost:
          "hover:bg-accent hover:text-accent-foreground dark:hover:bg-accent/50",
        link: "text-primary underline-offset-4 hover:underline",
        success:
          "bg-green-600 text-white shadow-xs hover:bg-green-600/90 focus-visible:ring-green-600/20 dark:focus-visible:ring-green-600/40",
        warning:
          "bg-yellow-600 text-white shadow-xs hover:bg-yellow-600/90 focus-visible:ring-yellow-600/20 dark:focus-visible:ring-yellow-600/40",
        info:
          "bg-blue-600 text-white shadow-xs hover:bg-blue-600/90 focus-visible:ring-blue-600/20 dark:focus-visible:ring-blue-600/40"
      },
      size: {
        default: "h-9 px-4 py-2 has-[>svg]:px-3 rounded-[0.75rem]",
        sm: "h-8 rounded-[0.75rem] gap-1.5 px-3 has-[>svg]:px-2.5",
        lg: "h-10 rounded-[0.75rem] px-6 has-[>svg]:px-4",
        icon: "size-9 rounded-[0.75rem]",
      },
      responsive: {
        true: "xl:gap-2 gap-0 [&_.button-text]:hidden xl:[&_.button-text]:inline",
        false: ""
      }
    },
    defaultVariants: {
      variant: "default",
      size: "default",
      responsive: false,
    },
  }
)

interface IconButtonProps extends React.ComponentProps<"button">, VariantProps<typeof iconButtonVariants> {
  asChild?: boolean
  icon?: React.ReactNode
  children?: React.ReactNode
}

function IconButton({
  className,
  variant,
  size,
  responsive = false,
  asChild = false,
  icon,
  children,
  ...props
}: IconButtonProps) {
  const Comp = asChild ? Slot : "button"

  return (
    <Comp
      data-slot="icon-button"
      className={cn(iconButtonVariants({ variant, size, responsive, className }))}
      {...props}
    >
      {icon && <span className="shrink-0">{icon}</span>}
      {children && <span className={responsive ? "button-text" : ""}>{children}</span>}
    </Comp>
  )
}

export { IconButton, iconButtonVariants }
export type { IconButtonProps }