import React from "react";
import { Box, Typography, Paper, List, Divider } from "@material-ui/core";

import {
  Candidate,
  findConnectedCandidates,
  candidateName,
  contributionAmount,
  contributions
} from "lib/candidate";
import { Connection } from "lib/connection";
import ConnectedCandidate from "./ConnectedCandidate";

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
    <Paper>
      <Box flexDirection="column" p={3}>
        <Typography variant="h3">{candidateName(candidate)}</Typography>
        <Typography>
          Direct Contributions: {contributions(candidate)}
        </Typography>
        <Typography>
          Direct Contribution Total: {contributionAmount(candidate)}
        </Typography>

        <Typography variant="h5">Connected Campaigns:</Typography>
        <List>
          {connectedCandidates.map(props => (
            <ConnectedCandidate
              key={props.candidate.id}
              {...props}
              onSelect={onSelect}
            />
          ))}
        </List>
      </Box>
    </Paper>
  );
};

export default React.memo(CandidateDetails);
