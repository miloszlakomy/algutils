from collections.abc import Iterable
from typing import Any


NodeId = Any
NodeIds = Iterable[NodeId]
EdgeIds = tuple[NodeId, NodeId]
EdgesIds = Iterable[EdgeIds]


class DisjointSets:
    def __init__(self, node_ids: NodeIds = (), edges_ids: EdgesIds = ()) -> None:
        self._node_id_to_node: dict[NodeId, _Node] = {}
        self._disjoint_sets_roots: set[_Node] = set()

        self.add_nodes(node_ids)
        self.add_edges(edges_ids)

    def __len__(self) -> int:
        return len(self._disjoint_sets_roots)

    def get_sets(self) -> list[set[NodeId]]:
        self._flatten()

        return [
            {node.node_id for node in root.children} | root.node_id
            for root in self._disjoint_sets_roots
        ]

    def add_node(self, node_id: Any) -> None:
        node = _Node(node_id)
        self._node_id_to_node[node_id] = node
        self._disjoint_sets_roots.add(node)

    def add_nodes(self, node_ids: NodeIds) -> None:
        for node_id in node_ids:
            self.add_node(node_id)

    def add_edge(self, edge_ids: EdgeIds) -> None:
        first_node_id, second_node_id = edge_ids

        first_node = self._node_id_to_node[first_node_id]
        second_node = self._node_id_to_node[second_node_id]

        first_root = self._find_root(first_node)
        second_root = self._find_root(second_node)

        if first_root is second_root:
            return

        self._disjoint_sets_roots.remove(second_root)
        first_root.children.add(second_root)
        second_root.parent = first_root

    def add_edges(self, edges_ids: EdgesIds) -> None:
        for edge_ids in edges_ids:
            self.add_edge(edge_ids)

    def _find_root(self, node: "_Node") -> "_Node":
        if node.parent is node.parent.parent:
            return node

        node.parent.children.remove(node)
        node.parent = node.parent.parent
        node.parent.children.add(node)

        return self._find_root(node.parent)

    def _flatten(self) -> None:
        for root in self._disjoint_sets_roots:
            disjoint_set_nodes = {root}
            nodes_layer = {root}

            while nodes_layer:
                nodes_layer = set.union(*(node.children for node in nodes_layer))
                disjoint_set_nodes.update(nodes_layer)

            for node in disjoint_set_nodes:
                node.parent = root
                node.children.clear()

            root.children = disjoint_set_nodes - {root}


class _Node:
    def __init__(self, node_id: Any) -> None:
        self.node_id = node_id
        self.parent = self
        self.children: set[_Node] = set()
