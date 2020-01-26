import React from "react";
import { Avatar, makeStyles, Tooltip } from "@material-ui/core";
import { Candidate } from "lib/candidate";
import { lookupOffice, lookupPartyColor } from "lib/lookups";

const useStyles = makeStyles(() => ({
  avatar: {
    background: ({ party }: Candidate) => lookupPartyColor(party)
  }
}));

export interface CandidateAvatarProps {
  candidate: Candidate;
}

const CandidateAvatar: React.FunctionComponent<CandidateAvatarProps> = ({
  candidate
}) => {
  const classes = useStyles(candidate);

  return (
    <Tooltip title={lookupOffice(candidate.office)}>
      <Avatar className={classes.avatar}>{candidate.office}</Avatar>
    </Tooltip>
  );
};

export default CandidateAvatar;
