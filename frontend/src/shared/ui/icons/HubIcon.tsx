import * as React from "react"

interface IconProps extends React.SVGProps<SVGSVGElement> {
  size?: number
}

export function HubIcon({ size = 16, ...props }: IconProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="currentColor"
      {...props}
    >
      <path d="M17 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V5a2 2 0 00-2-2zM9 7h1a1 1 0 110 2H9a1 1 0 110-2zm0 4h1a1 1 0 110 2H9a1 1 0 110-2zm5-4h1a1 1 0 110 2h-1a1 1 0 110-2zm0 4h1a1 1 0 110 2h-1a1 1 0 110-2zm-3 6a1 1 0 00-1-1h-1a1 1 0 00-1 1v2h3v-2zm2 0a1 1 0 011 1v2h2v-4h-3z" />
    </svg>
  )
}