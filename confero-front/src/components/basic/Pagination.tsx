import React from "react";
import { clamp } from "lodash";
import { Box, Button, Flex } from "@theme-ui/components";

export interface PaginationProps<T> {
  items: T[];
  size: number;
  children: (items: T[]) => React.ReactNode;
}

function Pagination<T extends { id: unknown }>({
  items,
  size = 10,
  children: renderItems
}: PaginationProps<T>) {
  const [page, setPage] = React.useState(0);

  const lastPage = Math.floor(items.length / size);

  const clampPage = (value: number) => {
    const validValue = clamp(value, 0, lastPage);
    setPage(validValue);
  };

  const filteredItems = React.useMemo(() => {
    return items.slice(page * size, (page + 1) * size);
  }, [items, size, page]);

  return (
    <Box>
      {renderItems(filteredItems)}

      <Flex sx={{ justifyContent: "space-between", alignItems: "center" }}>
        <Button onClick={() => clampPage(page - 1)}>Prev</Button>
        {page > 0 && <Button onClick={() => setPage(0)}>1</Button>}
        <Button>{page + 1}</Button>
        {page < lastPage && (
          <Button onClick={() => setPage(lastPage)}>{lastPage + 1}</Button>
        )}
        <Button onClick={() => clampPage(page + 1)}>Next</Button>
      </Flex>
    </Box>
  );
}

export default Pagination;
