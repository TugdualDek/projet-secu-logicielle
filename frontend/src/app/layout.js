import React from "react";
import "../styles/globals.css";
import Navbar from "../components/navbar";

import { Exo } from "next/font/google";

const exo = Exo({
  weight: ["400", "500", "600", "700"],
  style: ["normal", "italic"],
  subsets: ["latin"],
});

//metadata without typescript
export const metadata = {
  title: "Scanner de vulnérabilités",
  description: "Scanner de vulnérabilités automatiques d'applications web",
  lang: "fr",
};

export default function RootLayout({ children }) {
  return (
    <html lang="fr">
      <body
        className={`${exo.className} bg-gradient-to-br from-blue-600 to-green-400 text-white min-h-screen`}
      >
        <div className="flex flex-col items-center min-h-screen">
          <Navbar />
          <main className="w-full max-w-6xl px-4 py-8 flex-grow">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
