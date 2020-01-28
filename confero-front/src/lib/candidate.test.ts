import { Candidate, candidateName } from "./candidate";

describe("candidate", () => {
  const candidate: Candidate = {
    id: "cand-id",
    name: "Camacho",
    office: "H",
    district: 4,
    party: "DEM",
    score: 100,
    state: "CA",
    contribution_amount: 100,
    contribution_count: 4
  };
  describe("candidateName", () => {
    it("handles house candidates", () => {
      expect(candidateName(candidate)).toBe("Camacho: CA D4 House");
    });
  });
});
