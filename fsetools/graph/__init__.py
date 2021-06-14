import sys
from itertools import count
from typing import Union, List, Tuple

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow, shortest_path

from fsetools import logger

fake_modules = [np, csr_matrix, maximum_flow]


class Vertex(object):
    _ids = count(0)

    def __init__(self, capacity: int, is_enabled: bool = True, is_visible: bool = True, id: int = None, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        if id is None:
            self.__id = next(self._ids)
        else:
            self.__id = id
            ids = next(self._ids)
            if ids < id:
                self._ids = count(id + 1)
            else:
                self._ids = count(ids)

        self.__capacity = None

        self.capacity = capacity

        self.is_enabled = is_enabled
        self.is_visible = is_visible

    @property
    def id(self) -> int:
        return self.__id

    @property
    def capacity(self) -> int:
        return self.__capacity

    @capacity.setter
    def capacity(self, capacity: int):
        try:
            assert isinstance(capacity, int) and capacity >= 0
        except AssertionError as e:
            raise TypeError(f'capacity should be integer (provided {capacity}), {e}')
        self.__capacity = capacity

    def __lt__(self, other):
        return self.capacity < other.capacity

    def __le__(self, other):
        return self.capacity <= other.capacity

    def __eq__(self, other):
        return self.capacity == other.capacity

    def __ne__(self, other):
        return self.capacity != other.capacity

    def __gt__(self, other):
        return self.capacity > other.capacity

    def __ge__(self, other):
        return self.capacity >= other.capacity

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)


class Edge(object):
    _ids = count(0)

    def __init__(self, v1: Vertex, v2: Vertex, weight: int = 1, bidirectional: bool = False, id: int = None, *args,
                 **kwargs):
        if id is None:
            self.__id = next(self._ids)
        else:
            self.__id = int(id)
            ids = next(self._ids)
            if ids < id:
                self._ids = count(id + 1)
            else:
                self._ids = count(ids)
        self.__vertex_1 = v1
        self.__vertex_2 = v2
        self.__weight = weight
        self.__bidirectional = bidirectional

    @property
    def id(self) -> int:
        return self.__id

    @property
    def bidirectional(self) -> bool:
        return self.__bidirectional

    @property
    def v1(self) -> Vertex:
        return self.__vertex_1

    @property
    def v2(self) -> Vertex:
        return self.__vertex_2

    @property
    def capacity(self) -> int:
        return min(self.__vertex_1.capacity, self.__vertex_2.capacity)

    @property
    def weight(self) -> int:
        return self.__weight

    @weight.setter
    def weight(self, weight: int):
        if not isinstance(weight, int): raise TypeError
        self.__weight = weight

    def __str__(self):
        return str(self.id)


