import React from "react";
import { AppBar, Toolbar, Typography, Box, Button } from "@material-ui/core";

import Link from "./Link";

const Navbar = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Box flexGrow={1}>
          <Typography variant="h6">
            <Link to="/" color="inherit">
              Project Confero
            </Link>
          </Typography>
        </Box>
        <Link to="/candidates" color="inherit">
          <Button color="inherit">Candidates</Button>
        </Link>
        <Link to="/connections" color="inherit">
          <Button color="inherit">Connections</Button>
        </Link>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
