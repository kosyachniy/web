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
      <path d="M6 2C4.9 2 4 2.9 4 4v4c0 1.1.9 2 2 2s2-.9 2-2c0 1.1.9 2 2 2s2-.9 2-2V4c0-1.1-.9-2-2-2s-2 .9-2 2c0-1.1-.9-2-2-2z" />
      <path d="M18 2c-1.1 0-2 .9-2 2v4c0 1.1.9 2 2 2s2-.9 2-2c0 1.1.9 2 2 2s2-.9 2-2V4c0-1.1-.9-2-2-2s-2 .9-2 2c0-1.1-.9-2-2-2z" />
    </svg>
  )
}