class Graph(object):
    def __init__(self, *args, **kwargs):
        super(Graph, self).__init__(*args, **kwargs)
        self.__adjacency_matrix_c = None  # capacity adjacency matrix, based upon Vertex capacity
        self.__adjacency_matrix_w = None  # weighted adjacency matrix, based on Edge weight
        self.__adjacency_list = None

        self.__vertices: List[Vertex] = list()
        self.__edges: List[Edge] = list()

        self.__source = None
        self.__sink = None

        self.__vertices_id2index = dict()
        self.__vertices_index2id = dict()
        self.__vertices_index2name = dict()

        self.__maximum_flow = None
        self.__shortest_path = None

    @property
    def id2index(self) -> dict:
        return self.__vertices_id2index

    @property
    def index2id(self) -> dict:
        return self.__vertices_index2id

    @property
    def index2name(self)-> dict:
        return self.__vertices_index2name

    @property
    def vertices(self):
        return self.__vertices

    @property
    def edges(self):
        return self.__edges

    @property
    def adjacency_matrix_c(self) -> np.ndarray:
        return self.__adjacency_matrix_c

    @property
    def adjacency_matrix_w(self) -> np.ndarray:
        return self.__adjacency_matrix_w

    @property
    def adjacency_list(self) -> list:
        return self.__adjacency_list

    @property
    def flow_value(self) -> int:
        try:
            return self.__maximum_flow.flow_value
        except:
            logger.warn('Maximum flow not computed')
            return None

    @property
    def residual(self) -> csr_matrix:
        try:
            return self.__maximum_flow.residual
        except:
            logger.warn('Maximum flow not computed')
            return None

    @property
    def source(self):
        return self.__source

    @property
    def sink(self):
        return self.__sink

    @source.setter
    def source(self, v: Vertex):
        if isinstance(v, Vertex) or issubclass(type(v), Vertex):
            self.__source = v
        else:
            raise TypeError

    @sink.setter
    def sink(self, v: Vertex):
        if isinstance(v, Vertex) or issubclass(type(v), Vertex):
            self.__sink = v
        else:
            raise TypeError

    def add_vertex(self, vertex: Union[Vertex, List[Vertex], Tuple[Vertex, ...]]):
        if isinstance(vertex, Vertex):
            self.__vertices.append(vertex)
        elif isinstance(vertex, (list, tuple)) and all([isinstance(i, Vertex) for i in vertex]):
            self.__vertices.extend(vertex)
        else:
            raise TypeError(f'vertex must be Vertex type')
        self.__is_input_changed = True

    def add_edge(self, edge: Union[Edge, List[Edge], Tuple[Edge, ...]]):
        if isinstance(edge, Edge):
            self.__edges.append(edge)
        elif isinstance(edge, (list, tuple)) and all([isinstance(i, Edge) for i in edge]):
            self.__edges.extend(edge)
        else:
            raise TypeError(f'edge must be Edge type')
        self.__is_input_changed = True

    def build(self, vertices=None, edges=None):
        vertices = self.__vertices if vertices is None else vertices
        edges = self.__edges if edges is None else edges

        n_vertices = len(vertices)

        # ================================================================
        # Build index -> vertices id and vertices id -> index dictionaries
        # ================================================================
        index2id = {i: vertice.id for i, vertice in enumerate(vertices)}
        id2index = {vertice.id: i for i, vertice in enumerate(vertices)}
        index2name = {i: vertice.name for i, vertice in enumerate(vertices)}
        self.__vertices_index2id = index2id
        self.__vertices_id2index = id2index
        self.__vertices_index2name = index2name

        # =================================
        # Compute capacity adjacency matrix
        # =================================
        adjacency_matrix_c = np.zeros(shape=(n_vertices, n_vertices), dtype=int)
        adjacency_matrix_w = np.zeros(shape=(n_vertices, n_vertices), dtype=int)
        for edge in edges:
            v1id, v2id = edge.v1.id, edge.v2.id
            adjacency_matrix_c[id2index[v1id], id2index[v2id]] = edge.capacity
            adjacency_matrix_w[id2index[v1id], id2index[v2id]] = edge.weight
        self.__adjacency_matrix_c = adjacency_matrix_c
        self.__adjacency_matrix_w = adjacency_matrix_w

        # ======================
        # Compute adjacency list
        # ======================
        adjacency_list = dict()
        for i in range(n_vertices):
            adjacency_list[index2id[i]] = list()
            for j in range(n_vertices):
                if adjacency_matrix_c[i, j] > 0:
                    adjacency_list[index2id[i]].append(index2id[j])
        self.__adjacency_list = adjacency_list

    def maximum_flow(self):
        adjacency_matrix = self.adjacency_matrix_c
        id2index = self.__vertices_id2index

        # ====================
        # Compute maximum flow
        # ====================
        graph = csr_matrix(adjacency_matrix)
        self.__maximum_flow = maximum_flow(graph, id2index[self.source.id], id2index[self.sink.id])

    def shortest_path(self):
        adjacency_matrix = self.adjacency_matrix_w
        id2index = self.__vertices_id2index

        # ====================
        # Compute maximum flow
        # ====================
        graph = csr_matrix(adjacency_matrix)
        self.__shortest_path = shortest_path(graph, id2index[self.source.id], id2index[self.sink.id])


def _test():
    room_1 = Vertex(60)
    room_1_door = Vertex(120)
    room_2 = Vertex(60)
    room_2_door = Vertex(120)
    room_3 = Vertex(120)
    room_3_door = Vertex(120)
    room_4 = Vertex(120)
    room_4_door = Vertex(120)
    corridor = Vertex(sys.maxsize)
    stair_1 = Vertex(200)
    stair_1_door = Vertex(200)
    stair_2 = Vertex(200)
    stair_2_door = Vertex(200)
    virtual_source = Vertex(sys.maxsize)
    ultimate_safety = Vertex(sys.maxsize)
    vertices = list(dict(locals()).values())

    edges = (
        Edge(room_1, room_1_door),
        Edge(room_2, room_2_door),
        Edge(room_3, room_3_door),
        Edge(room_4, room_4_door),
        Edge(room_1_door, corridor),
        Edge(room_2_door, corridor),
        Edge(room_3_door, corridor),
        Edge(room_4_door, corridor),
        Edge(corridor, stair_1_door),
        Edge(corridor, stair_2_door),
        Edge(stair_1_door, stair_1),
        Edge(stair_2_door, stair_2),
        Edge(virtual_source, room_1),
        Edge(virtual_source, room_2),
        Edge(virtual_source, room_3),
        Edge(virtual_source, room_4),
        Edge(stair_1, ultimate_safety),
        Edge(stair_2, ultimate_safety),
    )

    g = Graph()
    g.add_vertex(vertices)
    g.add_edge(edges)
    g.source = virtual_source
    g.sink = ultimate_safety
    g.build()
    g.maximum_flow()
    print(f'flow achieved: {g.flow_value}')
    assert g.flow_value == 360


if __name__ == '__main__':
    _test()
