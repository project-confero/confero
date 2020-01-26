import React from "react";
import {
  Box,
  Container,
  TextField,
  Button,
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
import Pagination from "../basic/Pagination";
import CandidateDetails from "./CandidateDetails";
import OfficeBadge from "./CandidateAvatar";
import CandidateAvatar from "./CandidateAvatar";

const Candidates = () => {
  const [filter, setFilter] = React.useState("");
  const [officeFilters, setOfficeFilters] = React.useState<string[]>([]);
  const [
    selectedCandidate,
    setSelectedCandidate
  ] = React.useState<Candidate | null>(null);

  const onOfficeClick = (office: string) => {
    if (officeFilters.includes(office)) {
      setOfficeFilters(officeFilters.filter(filter => filter !== office));
    } else {
      setOfficeFilters([...officeFilters, office]);
    }
  };

  const shownCandidates = React.useMemo(() => {
    const compareFilter = filter.toLowerCase();
    return candidates.filter(candidate => {
      const matchesText = candidate.name.toLowerCase().includes(compareFilter);
      const matchesOffice =
        officeFilters.length > 0
          ? officeFilters.includes(candidate.office)
          : true;

      return matchesText && matchesOffice;
    });
  }, [filter, officeFilters]);

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

      <Box display="flex" my={2}>
        <Button
          variant="contained"
          onClick={() => onOfficeClick("P")}
          color={officeFilters.includes("P") ? "primary" : "default"}
        >
          President
        </Button>
        <Button
          variant="contained"
          color={officeFilters.includes("H") ? "primary" : "default"}
          onClick={() => onOfficeClick("H")}
        >
          House
        </Button>
        <Button
          variant="contained"
          color={officeFilters.includes("S") ? "primary" : "default"}
          onClick={() => onOfficeClick("S")}
        >
          Senate
        </Button>
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
