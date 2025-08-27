import * as React from "react"

interface IconProps extends React.SVGProps<SVGSVGElement> {
  size?: number
}

export function SpaceIcon({ size = 16, ...props }: IconProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      {...props}
    >
      <path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l8.57-8.57A4 4 0 118 8.84l-8.59 8.57a2 2 0 002.83 2.83l8.49-8.5a1 1 0 111.41 1.42l-8.49 8.49a4 4 0 01-5.66-5.66l8.59-8.57A6 6 0 0121.44 11.05z" />
    </svg>
  )
}