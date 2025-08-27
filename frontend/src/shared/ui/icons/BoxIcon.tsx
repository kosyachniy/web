import * as React from "react"

interface IconProps extends React.SVGProps<SVGSVGElement> {
  size?: number
}

export function BoxIcon({ size = 16, ...props }: IconProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="currentColor"
      {...props}
    >
      <path d="M12 2l3 3 3-3v12l-3-3-3 3V2zm8 0h2v2h-2V2zm0 4h2v2h-2V6zm0 4h2v2h-2v-2zm0 4h2v2h-2v-2zm0 4h2v2h-2v-2zM4 2v12l3-3 3 3V2L7 5 4 2z" />
    </svg>
  )
}