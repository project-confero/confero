import React from "react";
import {
  Box,
  Container,
  TextField,
  Typography,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon
} from "@material-ui/core";

import candidates from "data/candidates.json";
import connections from "data/connections.json";
import { Candidate, candidateName } from "lib/candidate";
import { officeOptions, partyOptions } from "lib/lookups";
import Pagination from "../basic/Pagination";
import CandidateDetails from "./CandidateDetails";
import CandidateAvatar from "./CandidateAvatar";
import FilterButtons from "./FilterButtons";

const filterCandidates = (
  candidates: Candidate[],
  textFilter: string,
  officeFilters: string[],
  partyFilters: string[]
): Candidate[] => {
  const compareFilter = textFilter.toLowerCase();
  return candidates.filter(candidate => {
    const matchesText = candidate.name.toLowerCase().includes(compareFilter);
    const matchesOffice =
      officeFilters.length === 0 || officeFilters.includes(candidate.office);
    const matchesParty =
      partyFilters.length === 0 ||
      partyFilters.includes(candidate.party || "") ||
      (partyFilters.includes("OTHER") &&
        candidate.party !== "DEM" &&
        candidate.party !== "REP");

    return matchesText && matchesOffice && matchesParty;
  });
};

const Candidates = () => {
  const [filter, setFilter] = React.useState("");
  const [officeFilters, setOfficeFilters] = React.useState<string[]>([]);
  const [partyFilters, setPartyFilters] = React.useState<string[]>([]);
  const [
    selectedCandidate,
    setSelectedCandidate
  ] = React.useState<Candidate | null>(null);

  const shownCandidates = React.useMemo(
    () => filterCandidates(candidates, filter, officeFilters, partyFilters),
    [filter, officeFilters, partyFilters]
  );

  return (
    <Container>
      <Box my={2}>
        <Typography>
          Looking to see how specific candidates are connected? Trying to figure
          out who to support?
        </Typography>
        <Typography>
          Search for candidates by name, or filter by office, party, and more.
        </Typography>
      </Box>

      <Divider />

      <TextField
        value={filter}
        onChange={event => setFilter(event.target.value)}
        label="Search by name"
        fullWidth
        variant="filled"
      />

      <Box display="flex">
        <FilterButtons
          value={officeFilters}
          options={officeOptions}
          onChange={setOfficeFilters}
        />

        <FilterButtons
          value={partyFilters}
          options={partyOptions}
          onChange={setPartyFilters}
        />
      </Box>

      <Box display="flex">
        <Pagination size={10} items={shownCandidates}>
          {candidates => (
            <List>
              {candidates.map((candidate: Candidate) => (
                <ListItem
                  key={candidate.id}
                  button
                  onClick={() => setSelectedCandidate(candidate)}
                >
                  <ListItemIcon>
                    <CandidateAvatar candidate={candidate} />
                  </ListItemIcon>
                  <ListItemText
                    primary={candidateName(candidate)}
                    secondary={`Connection Score: ${candidate.score}`}
                  />
                </ListItem>
              ))}
            </List>
          )}
        </Pagination>

        <Box flexGrow={1} pl={2}>
          {selectedCandidate && (
            <CandidateDetails
              candidate={selectedCandidate}
              candidates={candidates}
              connections={connections}
              onSelect={setSelectedCandidate}
            />
          )}
        </Box>
      </Box>
    </Container>
  );
};

export default Candidates;
