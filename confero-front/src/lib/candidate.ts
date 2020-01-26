import { Connection } from "./connection";
import { orderBy } from "lodash";

export interface Candidate {
  id: string;
  name: string;
  party: string | null;
  office: string;
  state: string;
  district: number;
}

export interface CandidateNode extends Candidate {
  x: number;
  y: number;
}

export const candidateName = (candidate: Candidate): string => {
  if (!candidate.party) return candidate.name;
  return `${candidate.name} (${candidate.party[0]} ${candidate.state})`;
};

export const findConnectedCandidates = (
  candidate: Candidate,
  candidates: Candidate[],
  connections: Connection[]
): { candidate: Candidate; score: number }[] => {
  const candidateConnections = connections.filter(
    connection => connection.source_id === candidate.id
  );
  const ordered = orderBy(
    candidateConnections,
    connection => connection.score,
    "desc"
  );

  return ordered
    .map(connection => {
      const candidate = candidates.find(
        candidate => candidate.id === connection.target_id
      );
      if (!candidate) return null;
      return { candidate, score: connection.score };
    })
    .filter(isDefined);
};

function isDefined<T>(value: T | undefined | null): value is T {
  return !(value === undefined || value === null);
}
