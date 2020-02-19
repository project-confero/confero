import React from "react";
import { render } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import Pagination, { PaginationProps } from "./Pagination";

describe("Pagination", () => {
  let props: PaginationProps<string>;

  beforeEach(() => {
    props = {
      items: ["a", "b", "c", "d", "e"],
      size: 2,
      children: items => items.join(", ")
    };
  });

  describe("render integration tests", () => {
    const renderComponent = () => render(<Pagination {...props} />);

    it("renders the first page by default", () => {
      const wrapper = renderComponent();

      expect(wrapper.container).toHaveTextContent("a, b");

      expect(wrapper.container).not.toHaveTextContent("c, d");
    });

    it("renders the second page on next", () => {
      const wrapper = renderComponent();

      userEvent.click(wrapper.queryByText("Next"));

      expect(wrapper.container).not.toHaveTextContent("a, b");
      expect(wrapper.container).toHaveTextContent("c, d");
    });
  });
});
