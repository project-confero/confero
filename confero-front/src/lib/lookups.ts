const offices: Record<string, string> = {
  H: "House",
  S: "Senate",
  P: "President"
};

const partyColors: Record<string, string> = {
  DEM: "blue",
  REP: "red",
  DEFAULT: "gray"
};

export const lookupOffice = (abbreviation: string): string =>
  offices[abbreviation] || "Unknown";

export const lookupPartyColor = (party: string | null): string =>
  party ? partyColors[party] || partyColors.DEFAULT : partyColors.DEFAULT;
