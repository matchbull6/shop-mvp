export type Product = {
  id: number;
  name: string;
  image_url: string;
};

export type ProductPage = {
  items: Product[];
  total: number;
};

export async function fetchProducts(
  limit: number,
  offset: number,
): Promise<ProductPage> {
  const url = `${process.env.API_URL}/api/products?limit=${limit}&offset=${offset}`;
  const response = await fetch(url, { cache: "no-store" });
  if (!response.ok) throw new Error(`Бэкенд ответил ${response.status}`);
  return response.json();
}
