import React from "react";
import { Container, Typography, Box } from "@material-ui/core";

import Graph from "./Graph";

const Connections = () => {
  return (
    <Container style={{ height: "calc(100vh - 64px)" }}>
      <Box display="flex" height="100%" flexDirection="column">
        <Box py={2}>
          <Typography>
            An overall look at candidate interconnectedness. Every candidate
            with at least one connection is displayed, with gray lines denoting
            shared contributors.
          </Typography>
        </Box>
        <Graph />
      </Box>
    </Container>
  );
};

export default Connections;
