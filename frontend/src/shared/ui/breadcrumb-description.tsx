import * as React from "react"
import Link from 'next/link'

interface BreadcrumbItem {
  id: number
  title: string
  url: string
  position: number
}

interface BreadcrumbDescriptionProps {
  breadcrumbs: BreadcrumbItem[]
}

export function BreadcrumbDescription({ breadcrumbs }: BreadcrumbDescriptionProps) {
  if (breadcrumbs.length <= 1) return null

  return (
    <span className="flex items-center flex-wrap gap-1">
      {breadcrumbs.slice(0, -1).map((breadcrumb, index) => (
        <React.Fragment key={breadcrumb.id}>
          {index > 0 && <span className="text-muted-foreground/50">/</span>}
          <Link
            href={breadcrumb.url}
            className="text-muted-foreground hover:text-foreground underline decoration-dashed decoration-1 underline-offset-2 transition-colors"
            title={`Go to ${breadcrumb.title}`}
          >
            {breadcrumb.title}
          </Link>
        </React.Fragment>
      ))}
    </span>
  )
}