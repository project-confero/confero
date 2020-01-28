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
  ListItemIcon,
  Grid,
  Paper
} from "@material-ui/core";

import candidates from "data/2000/candidates.json";
import connections from "data/2000/connections.json";
import { Candidate, candidateName } from "lib/candidate";
import { officeOptions, partyOptions } from "lib/lookups";
import Pagination from "../basic/Pagination";
import CandidateDetails from "./CandidateDetails";
import CandidateAvatar from "./CandidateAvatar";
import FilterButtons from "./FilterButtons";
import Graph from "components/connections/Graph";

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

      <Box display="flex" flexWrap="wrap">
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

      {/* Candidates */}
      <Grid container spacing={2} wrap="wrap-reverse">
        <Grid item xs={12} md={4}>
          <Pagination size={10} items={shownCandidates}>
            {candidates => (
              <List>
                {candidates.map((candidate: Candidate) => {
                  const isSelected = candidate.id === selectedCandidate?.id;
                  return (
                    <ListItem
                      key={candidate.id}
                      button
                      selected={isSelected}
                      onClick={() =>
                        setSelectedCandidate(isSelected ? null : candidate)
                      }
                    >
                      <ListItemIcon>
                        <CandidateAvatar candidate={candidate} />
                      </ListItemIcon>
                      <ListItemText
                        primary={candidateName(candidate)}
                        secondary={`Connection Score: ${candidate.score}`}
                      />
                    </ListItem>
                  );
                })}
              </List>
            )}
          </Pagination>
        </Grid>

        {/* Connections */}
        <Grid item xs={12} md={8}>
          <Paper>
            <Box width="100%" paddingBottom="60%" position="relative" m={2}>
              <Box
                position="absolute"
                left="0"
                right="0"
                width="100%"
                height="100%"
              >
                <Graph
                  selectedCandidate={selectedCandidate}
                  candidates={candidates}
                  connections={connections}
                  onSelect={setSelectedCandidate}
                ></Graph>
              </Box>
            </Box>

            {selectedCandidate ? (
              <CandidateDetails
                candidate={selectedCandidate}
                candidates={candidates}
                connections={connections}
                onSelect={setSelectedCandidate}
              />
            ) : (
              <Box p={2}>
                <Typography>
                  This is a graph of every Federal Candidate that had at least
                  two shared contributors with another candidate in 2019. Large
                  circles represent Presidential candidates.
                </Typography>
                <Typography>
                  You can click on a circle, or a name on the left, to highlight
                  connections with that candidate.
                </Typography>
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Candidates;
