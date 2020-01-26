import React from "react";
import { Box, Flex, Heading, Text, Divider } from "@theme-ui/components";

import { Candidate, findConnectedCandidates } from "lib/candidate";
import { Connection } from "lib/connection";
import ConnectedCandidate from "./ConnectedCandidate";
import { lookupOffice } from "lib/lookups";

export interface CandidateDetailsProps {
  candidate: Candidate;
  candidates: Candidate[];
  connections: Connection[];
  onSelect: (candidate: Candidate) => void;
}

const CandidateDetails: React.FunctionComponent<CandidateDetailsProps> = ({
  candidate,
  candidates,
  connections,
  onSelect
}) => {
  const connectedCandidates = findConnectedCandidates(
    candidate,
    candidates,
    connections
  );

  return (
    <Flex sx={{ flexDirection: "column" }}>
      <Heading>{candidate.name}</Heading>
      <Text>Running For: {lookupOffice(candidate.office)}</Text>

      <Heading as="h3">Connected Campaigns:</Heading>
      {connectedCandidates.map(props => (
        <Box key={props.candidate.id}>
          <ConnectedCandidate {...props} onSelect={onSelect} />
          <Divider />
        </Box>
      ))}
    </Flex>
  );
};

export default React.memo(CandidateDetails);
