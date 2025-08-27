import * as React from "react"

interface IconProps extends React.SVGProps<SVGSVGElement> {
  size?: number
}

export function ComputerIcon({ size = 16, ...props }: IconProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="currentColor"
      {...props}
    >
      <path d="M21 16H3V4h18m0-2H3c-1.11 0-2 .89-2 2v12c0 1.11.89 2 2 2h7l-2 3v1h8v-1l-2-3h7c1.11 0 2-.89 2-2V4c0-1.11-.89-2-2-2z" />
    </svg>
  )
}