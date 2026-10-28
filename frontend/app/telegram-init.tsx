"use client";

import Script from "next/script";

type TelegramWebApp = {
  initData: string;
  ready: () => void;
  expand: () => void;
};

declare global {
  interface Window {
    Telegram?: { WebApp: TelegramWebApp };
  }
}

export default function TelegramInit() {
  return (
    <Script
      src="https://telegram.org/js/telegram-web-app.js"
      strategy="afterInteractive"
      onLoad={() => {
        const webApp = window.Telegram?.WebApp;
        if (!webApp?.initData) return;
        webApp.ready();
        webApp.expand();
      }}
    />
  );
}
