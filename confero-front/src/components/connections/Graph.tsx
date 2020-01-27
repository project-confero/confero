import React from "react";
import { orderBy } from "lodash";
import {
  runSimulation,
  CandidateNode,
  ConnectionLink,
  SIM_WIDTH,
  SIM_HEIGHT
} from "lib/simulation";
import { Candidate } from "lib/candidate";
import { Connection } from "lib/connection";

const PARTY_COLORS: Record<string, string> = {
  DEM: "blue",
  REP: "red",
  IND: "yellow",
  default: "black"
};

const nodeColor = (candidate: CandidateNode) =>
  candidate.party !== null
    ? PARTY_COLORS[candidate.party] || PARTY_COLORS.default
    : PARTY_COLORS.default;

const nodeSize = (candidate: CandidateNode) =>
  candidate.office === "P" ? 10 : 5;

const nodeOpacity = (
  candidate: CandidateNode,
  selectedCandidate: string | null
) => {
  if (!selectedCandidate) return 1;
  if (candidate.id === selectedCandidate) return 1;
  if (candidate.connected) return 1;
  return 0.25;
};

const nodeBorder = (
  candidate: CandidateNode,
  selectedCandidate: string | null
) => {
  if (selectedCandidate && selectedCandidate === candidate.id) return "yellow";
  return "white";
};

const nodeBorderWidth = (
  candidate: CandidateNode,
  selectedCandidate: string | null
) => {
  if (selectedCandidate && selectedCandidate === candidate.id) return 3;
  return 1.5;
};

const linkOpacity = (
  link: ConnectionLink,
  selectedCandidate: string | null
) => {
  if (!selectedCandidate) return 1;
  if (link.source.id === selectedCandidate) return 1;
  return 0;
};

const linkBorder = (link: ConnectionLink, selectedCandidate: string | null) => {
  if (link.source.id === selectedCandidate) return "black";
  return "gray";
};

interface GraphPropTypes {
  candidates: Candidate[];
  connections: Connection[];
}

const Graph: React.FunctionComponent<GraphPropTypes> = ({
  candidates,
  connections
}) => {
  const [selectedCandidate, setSelectedCandidate] = React.useState<
    string | null
  >(null);

  const [simCandidates, setSimCandidates] = React.useState<
    CandidateNode[] | null
  >(null);

  const [simEdges, setSimEdges] = React.useState<ConnectionLink[] | null>(null);

  React.useEffect(() => {
    const { nodes, links } = runSimulation(candidates, connections);

    // Render the graph
    setSimCandidates(nodes);
    setSimEdges(links);

    return () => {};
  }, [candidates, connections]);

  const simCandidatesWithConnections = React.useMemo(() => {
    if (!selectedCandidate || !simEdges || !simCandidates) return simCandidates;

    const connectedCandidates = simEdges
      .filter(({ source }) => source.id === selectedCandidate)
      .map(({ target }) => target.id);

    const candidates = simCandidates.map(candidate =>
      connectedCandidates.includes(candidate.id)
        ? { ...candidate, connected: true }
        : { ...candidate, connected: false }
    );

    // Order: selected candidate, then connected, the rest.
    return orderBy(candidates, candidate =>
      candidate.id === selectedCandidate ? 2 : candidate.connected ? 1 : 0
    );
  }, [selectedCandidate, simEdges, simCandidates]);

  if (!(simCandidatesWithConnections && simEdges)) return null;

  return (
    <svg
      style={{ flexGrow: 1 }}
      width="100%"
      height="100%"
      viewBox={`0 0 ${SIM_WIDTH} ${SIM_HEIGHT}`}
      preserveAspectRatio="xMidYMid meet"
    >
      {/* Edges */}
      <g stroke="#999" strokeOpacity={0.6}>
        {simEdges.map(edge => {
          return (
            <line
              key={edge.index}
              strokeWidth={1}
              x1={edge.source.x}
              y1={edge.source.y}
              x2={edge.target.x}
              y2={edge.target.y}
              opacity={linkOpacity(edge, selectedCandidate)}
              stroke={linkBorder(edge, selectedCandidate)}
            />
          );
        })}
      </g>

      {/* Nodes */}
      <g stroke="#fff" strokeWidth={1.5}>
        {simCandidatesWithConnections.map((candidate: CandidateNode) => (
          <circle
            key={candidate.index}
            r={nodeSize(candidate)}
            fill={nodeColor(candidate)}
            cx={candidate.x}
            cy={candidate.y}
            onClick={() =>
              selectedCandidate === candidate.id
                ? setSelectedCandidate(null)
                : setSelectedCandidate(candidate.id)
            }
            opacity={nodeOpacity(candidate, selectedCandidate)}
            stroke={nodeBorder(candidate, selectedCandidate)}
            strokeWidth={nodeBorderWidth(candidate, selectedCandidate)}
          >
            <title>
              {candidate.name} | {candidate.office} | {candidate.state}
            </title>
          </circle>
        ))}
      </g>
    </svg>
  );
};

export default Graph;
