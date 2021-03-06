import { Connection } from "./connection";
import { orderBy } from "lodash";

export interface Candidate {
  id: string;
  name: string;
  party: string | null;
  office: string;
  state: string;
  district: number;
  score: number;
  contribution_count: number;
  contribution_amount: number;
}

const numberFormatter = new Intl.NumberFormat("en-US", {
  minimumFractionDigits: 0
});

const currencyFormatter = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  minimumFractionDigits: 0
});

export const candidateName = ({
  name,
  office,
  state,
  district
}: Candidate): string => {
  if (office === "P") return `${name}: President`;
  if (office === "S") return `${name}: ${state} Senate`;
  return `${name}: ${state} D${district} House`;
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

export const contributions = (candidate: Candidate): string =>
  numberFormatter.format(candidate.contribution_count);

export const contributionAmount = (candidate: Candidate): string =>
  currencyFormatter.format(candidate.contribution_amount);

export const orderByOffice = (candidates: Candidate[]) =>
  orderBy(
    candidates,
    ({ office }) => (office === "P" ? 0 : office === "S" ? 1 : 2),
    "desc"
  );

function isDefined<T>(value: T | undefined | null): value is T {
  return !(value === undefined || value === null);
}
