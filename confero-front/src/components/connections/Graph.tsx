import React from "react";
import { Box, Container } from "theme-ui";
import * as d3 from "d3";
import { SimulationNodeDatum, SimulationLinkDatum } from "d3-force";

import candidates from "../../data/candidates.json";
import connections from "../../data/connections.json";
import { Candidate } from "../../lib/candidate";
import { convertConnections, ConnectionEdge } from "../../lib/connection";

type CandidateNode = Candidate & SimulationNodeDatum;
type ConnectionLink = ConnectionEdge & SimulationLinkDatum<CandidateNode>;

const edges: ConnectionLink[] = convertConnections(connections);

console.log({ ...edges[0] }, edges[0]);
console.log(candidates[0]);

const PARTY_COLORS: Record<string, string> = {
  DEM: "blue",
  REP: "red",
  IND: "yellow",
  default: "black"
};

const width = 960;
const height = 600;

const nodeColor = (candidate: CandidateNode) =>
  candidate.party !== null
    ? PARTY_COLORS[candidate.party] || PARTY_COLORS.default
    : PARTY_COLORS.default;

const nodeSize = (candidate: CandidateNode) =>
  candidate.office === "P" ? 10 : 5;

const nodeOpacity = (
  selectedCandidate: string,
  connectedCandidates: string[]
) => (candidate: CandidateNode) => {
  if (!selectedCandidate) return 1;
  if (candidate.id === selectedCandidate) return 1;
  if (connectedCandidates.includes(candidate.id)) return 1;
  return 0.25;
};

const nodeBorder = (selectedCandidate: string) => (
  candidate: CandidateNode
) => {
  if (selectedCandidate && selectedCandidate === candidate.id) return "yellow";
  return "white";
};

const nodeBorderWidth = (selectedCandidate: string) => (
  candidate: CandidateNode
) => {
  if (selectedCandidate && selectedCandidate === candidate.id) return 3;
  return 1.5;
};

const linkOpacity = (selectedCandidate: string) => (connection: any) => {
  if (!selectedCandidate) return 1;
  if (connection.source.id === selectedCandidate) return 1;
  return 0;
};

const Graph = () => {
  const ref = React.useRef<SVGSVGElement>(null);

  const [
    selectedCandidate,
    setSelectedCandidate
  ] = React.useState<CandidateNode | null>(null);

  const [node, setNode] = React.useState<d3.Selection<
    SVGSVGElement,
    CandidateNode,
    SVGSVGElement,
    CandidateNode
  > | null>(null);

  const [link, setLink] = React.useState<d3.Selection<
    SVGSVGElement,
    ConnectionLink,
    SVGSVGElement,
    ConnectionLink
  > | null>(null);

  React.useEffect(() => {
    const svg = d3.select(ref.current);

    const simulation = d3
      .forceSimulation(candidates as CandidateNode[])
      .force(
        "link",
        d3.forceLink(edges).id((node: any) => node.id)
      )
      .force(
        "charge",
        d3.forceManyBody().strength(() => -4)
      )
      .force("center", d3.forceCenter(width / 2, height / 2));

    /* SVG */
    const link = svg
      .append("g")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .selectAll("line")
      .data(edges)
      .join("line")
      .attr("stroke-width", d => Math.sqrt(d.score));

    const node = svg
      .append("g")
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
      .selectAll("circle")
      .data(candidates as Candidate[])
      .join("circle")
      .attr("r", nodeSize)
      .attr("fill", nodeColor);

    link.append("title").text(connection => connection.score);

    node
      .append("title")
      .text(
        candidate =>
          `${candidate.name} | ${candidate.office} | ${candidate.state}`
      );

    simulation.on("tick", () => {
      link
        .attr("x1", (d: any) => d.source.x)
        .attr("y1", (d: any) => d.source.y)
        .attr("x2", (d: any) => d.target.x)
        .attr("y2", (d: any) => d.target.y);

      node.attr("cx", (d: any) => d.x).attr("cy", (d: any) => d.y);
    });

    /* Zoom */
    function zoomed() {
      node.attr("transform", d3.event.transform);
      link.attr("transform", d3.event.transform);
    }

    svg.call(d3.zoom().on("zoom", zoomed) as any);

    setNode(node as any);
    setLink(link as any);
  }, []);

  // React.useEffect(() => {
  //   if (!node || !link) return;

  //   const connectedCandidates = edges
  //     .filter(({ source }) => source.id === selectedCandidate)
  //     .map(({ target }) => target.id);

  //   const selectedNode = node.filter(({ id }) => id === selectedCandidate);
  //   const connectedNodes = node.filter(({ id }) =>
  //     connectedCandidates.includes(id)
  //   );

  //   const connectedLinks = link.filter(
  //     ({ source }) => source.id === selectedCandidate
  //   );

  //   // Raise above other nodes for selection
  //   connectedLinks.raise();
  //   connectedNodes.raise();
  //   selectedNode.raise();

  //   // Reset
  //   node
  //     .style("opacity", 0.25)
  //     .attr("stroke", "white")
  //     .attr("stroke-width", 1.5);
  //   link.style("opacity", 0.1).attr("stroke", "#999");

  //   // Set connected/selected styles
  //   connectedNodes.style("opacity", 1);
  //   selectedNode
  //     .style("opacity", 1)
  //     .attr("stroke", "yellow")
  //     .attr("stroke-width", 3);
  //   connectedLinks.style("opacity", 1).attr("stroke", "black");
  // });

  console.log("render");

  return (
    <Container>
      <Box>Confero Graph</Box>
      <svg ref={ref} width={width} height={height}></svg>
    </Container>
  );
};

export default Graph;
