import json
import sys
from typing import Union, List

from fsetools import logger
from fsetools.graph import Edge, Vertex
from fsetools.graph import Graph


class EnclosureBase(object):
    def __init__(self, name: str = None, *args, **kwargs):
        self.__kwargs = dict(kwargs)
        self.__name = name
        super(EnclosureBase, self).__init__(*args, **kwargs)

        self.__utilisation = None

    @property
    def name(self):
        return self.__name

    @property
    def utilisation(self) -> int:
        return self.__utilisation

    @name.setter
    def name(self, name: str):
        self.__name = name

    @utilisation.setter
    def utilisation(self, utilisation: int):
        try:
            assert isinstance(utilisation, int) and utilisation >= 0
        except AssertionError as e:
            raise TypeError(f'capacity should be integer (provided {utilisation}), {e}')
        self.__utilisation = utilisation

    def to_dict(self):
        self.__kwargs['name'] = self.name
        self.__kwargs['obj'] = type(self).__name__
        try:
            self.__kwargs['id'] = self.id
        except:
            pass
        return self.__kwargs


class Route(EnclosureBase, Edge):
    def __init__(self, v1: Vertex, v2: Union[Vertex, List[Vertex]], bidirectional: bool = False, *args, **kwargs):
        super(Route, self).__init__(v1=v1, v2=v2, bidirectional=bidirectional, *args, **kwargs)


class Room(EnclosureBase, Vertex):
    def __init__(self, capacity, *args, **kwargs):
        super().__init__(capacity=capacity, *args, **kwargs)


class Corridor(EnclosureBase, Vertex):
    def __init__(self, capacity, *args, **kwargs):
        super().__init__(capacity=capacity, *args, **kwargs)


class Floor(EnclosureBase, Vertex):
    def __init__(self, *args, **kwargs):
        super().__init__(capacity=sys.maxsize, *args, **kwargs)


class Stair(EnclosureBase, Vertex):
    def __init__(self, capacity, *args, **kwargs):
        super().__init__(capacity=capacity, *args, **kwargs)


class Door(EnclosureBase, Vertex):
    def __init__(self, capacity, *args, **kwargs):
        super().__init__(capacity=capacity, *args, **kwargs)


class FinalExit(EnclosureBase, Vertex):
    def __init__(self, capacity, *args, **kwargs):
        super(FinalExit, self).__init__(capacity=capacity, *args, **kwargs)


class USource(EnclosureBase, Vertex):
    def __init__(self, *args, **kwargs):
        super().__init__(capacity=sys.maxsize, *args, **kwargs)


class USink(EnclosureBase, Vertex):
    def __init__(self, *args, **kwargs):
        super().__init__(capacity=sys.maxsize, *args, **kwargs)


