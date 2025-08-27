import * as React from "react"

interface IconProps extends React.SVGProps<SVGSVGElement> {
  size?: number
}

export function RocketIcon({ size = 16, ...props }: IconProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="currentColor"
      {...props}
    >
      <path d="M12 2.5s4.5 2.04 4.5 10.5c0 3-2.5 4.5-4.5 4.5S7.5 16 7.5 13C7.5 4.54 12 2.5 12 2.5zm2 8.5c0-.83-.67-1.5-1.5-1.5S11 10.17 11 11s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5zM3 19c0 1.1.9 2 2 2h2c0-1.5 1.5-1.5 1.5-1.5S10 18 10 16.5c-.83 0-1.5.67-1.5 1.5H5.5c-.28 0-.5-.22-.5-.5s.22-.5.5-.5H8c-.5-.5-1.5-.5-1.5-.5s-.5-1-.5-2.5c-.83 0-1.5.67-1.5 1.5H2.5c-.28 0-.5.22-.5.5s.22.5.5.5H3z" />
    </svg>
  )
}