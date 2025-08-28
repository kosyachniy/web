import * as React from "react"

import { cn } from "@/shared/lib/utils"

const Textarea = React.forwardRef<HTMLTextAreaElement, React.ComponentProps<"textarea">>(
  (allProps, ref) => {
    const { className, value, ...props } = allProps;
    const hasValueProp = Object.prototype.hasOwnProperty.call(allProps, 'value');
    const isControlledRef = React.useRef(hasValueProp);

    // Once controlled, always controlled; once uncontrolled, always uncontrolled
    if (hasValueProp) {
      isControlledRef.current = true;
    }

    return (
      <textarea
        data-slot="textarea"
        className={cn(
          "placeholder:text-muted-foreground selection:bg-primary selection:text-primary-foreground bg-muted/50 dark:bg-input/30 flex w-full min-w-0 rounded-[0.75rem] px-3 py-2 text-base shadow-xs transition-[color,box-shadow] outline-none focus:outline-none active:outline-none disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 md:text-sm min-h-[60px] resize-y",
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

Textarea.displayName = "Textarea"

export { Textarea }