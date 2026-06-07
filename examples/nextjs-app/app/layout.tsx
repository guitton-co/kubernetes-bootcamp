import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "k8s-kata Next.js",
  description: "Hello world Next.js app running on Kubernetes",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
