(function() {
  const fetchData = type =>
    fetch(`/api/graph/${type}`).then(response => response.json());

  const PARTY_COLORS = {
    DEM: "blue",
    REP: "red",
    IND: "yellow",
    default: "black"
  };
  const nodeColor = campaign =>
    PARTY_COLORS[campaign.party] || PARTY_COLORS.default;

  const nodeSize = campaign =>
    campaign.party === "IND" ? 20 : campaign.office === "P" ? 15 : 5;

  const main = async () => {
    const svg = d3.select("svg");

    const width = 960;
    const height = 600;

    const [campaigns, connections] = await Promise.all([
      fetchData("campaigns"),
      fetchData("connections")
    ]);

    const simulation = d3
      .forceSimulation(campaigns)
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
      .data(campaigns)
      .join("circle")
      .attr("r", nodeSize)
      .attr("fill", nodeColor);

    node
      .append("title")
      .text(
        campaign => `${campaign.name} | ${campaign.office} | ${campaign.state}`
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
