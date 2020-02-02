import * as d3 from "d3";
import { SimulationLinkDatum, SimulationNodeDatum } from "d3";
import { memoize, clamp } from "lodash";

import { Connection, ConnectionEdge, convertConnections } from "./connection";
import { Candidate, orderByOffice } from "./candidate";

type OmitNodes<T> = Omit<Omit<T, "target">, "source">;

export type CandidateNode = Candidate &
  SimulationNodeDatum & { connected?: boolean };
export type ConnectionLink = OmitNodes<ConnectionEdge> &
  OmitNodes<SimulationLinkDatum<CandidateNode>> & {
    source: CandidateNode;
    target: CandidateNode;
  };

export const SIM_WIDTH = 2000;
export const SIM_HEIGHT = 1200;
export const NODE_SIZE = SIM_WIDTH / 200;

const CHARGE = -20;
const ITERATIONS = 300;

export const runSimulation = memoize(
  (candidates: Candidate[], connections: Connection[]) => {
    if (!(candidates.length > 0 && connections.length > 0)) {
      return { nodes: [], links: [] };
    }
    const nodes = orderByOffice(candidates) as CandidateNode[];

    const links = (convertConnections(
      connections
    ) as unknown) as ConnectionLink[];

    const simulation = d3
      .forceSimulation(nodes)
      .force("collide", d3.forceCollide(NODE_SIZE * 2))
      .force(
        "link",
        d3
          .forceLink(links)
          .id((node: any) => node.id)
          .distance(link => link.score)
      )
      .force(
        "charge",
        d3.forceManyBody().strength(() => CHARGE)
      )
      .force("center", d3.forceCenter(SIM_WIDTH / 3, SIM_HEIGHT / 2));

    // Run the simulation
    for (var i = 0; i < ITERATIONS; ++i) {
      simulation.tick();

      nodes.forEach(node => {
        node.x = clamp(node.x || 0, 10, SIM_WIDTH - 10);
        node.y = clamp(node.y || 0, 10, SIM_HEIGHT - 10);
      });
    }
    simulation.stop();

    return { nodes, links };
  }
);
