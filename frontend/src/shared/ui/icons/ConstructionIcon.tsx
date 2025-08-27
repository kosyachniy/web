import * as React from "react"

interface IconProps extends React.SVGProps<SVGSVGElement> {
  size?: number
}

export function ConstructionIcon({ size = 16, ...props }: IconProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="currentColor"
      {...props}
    >
      <path d="M13.75 9L15 7.75 16.25 9 18 7.25 16.25 5.5 17.5 4.25 16.25 3L15 4.25 13.75 3 12.5 4.25 13.75 5.5 12 7.25 13.75 9zm-3.5 6.5L12 17.25l1.75-1.75L12 13.75 10.25 15.5zm7-7L18 7.75l1.75 1.75 1.25-1.25L18.75 6 20 4.75 18.75 3.5 17.5 4.75 16.25 3.5 15 4.75 16.25 6 14.5 7.75l1.75 1.75zm-13.5.75L2 8.5 3.75 10.25 5 9l1.25 1.25L8 8.5 6.25 6.75 7.5 5.5 6.25 4.25 5 5.5 3.75 4.25 2.5 5.5 3.75 6.75z" />
      <path d="M9.5 16.5l2-2 6.5 6.5-2 2-6.5-6.5zm-2-11L6 4 4 6l1.5 1.5L2 11l7 7 3.5-3.5L11 13l4.5-4.5z" />
    </svg>
  )
}