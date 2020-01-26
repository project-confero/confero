import React from "react";
import { ListItem, ListItemText, ListItemAvatar } from "@material-ui/core";

import { Candidate, candidateName } from "lib/candidate";
import CandidateAvatar from "./CandidateAvatar";

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
    <ListItem button onClick={() => onSelect(candidate)}>
      <ListItemAvatar>
        <CandidateAvatar candidate={candidate} />
      </ListItemAvatar>
      <ListItemText
        primary={candidateName(candidate)}
        secondary={`Shared Contributors: ${score}`}
      />
    </ListItem>
  );
};

export default ConnectedCandidate;
