import * as React from "react"

import { cn } from "@/shared/lib/utils"

const Input = React.forwardRef<HTMLInputElement, React.ComponentProps<"input">>(
  (allProps, ref) => {
    const { className, type, value, ...props } = allProps;
    const hasValueProp = Object.prototype.hasOwnProperty.call(allProps, 'value');
    const isControlledRef = React.useRef(hasValueProp);

    // Once controlled, always controlled; once uncontrolled, always uncontrolled
    if (hasValueProp) {
      isControlledRef.current = true;
    }

    return (
      <input
        type={type}
        data-slot="input"
        className={cn(
          "file:text-foreground placeholder:text-muted-foreground selection:bg-primary selection:text-primary-foreground bg-muted/50 dark:bg-input/30 flex h-9 w-full min-w-0 rounded-[0.75rem] px-3 py-1 text-base shadow-xs transition-[color,box-shadow] outline-none focus:outline-none active:outline-none file:inline-flex file:h-7 file:bg-transparent file:text-sm file:font-medium disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 md:text-sm",
          "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40",
          className
        )}
        ref={ref}
        {...props}
        {...(isControlledRef.current && { value: value ?? '' })}
      />
    )
  }
)

Input.displayName = "Input"

export { Input }
