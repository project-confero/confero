$(function() {
  const fetchData = type =>
    fetch(`/api/graph/${type}`).then(response => response.json());

  const PARTY_COLORS = {
    DEM: "blue",
    REP: "red",
    IND: "yellow",
    default: "black"
  };
  const nodeColor = candidate =>
    PARTY_COLORS[candidate.party] || PARTY_COLORS.default;

  const nodeSize = candidate => (candidate.office === "P" ? 10 : 5);

  const main = async () => {
    const svg = d3.select("svg");

    const width = 960;
    const height = 600;

    const [candidates, connections] = await Promise.all([
      fetchData("candidates"),
      fetchData("connections")
    ]);

    /* Force Simulation */
    const simulation = d3
      .forceSimulation(candidates)
      .force("link", d3.forceLink(connections).id(node => node.id))
      .force("charge", d3.forceManyBody().strength(() => -4))
      .force("center", d3.forceCenter(width / 2, height / 2));

    /* SVG */
    const link = svg
      .append("g")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .selectAll("line")
      .data(connections)
      .join("line")
      .attr("stroke-width", d => Math.sqrt(d.score));

    const node = svg
      .append("g")
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
      .selectAll("circle")
      .data(candidates)
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
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      node.attr("cx", d => d.x).attr("cy", d => d.y);
    });

    /* Zoom */
    function zoomed() {
      node.attr("transform", d3.event.transform);
      link.attr("transform", d3.event.transform);
    }

    svg.call(d3.zoom().on("zoom", zoomed));

    const nodeOpacity = (
      selectedCandidate,
      connectedCandidates
    ) => candidate => {
      if (!selectedCandidate) return 1;
      if (candidate.id === selectedCandidate) return 1;
      if (connectedCandidates.includes(candidate.id)) return 1;
      return 0.25;
    };

    const nodeBorder = selectedCandidate => candidate => {
      if (selectedCandidate && selectedCandidate === candidate.id)
        return "yellow";
      return "white";
    };

    const nodeBorderWidth = selectedCandidate => candidate => {
      if (selectedCandidate && selectedCandidate === candidate.id) return 3;
      return 1.5;
    };

    const linkOpacity = selectedCandidate => connection => {
      if (!selectedCandidate) return 1;
      if (connection.source.id === selectedCandidate) return 1;
      return 0;
    };

    const updateHighlight = selectedCandidate => {
      const connectedCandidates = connections
        .filter(({ source }) => source.id === selectedCandidate)
        .map(({ target }) => target.id);

      const selectedNode = node.filter(({ id }) => id === selectedCandidate);
      const connectedNodes = node.filter(({ id }) =>
        connectedCandidates.includes(id)
      );

      const connectedLinks = link.filter(
        ({ source }) => source.id === selectedCandidate
      );

      // Raise above other nodes for selection
      connectedLinks.raise();
      connectedNodes.raise();
      selectedNode.raise();

      // Reset
      node
        .style("opacity", 0.25)
        .attr("stroke", "white")
        .attr("stroke-width", 1.5);
      link.style("opacity", 0.1).attr("stroke", "#999");

      // Set connected/selected styles
      connectedNodes.style("opacity", 1);
      selectedNode
        .style("opacity", 1)
        .attr("stroke", "yellow")
        .attr("stroke-width", 3);
      connectedLinks.style("opacity", 1).attr("stroke", "black");
    };

    $("#candidates").val("");
    $("#candidates").autocomplete({
      source: candidates.map(candidate => ({
        label: candidate.name,
        id: candidate.id
      })),
      select: (event, ui) => updateHighlight(ui.item.id)
    });

    node.on("click", ({ id }) => updateHighlight(id));

    $("#clear").click(() => {
      $("#candidates").val("");

      node
        .style("opacity", 1)
        .attr("stroke", "white")
        .attr("stroke-width", 1.5);
      link.style("opacity", 1).attr("stroke", "#999");
    });
  };

  main();
});
