import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.scss";
import { AuthProvider } from './context/AuthContext';
import ClientHeaderWrapper from './components/ClientHeaderWrapper'; // Импортируем новый компонент

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Управление дефектами",
  description: "Система управления дефектами на строительных объектах",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ru">
      <body className={inter.className}>
        <AuthProvider>
          <ClientHeaderWrapper /> {/* Используем ClientHeaderWrapper */}
          <main>
            {children}
          </main>
        </AuthProvider>
      </body>
    </html>
  );
}
