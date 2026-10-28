import type { Metadata } from "next";
import "./globals.css";
import TelegramInit from "./telegram-init";

export const metadata: Metadata = {
  title: "Каталог",
};

type Props = {
  children: React.ReactNode;
};

export default function RootLayout({ children }: Props) {
  return (
    <html>
      <body>
        <TelegramInit />
        {children}
      </body>
    </html>
  );
}
