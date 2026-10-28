import { fetchProducts } from "@/lib/api";
import Pagination from "./pagination";

const PAGE_SIZE = 10;

type Props = {
  searchParams: Promise<{ page?: string }>;
};

export default async function CatalogPage({ searchParams }: Props) {
  const { page: rawPage } = await searchParams;
  const page = Math.max(1, Number.parseInt(rawPage ?? "1", 10) || 1);

  const { items: products, total } = await fetchProducts(
    PAGE_SIZE,
    (page - 1) * PAGE_SIZE,
  );
  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  return (
    <main>
      <h1>Каталог</h1>
      <p className="summary">
        Страница {page} из {totalPages} (товаров: {total})
      </p>
      <Pagination currentPage={page} totalPages={totalPages} />
      {products.length === 0 ? (
        <p>Товаров нет</p>
      ) : (
        <ul className="products">
          {products.map((p) => (
            <li key={p.id} className="product">
              <img src={p.image_url} alt={p.name} loading="lazy" />
              <div>{p.name}</div>
            </li>
          ))}
        </ul>
      )}
      <Pagination currentPage={page} totalPages={totalPages} />
    </main>
  );
}
