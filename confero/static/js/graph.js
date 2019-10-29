(function() {
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

  const nodeSize = candidate =>
    candidate.party === "IND" ? 20 : candidate.office === "P" ? 10 : 5;

  const main = async () => {
    const svg = d3.select("svg");

    const width = 960;
    const height = 600;

    const [candidates, connections] = await Promise.all([
      fetchData("candidates"),
      fetchData("connections")
    ]);

    const simulation = d3
      .forceSimulation(candidates)
      .force("link", d3.forceLink(connections).id(node => node.id))
      .force("charge", d3.forceManyBody().strength(() => -4))
      .force("center", d3.forceCenter(width / 2, height / 2));

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

    function zoomed() {
      node.attr("transform", d3.event.transform);
      link.attr("transform", d3.event.transform);
    }

    svg.call(d3.zoom().on("zoom", zoomed));
  };

  main();
})();
