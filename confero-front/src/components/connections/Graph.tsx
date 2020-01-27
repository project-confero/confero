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
import { lookupPartyColor } from "lib/lookups";

interface GraphPropTypes {
  candidates: Candidate[];
  connections: Connection[];
  selectedCandidate: Candidate | null;
  onSelect: (candidate: Candidate | null) => void;
}

const Graph: React.FunctionComponent<GraphPropTypes> = ({
  candidates,
  connections,
  selectedCandidate,
  onSelect
}) => {
  const selectedCandidateId = selectedCandidate ? selectedCandidate.id : null;
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
    if (!selectedCandidateId || !simEdges || !simCandidates)
      return simCandidates;

    const connectedCandidates = simEdges
      .filter(({ source }) => source.id === selectedCandidateId)
      .map(({ target }) => target.id);

    const candidates = simCandidates.map(candidate =>
      connectedCandidates.includes(candidate.id)
        ? { ...candidate, connected: true }
        : { ...candidate, connected: false }
    );

    // Order: selected candidate, then connected, the rest.
    return orderBy(candidates, candidate =>
      candidate.id === selectedCandidateId ? 2 : candidate.connected ? 1 : 0
    );
  }, [selectedCandidateId, simEdges, simCandidates]);

  if (!(simCandidatesWithConnections && simEdges)) return null;

  return (
    <svg
      style={{ flexGrow: 1, padding: "1rem" }}
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
              opacity={linkOpacity(edge, selectedCandidateId)}
              stroke={linkBorder(edge, selectedCandidateId)}
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
              selectedCandidateId === candidate.id
                ? onSelect(null)
                : onSelect(candidate)
            }
            opacity={nodeOpacity(candidate, selectedCandidateId)}
            stroke={nodeBorder(candidate, selectedCandidateId)}
            strokeWidth={nodeBorderWidth(candidate, selectedCandidateId)}
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

export default React.memo(Graph);

const nodeColor = (candidate: CandidateNode) =>
  lookupPartyColor(candidate.party);

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
