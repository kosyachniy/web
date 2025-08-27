import * as React from "react"

interface IconProps extends React.SVGProps<SVGSVGElement> {
  size?: number
}

export function PostsIcon({ size = 16, ...props }: IconProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="currentColor"
      {...props}
    >
      <path d="M6 2a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H6zm2 4h8a1 1 0 110 2H8a1 1 0 010-2zm0 4h8a1 1 0 110 2H8a1 1 0 010-2zm0 4h5a1 1 0 110 2H8a1 1 0 010-2z" />
    </svg>
  )
}