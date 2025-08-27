import * as React from "react"

interface IconProps extends React.SVGProps<SVGSVGElement> {
  size?: number
}

export function ShoppingIcon({ size = 16, ...props }: IconProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="currentColor"
      {...props}
    >
      <path d="M19 7h-2V6a5 5 0 00-10 0v1H5a1 1 0 00-1 1v11a3 3 0 003 3h10a3 3 0 003-3V8a1 1 0 00-1-1zM9 6a3 3 0 016 0v1H9V6zm8 13a1 1 0 01-1 1H8a1 1 0 01-1-1V9h2v1a1 1 0 102 0V9h2v1a1 1 0 102 0V9h2v10z" />
    </svg>
  )
}