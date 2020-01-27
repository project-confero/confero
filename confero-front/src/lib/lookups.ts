const offices: Record<string, string> = {
  P: "President",
  S: "Senate",
  H: "House"
};

const partyColors: Record<string, string> = {
  DEM: "blue",
  REP: "red",
  IND: "yellow",
  DEFAULT: "gray"
};

export const officeOptions = Object.entries(offices).map(([value, label]) => ({
  value,
  label
}));

export const partyOptions = [
  { value: "DEM", label: "Democrats" },
  { value: "REP", label: "Republicans" },
  { value: "OTHER", label: "Others" }
];

export const lookupOffice = (abbreviation: string): string =>
  offices[abbreviation] || "Unknown";

export const lookupPartyColor = (party: string | null): string =>
  party ? partyColors[party] || partyColors.DEFAULT : partyColors.DEFAULT;
