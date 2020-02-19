import React from "react";
import { Container, Typography } from "@material-ui/core";

const Home = () => {
  return (
    <Container>
      <Typography variant="h1">Project Confero</Typography>
      <Typography>
        Project Confero is an attempt to help voters explore connections between
        candidates for Federal office in the US. Specifically, we've focused on
        the metric of "shared contributors" - that is, people who donated money
        to multiple campaigns.
      </Typography>
    </Container>
  );
};

export default Home;
