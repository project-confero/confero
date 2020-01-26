import React from "react";
import { Box, Text } from "@theme-ui/components";

import { Candidate, candidateName } from "lib/candidate";
import TextButton from "components/basic/TextButton";

export interface ConnectedCandidateProps {
  candidate: Candidate;
  score: number;
  onSelect: (candidate: Candidate) => void;
}

const ConnectedCandidate: React.FunctionComponent<ConnectedCandidateProps> = ({
  candidate,
  score,
  onSelect
}) => {
  return (
    <TextButton onClick={() => onSelect(candidate)}>
      <Text>{candidateName(candidate)}</Text>
      <Text>Shared Contributors: {score}</Text>
    </TextButton>
  );
};

export default ConnectedCandidate;
