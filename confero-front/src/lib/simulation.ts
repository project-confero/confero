import * as d3 from "d3";
import { SimulationLinkDatum, SimulationNodeDatum } from "d3";
import { memoize, clamp } from "lodash";

import { Connection, ConnectionEdge, convertConnections } from "./connection";
import { Candidate } from "./candidate";

type OmitNodes<T> = Omit<Omit<T, "target">, "source">;

export type CandidateNode = Candidate &
  SimulationNodeDatum & { connected?: boolean };
export type ConnectionLink = OmitNodes<ConnectionEdge> &
  OmitNodes<SimulationLinkDatum<CandidateNode>> & {
    source: CandidateNode;
    target: CandidateNode;
  };

export const SIM_WIDTH = 1000;
export const SIM_HEIGHT = 600;

export const runSimulation = memoize(
  (candidates: Candidate[], connections: Connection[]) => {
    const nodes = [...candidates] as CandidateNode[];
    const links = (convertConnections(
      connections
    ) as unknown) as ConnectionLink[];

    const simulation = d3
      .forceSimulation(nodes)
      .force(
        "link",
        d3.forceLink(links).id((node: any) => node.id)
      )
      .force(
        "charge",
        d3.forceManyBody().strength(() => -4)
      )
      .force("center", d3.forceCenter(SIM_WIDTH / 2, SIM_HEIGHT / 2));

    // Run the simulation
    for (var i = 0; i < 100; ++i) {
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
