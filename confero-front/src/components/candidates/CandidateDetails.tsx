import React from "react";
import { Box, Typography, List } from "@material-ui/core";

import {
  Candidate,
  findConnectedCandidates,
  candidateName,
  contributionAmount,
  contributions
} from "lib/candidate";
import { Connection } from "lib/connection";
import ConnectedCandidate from "./ConnectedCandidate";
import { fetchInfo } from "lib/wikipedia";

export interface CandidateDetailsProps {
  candidate: Candidate;
  candidates: Candidate[];
  connections: Connection[];
  onSelect: (candidate: Candidate | null) => void;
}

const CandidateDetails: React.FunctionComponent<CandidateDetailsProps> = ({
  candidate,
  candidates,
  connections,
  onSelect
}) => {
  const [extract, setExtract] = React.useState("");

  React.useEffect(() => {
    fetchInfo(candidate.name).then(setExtract);
  }, [candidate]);

  const connectedCandidates = findConnectedCandidates(
    candidate,
    candidates,
    connections
  );

  return (
    <Box p={3}>
      <Typography variant="h3">{candidateName(candidate)}</Typography>
      <Typography>Direct Contributions: {contributions(candidate)}</Typography>
      <Typography>
        Direct Contribution Total: {contributionAmount(candidate)}
      </Typography>

      <Typography>{extract}</Typography>

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
  );
};

export default React.memo(CandidateDetails);
