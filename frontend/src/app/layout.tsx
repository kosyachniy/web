// The root layout is required and can't be removed
// It is used for default redirects and metadata
// Note: HTML structure is provided by the [locale] layout
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
