import "./globals.css";

//metadata without typescript
export const metadata = {
  title: "Scanner de vulnérabilités",
  description: "Scanner de vulnérabilités automatiques d'applications web",
  lang: "en",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        {children}
      </body>
    </html>
  );
}
