import { CandidateNode } from "./candidate";

export interface Connection {
  id: number;
  score: number;
  source_id: string;
  target_id: string;
}

export interface ConnectionEdge {
  target: string;
  source: string;
  score: number;
}

export const connectionToEdge = (connection: Connection): ConnectionEdge => ({
  target: connection.target_id,
  source: connection.source_id,
  score: connection.score
});

export const convertConnections = (
  connections: Connection[]
): ConnectionEdge[] => connections.map(connectionToEdge);
