from __future__ import annotations

from dataclasses import dataclass, field

from hac.models import EdgeType


@dataclass(frozen=True, order=True)
class Edge:
    source: str
    edge_type: EdgeType
    target: str


@dataclass
class SecurityGraph:
    edges: set[Edge] = field(default_factory=set)

    def add_edge(self, source: str, edge_type: EdgeType, target: str) -> None:
        self.edges.add(Edge(source=source, edge_type=edge_type, target=target))

    def has_edge(self, source: str, edge_type: EdgeType, target: str) -> bool:
        return Edge(source=source, edge_type=edge_type, target=target) in self.edges

    def outgoing(self, source: str, edge_type: EdgeType | None = None) -> list[Edge]:
        edges = [edge for edge in self.edges if edge.source == source]
        if edge_type is not None:
            edges = [edge for edge in edges if edge.edge_type == edge_type]
        return sorted(edges)

    def incoming(self, target: str, edge_type: EdgeType | None = None) -> list[Edge]:
        edges = [edge for edge in self.edges if edge.target == target]
        if edge_type is not None:
            edges = [edge for edge in edges if edge.edge_type == edge_type]
        return sorted(edges)

    def to_dict(self) -> dict[str, list[dict[str, str]]]:
        return {
            "edges": [
                {"source": e.source, "edge_type": e.edge_type.value, "target": e.target}
                for e in sorted(self.edges)
            ]
        }