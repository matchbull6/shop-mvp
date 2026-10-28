"use client";

export default function Error({ reset }: { reset: () => void }) {
  return (
    <main>
      <h1>Каталог</h1>
      <p>Не удалось загрузить товары</p>
      <button onClick={reset}>Повторить</button>
    </main>
  );
}
