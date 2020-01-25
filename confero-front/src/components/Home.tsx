import React from "react";
import { Container, Heading, Text } from "@theme-ui/components";

const Home = () => {
  return (
    <Container>
      <Heading as="h1" mb={2} mt={3}>
        Project Confero
      </Heading>
      <Text>
        Project Confero is an attempt to help voters explore connections between
        candidates for Federal office in the US. Specifically, we've focused on
        the metric of "shared contributors" - that is, people who donated money
        to multiple campaigns.
      </Text>
    </Container>
  );
};

export default Home;
