import React from "react";
import { Container, Typography, Box } from "@material-ui/core";

import Graph from "./Graph";
import candidates from "data/candidates.json";
import connections from "data/connections.json";

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
        <Graph candidates={candidates} connections={connections} />
      </Box>
    </Container>
  );
};

export default Connections;
