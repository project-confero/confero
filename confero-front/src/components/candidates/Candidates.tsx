import React from "react";
import { Box, Container, Flex, Input, Button } from "@theme-ui/components";

import candidates from "data/candidates.json";
import connections from "data/connections.json";
import { Candidate, candidateName } from "lib/candidate";
import Pagination from "../basic/Pagination";
import CandidateDetails from "./CandidateDetails";

const Candidates = () => {
  const [filter, setFilter] = React.useState("");
  const [
    selectedCandidate,
    setSelectedCandidate
  ] = React.useState<Candidate | null>(null);

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

      <Flex>
        <Pagination size={10} items={shownCandidates}>
          {candidates =>
            candidates.map((candidate: Candidate) => (
              <Flex key={candidate.id}>
                <Button
                  bg="transparent"
                  color="text"
                  onClick={() => setSelectedCandidate(candidate)}
                >
                  {candidateName(candidate)}
                </Button>
              </Flex>
            ))
          }
        </Pagination>

        <Box sx={{ flexGrow: 1 }} pl={2}>
          {selectedCandidate && (
            <CandidateDetails
              candidate={selectedCandidate}
              candidates={candidates}
              connections={connections}
              onSelect={setSelectedCandidate}
            />
          )}
        </Box>
      </Flex>
    </Container>
  );
};

export default Candidates;
