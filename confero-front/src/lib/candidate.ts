export interface Candidate {
  id: string;
  name: string;
  party: string | null;
  office: string;
  state: string;
  district: string | null;
}

export const candidateName = (candidate: Candidate): string => {
  if (!candidate.party) return candidate.name;
  return `${candidate.name} (${candidate.party[0]} ${candidate.state})`;
};