class ExitCapacityModel(EnclosureBase, Graph):
    def __init__(self, *args, **kwargs):
        super(ExitCapacityModel, self).__init__(*args, **kwargs)
        self.source: USource = USource(name='__START__')
        self.sink: USink = USink(name='__END__')

    def plot_residual(self, ax, show_name: bool = False):
        from matplotlib.pyplot import Axes
        if not isinstance(ax, Axes):
            raise TypeError

        residual = self.residual.toarray()
        ax.imshow(residual, cmap='Blues', origin='upper')

        for i in range(residual.shape[0]):
            for j in range(residual.shape[1]):
                ax.text(i, j, str(residual[i, j]), color='k', ha='center', va='center')

        if show_name:
            index2name = self.index2name
            ax.set_xticks(range(residual.shape[0]))
            ax.set_yticks(range(residual.shape[1]))
            ax.set_xticklabels([index2name[i] for i in range(residual.shape[0])], rotation=90)
            ax.set_yticklabels([index2name[i] for i in range(residual.shape[0])])
        else:
            ax.set_xticks(range(residual.shape[0]))
            ax.set_yticks(range(residual.shape[1]))
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')
        ax.axis('equal')

    def build(self, *args, **kwargs):
        vertices = self.vertices
        edges = self.edges

        edges_new = list()
        for vertex in vertices:
            if isinstance(vertex, Room):
                edges_new.append(Edge(self.source, vertex))
            elif isinstance(vertex, FinalExit):
                edges_new.append(Edge(vertex, self.sink))

        super(ExitCapacityModel, self).build(
            vertices=list(vertices) + [self.source, self.sink], edges=list(edges) + edges_new
        )

    def assign_utilisation(self):
        residual = self.residual.toarray()
        residual[residual < 0] = 0
        for v in self.vertices:
            v.utilisation = int(sum(residual[:, self.id2index[v.id]]))

    def get_total_occupancy(self):
        """Calculate the total capacity assigned to all Room objects"""
        occ = 0
        for v in self.vertices:
            if isinstance(v, Room):
                occ += v.capacity
        return occ

    def get_total_exit_capacity(self):
        """Calculate the sum of all flows to self.sink"""
        return sum(self.residual.toarray()[:, self.id2index[self.sink.id]])

    def export_to_dict(self):
        export_data = dict()
        export_data['ExitCapacityModel'] = self.to_dict()
        export_data['vertices'] = [vertex.to_dict() for vertex in self.vertices]
        export_data['edges'] = [edge.to_dict() for edge in self.edges]
        return export_data

    def export_to_json(self):
        def obj2basic_types(v):
            v1 = str(v)
            try:
                if float(v1) == int(v1):
                    return int(v1)
                else:
                    return float(v1)
            except TypeError:
                v1_lower = v1.lower()
                if v1_lower == 'false':
                    return False
                elif v1_lower == 'true':
                    return True
                else:
                    return v1

        return json.dumps(self.export_to_dict(), indent=4, default=obj2basic_types)


def json2graph(json_string: str) -> ExitCapacityModel:
    dict_data = json.loads(json_string)

    vertices = dict()
    vertex_type_dict = dict(Room=Room, Door=Door, Corridor=Corridor, FinalExit=FinalExit)
    for v in dict_data['vertices']:
        obj = v.pop('obj')
        vertices[v['id']] = vertex_type_dict[obj](**v)

    edges = dict()
    for e in dict_data['edges']:
        e.pop('obj')
        v1 = vertices[e.pop('v1')]
        v2 = vertices[e.pop('v2')]
        edges[e['id']] = Route(v1=v1, v2=v2, **e)

    model = ExitCapacityModel()
    model.add_vertex(list(vertices.values()))
    model.add_edge(list(edges.values()))
    return model


def csv2exit_capacity_model(fp_vertices: str, fp_edges: str) -> ExitCapacityModel:
    import csv
    try:
        with open(fp_vertices, 'r') as f:
            r = csv.reader(f)
    except:
        r = csv.reader(fp_vertices)
    vertices_l = list(r)[1:]
    vertices = dict()
    vertex_type = dict(Room=Room, Door=Door, FinalExit=FinalExit, Corridor=Corridor, Stair=Stair)
    for vl in vertices_l:
        name, type_, capacity = vl
        vertices[name] = vertex_type[type_](capacity=int(capacity), name=name)

    try:
        with open(fp_edges, 'r') as f:
            r = csv.reader(f)
    except:
        r = csv.reader(fp_edges)

    edges_l = list(r)[1:]
    edges = list()
    for el in edges_l:
        v1name, v0name, v2name, bidirectional = el
        if bidirectional.lower() == 'false':
            bidirectional = False
        elif bidirectional.lower() == 'true':
            bidirectional = True
        else:
            raise ValueError

        try:
            if v0name != '-':
                edges.append(Route(v1=vertices[v0name], v2=vertices[v1name], bidirectional=bidirectional))
        except KeyError:
            logger.warn(f'Failed to instantiate Edge, v1 name {v0name} and v2 name {v1name}')
            pass
        try:
            if v2name != '-':
                edges.append(Route(v1=vertices[v1name], v2=vertices[v2name], bidirectional=bidirectional))
        except KeyError:
            logger.warn(f'Failed to instantiate Edge, v1 name {v1name} and v2 name {v2name}')

    model = ExitCapacityModel()
    model.add_vertex(list(vertices.values()))
    model.add_edge(edges)
    return model


if __name__ == '__main__':
    pass
