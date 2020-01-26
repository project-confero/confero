const offices: Record<string, string> = {
  H: "House",
  S: "Senate",
  P: "President"
};

export const lookupOffice = (abbreviation: string): string =>
  offices[abbreviation] || "Unknown";
