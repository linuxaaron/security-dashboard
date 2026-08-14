import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Security Dashboard",
  description: "Security monitoring and vulnerability intelligence dashboard",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
