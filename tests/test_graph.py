from hac.graph import SecurityGraph
from hac.models import EdgeType


def test_graph_adds_edges_once():
    graph = SecurityGraph()
    graph.add_edge("a", EdgeType.READS, "r")
    graph.add_edge("a", EdgeType.READS, "r")
    assert len(graph.edges) == 1


def test_graph_queries_outgoing():
    graph = SecurityGraph()
    graph.add_edge("a", EdgeType.READS, "r")
    graph.add_edge("a", EdgeType.WRITES, "x")
    assert [edge.target for edge in graph.outgoing("a", EdgeType.READS)] == ["r"]


def test_graph_serialization_is_sorted():
    graph = SecurityGraph()
    graph.add_edge("b", EdgeType.READS, "2")
    graph.add_edge("a", EdgeType.READS, "1")
    assert graph.to_dict()["edges"][0]["source"] == "a"