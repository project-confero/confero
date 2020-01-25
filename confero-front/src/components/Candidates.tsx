import React from "react";
import { Box, Container, Flex, Input } from "@theme-ui/components";

import candidates from "../data/candidates.json";
import { Candidate, candidateName } from "../lib/candidate";
import Link from "./nav/Link";
import Pagination from "./basic/Pagination";

const Candidates = () => {
  const [filter, setFilter] = React.useState("");

  const shownCandidates = React.useMemo(() => {
    const compareFilter = filter.toLowerCase();
    return candidates.filter(candidate =>
      candidate.name.toLowerCase().includes(compareFilter)
    );
  }, [filter]);

  return (
    <Container>
      <Input
        value={filter}
        onChange={event => setFilter(event.target.value)}
        placeholder="Search by name"
      />

      <Pagination size={10} items={shownCandidates}>
        {candidates =>
          candidates.map((candidate: Candidate) => (
            <Flex key={candidate.id}>
              <Link to="/candidates">
                <Box>{candidateName(candidate)}</Box>
              </Link>
            </Flex>
          ))
        }
      </Pagination>
    </Container>
  );
};

export default Candidates;
