import "./globals.css";
import { Inter } from 'next/font/google';

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

export const metadata = { 
  title: "LegalLens - AI Contract Risk Analyzer",
  description: "Advanced AI-powered contract analysis tool for detecting risks and suggesting improvements using NVIDIA's Nemotron models.",
  keywords: "legal, contract, AI, analysis, risk, NVIDIA, Nemotron, legal tech",
  authors: [{ name: "LegalLens Team" }],
  openGraph: {
    title: "LegalLens - AI Contract Risk Analyzer",
    description: "Advanced AI-powered contract analysis tool for detecting risks and suggesting improvements.",
    type: "website",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "LegalLens - AI Contract Risk Analyzer",
    description: "Advanced AI-powered contract analysis tool for detecting risks and suggesting improvements.",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export const viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: "#0a0a0a",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.variable}>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚖️</text></svg>" />
      </head>
      <body className={`${inter.className} antialiased`}>
        <div className="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)]">
          {children}
        </div>
      </body>
    </html>
  );
}
