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
