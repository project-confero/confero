import React from "react";
import { Box, Flex } from "@theme-ui/components";

import NavLink from "./NavLink";

const Navbar = () => {
  return (
    <Flex sx={{ px: 2, bg: "black", alignItems: "center" }} color="white">
      <NavLink to="/" p={2}>
        Confero
      </NavLink>

      <Box sx={{ mx: "auto" }} />
      <NavLink p={2} to="/candidates">
        Candidates
      </NavLink>
      <NavLink p={2} to="/connections">
        Connections
      </NavLink>
    </Flex>
  );
};

export default Navbar;
