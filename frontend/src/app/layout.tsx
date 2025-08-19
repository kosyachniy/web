// The root layout is required and can't be removed
// It is used for default redirects and metadata
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
