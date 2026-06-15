import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Argus AI — Insider Threat Intelligence",
  description: "Privacy-Preserving Digital Employee Twins for Continuous Insider Threat Detection in Banking Environments",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
