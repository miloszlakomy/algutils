from collections.abc import Iterable
from pprint import pformat
from typing import Any

from algutils.freeze import freeze
from algutils.utils import indent


NodeID = Any
EdgeIDs = tuple[NodeID, NodeID]
NodesDict = dict[NodeID, "DG.Node"]


class DG:
    """Directed Graph"""

    class Node:
        def __init__(self, node_id: NodeID) -> None:
            self.node_id = node_id
            self.parents: NodesDict = {}
            self.children: NodesDict = {}

    def __init__(
        self, node_ids: Iterable[NodeID] = (), edges_ids: Iterable[EdgeIDs] = ()
    ) -> None:
        self.nodes: NodesDict = {}

        self.update_nodes(node_ids)
        self.update_edges(edges_ids)

    def add_node(self, node_id: NodeID) -> None:
        node_id = freeze(node_id)

        if node_id not in self.nodes:
            self.nodes[node_id] = DG.Node(node_id)

    def add_edge(self, edge_ids: EdgeIDs) -> None:
        edge_ids = freeze(edge_ids)

        self.update_nodes(edge_ids)
        parent_id, child_id = edge_ids
        parent = self.nodes[parent_id]
        child = self.nodes[child_id]
        parent.children[child_id] = child
        child.parents[parent_id] = parent

    def update_nodes(self, node_ids: Iterable[NodeID]) -> None:
        for node_id in node_ids:
            self.add_node(node_id)

    def update_edges(self, edges_ids: Iterable[EdgeIDs]) -> None:
        for edge_ids in edges_ids:
            self.add_edge(edge_ids)

    def __str__(self) -> str:
        return "\n".join(
            f"{node.node_id} -> {", ".join(str(child) for child in node.children)}".strip()
            for node in self.nodes.values()
        )

    def __repr__(self) -> str:
        node_ids = list(self.nodes)
        edges_ids = list(set.union(*({*node.children} for node in self.nodes.values())))

        pretty_repr_node_ids = pformat(node_ids)
        pretty_repr_edges_ids = pformat(edges_ids)

        return f"""
{__name__}.DirectedGraph(
    node_ids=(
{indent(pretty_repr_node_ids, times=2)}
    ),
    edges_ids=(
{indent(pretty_repr_edges_ids, times=2)}
    ),
)
""".strip()


DirectedGraph = DG
