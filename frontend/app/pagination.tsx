import Link from "next/link";
import {
  getPaginationModel,
  ITEM_TYPES,
  type PaginationModelItem,
} from "ultimate-pagination";

const ARROWS: Record<string, string> = {
  [ITEM_TYPES.PREVIOUS_PAGE_LINK]: "<",
  [ITEM_TYPES.NEXT_PAGE_LINK]: ">",
};

function renderItem(item: PaginationModelItem) {
  if (item.type === ITEM_TYPES.ELLIPSIS) {
    return (
      <span key={item.key} className="ellipsis">
        …
      </span>
    );
  }

  if (item.type === ITEM_TYPES.PAGE) {
    return item.isActive ? (
      <span key={item.key} className="active">
        {item.value}
      </span>
    ) : (
      <Link key={item.key} href={`/?page=${item.value}`}>
        {item.value}
      </Link>
    );
  }

  const arrow = ARROWS[item.type];
  return item.isActive ? (
    <span key={item.key} className="disabled">
      {arrow}
    </span>
  ) : (
    <Link key={item.key} href={`/?page=${item.value}`}>
      {arrow}
    </Link>
  );
}

type Props = {
  currentPage: number;
  totalPages: number;
};

export default function Pagination({ currentPage, totalPages }: Props) {
  if (totalPages <= 1) return null;

  const items = getPaginationModel({
    currentPage,
    totalPages,
    boundaryPagesRange: 1,
    siblingPagesRange: 1,
    hideFirstAndLastPageLinks: true,
  });

  return <nav className="pagination">{items.map(renderItem)}</nav>;
}
