import * as React from "react"
import Link from 'next/link'
import { cn } from "@/shared/lib/utils"

interface BreadcrumbItem {
  id: number
  title: string
  url: string
  position: number
}

interface BreadcrumbLinksProps {
  breadcrumbs: BreadcrumbItem[]
  className?: string
  showStructuredData?: boolean
}

export function BreadcrumbLinks({ breadcrumbs, className, showStructuredData = true }: BreadcrumbLinksProps) {
  const structuredData = {
    '@context': 'http://schema.org/',
    '@type': 'BreadcrumbList',
    itemListElement: breadcrumbs.map((item) => ({
      '@type': 'ListItem',
      position: item.position + 1,
      name: item.title,
      item: {
        '@type': 'Thing',
        '@id': item.url,
        name: item.title
      }
    }))
  }

  return (
    <>
      <nav 
        role="navigation"
        aria-label="breadcrumb"
        itemScope
        itemType="http://schema.org/BreadcrumbList"
        className={cn("flex items-center flex-wrap text-sm", className)}
      >
        {breadcrumbs.slice(0, -1).map((breadcrumb) => (
          <span key={breadcrumb.id} className="flex items-center">
            <span
              itemProp="itemListElement"
              itemScope
              itemType="http://schema.org/ListItem"
            >
              <meta content={breadcrumb.position.toString()} itemProp="position" />
              <Link
                href={breadcrumb.url}
                title={breadcrumb.title}
                itemID={breadcrumb.url}
                itemScope
                itemType="http://schema.org/Thing"
                className="text-muted-foreground hover:text-foreground underline decoration-dashed decoration-1 underline-offset-2 transition-colors"
              >
                <span itemProp="name">{breadcrumb.title}</span>
              </Link>
            </span>
            <span className="mx-2 text-muted-foreground/50">/</span>
          </span>
        ))}
        {breadcrumbs.length > 0 && (
          <span className="text-muted-foreground">{breadcrumbs[breadcrumbs.length - 1]?.title}</span>
        )}
      </nav>
      
      {/* Structured data for SEO */}
      {showStructuredData && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(structuredData)
          }}
        />
      )}
    </>
  )
}