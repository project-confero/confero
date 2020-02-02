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
  Paper,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormHelperText
} from "@material-ui/core";
import axios from "axios";

import { Candidate, candidateName } from "lib/candidate";
import { officeOptions, partyOptions } from "lib/lookups";
import Pagination from "../basic/Pagination";
import CandidateDetails from "./CandidateDetails";
import CandidateAvatar from "./CandidateAvatar";
import FilterButtons from "./FilterButtons";
import Graph from "components/connections/Graph";
import { Connection } from "lib/connection";

const YEARS = [2020, 2016, 2012, 2008, 2004, 2000];

const getCandidates = async (year: number): Promise<Candidate[]> => {
  const { data } = await axios.get(`./data/${year}/candidates.json`);
  return data;
};

const getConnections = async (year: number): Promise<Connection[]> => {
  const { data } = await axios.get(`./data/${year}/connections.json`);
  return data;
};

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
  const [year, setYear] = React.useState(2020);
  const [filter, setFilter] = React.useState("");
  const [officeFilters, setOfficeFilters] = React.useState<string[]>([]);
  const [partyFilters, setPartyFilters] = React.useState<string[]>([]);
  const [
    selectedCandidate,
    setSelectedCandidate
  ] = React.useState<Candidate | null>(null);

  const [candidates, setCandidates] = React.useState<Candidate[]>([]);
  const [connections, setConnections] = React.useState<Connection[]>([]);

  React.useEffect(() => {
    setCandidates([]);
    setConnections([]);
    getCandidates(year).then(setCandidates);
    getConnections(year).then(setConnections);
  }, [year]);

  const isLoaded = candidates.length > 0 && connections.length > 0;

  const shownCandidates = React.useMemo(
    () => filterCandidates(candidates, filter, officeFilters, partyFilters),
    [candidates, filter, officeFilters, partyFilters]
  );

  return (
    <Container>
      <Box my={2} display="flex">
        <Box flexGrow={1}>
          <Typography>
            Looking to see how specific candidates are connected? Trying to
            figure out who to support?
          </Typography>
          <Typography>
            Search for candidates by name, or filter by office, party, and more.
          </Typography>
        </Box>

        <Box>
          <FormControl>
            <InputLabel>Election Year</InputLabel>
            <Select
              value={year}
              onChange={event =>
                setYear(parseInt(event.target.value as string))
              }
            >
              {YEARS.map(year => (
                <MenuItem key={year} value={year}>
                  {year}
                </MenuItem>
              ))}
            </Select>
            <FormHelperText>Select an election year to view</FormHelperText>
          </FormControl>
        </Box>
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

      {isLoaded ? (
        <Grid container spacing={2} wrap="wrap-reverse">
          {/* Candidates */}
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
                    two shared contributors with another candidate in in the{" "}
                    {year} election. Large circles represent Presidential
                    candidates, and gray lines represent particularly strong
                    connections.
                  </Typography>
                  <Typography>
                    You can click on a circle, or a name on the left, to
                    highlight connections with that candidate.
                  </Typography>
                </Box>
              )}
            </Paper>
          </Grid>
        </Grid>
      ) : null}
    </Container>
  );
};

export default Candidates;
