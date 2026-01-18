import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'AI Friend Chat',
  description: 'Chat with your AI friend - a colorful and playful conversational experience',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  )
}
