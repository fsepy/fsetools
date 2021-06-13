import json
import sys
from typing import Union, List

from fsetools import logger
from fsetools.graph import Edge, Vertex
from fsetools.graph import Graph


class PropertyManager:
    def __init__(self, name: str = None, *args, **kwargs):
        self.__kwargs = dict(kwargs)
        self.__name = name
        super(PropertyManager, self).__init__(*args, **kwargs)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    def to_dict(self):
        self.__kwargs['name'] = self.name
        self.__kwargs['obj'] = type(self).__name__
        try:
            self.__kwargs['id'] = self.id
        except:
            pass
        return self.__kwargs


class Route(PropertyManager, Edge):
    def __init__(self, v1: Vertex, v2: Union[Vertex, List[Vertex]], bidirectional: bool = False, *args, **kwargs):
        super(Route, self).__init__(v1=v1, v2=v2, bidirectional=bidirectional, *args, **kwargs)


class Shape2D:
    def __init__(self, *args, **kwargs):
        super(Shape2D, self).__init__(*args, **kwargs)
        self.__x = None
        self.__y = None

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @x.setter
    def x(self, v: float):
        if not isinstance(v, (int, float)): raise TypeError
        self.__x = v

    @y.setter
    def y(self, v: float):
        if not isinstance(v, (int, float)): raise TypeError
        self.__y = v


class Room(PropertyManager, Vertex):
    def __init__(self, capacity, *args, **kwargs):
        super().__init__(capacity=capacity, *args, **kwargs)


class Corridor(PropertyManager, Vertex):
    def __init__(self, capacity, *args, **kwargs):
        super().__init__(capacity=capacity, *args, **kwargs)


class Floor(PropertyManager, Vertex):
    def __init__(self, *args, **kwargs):
        super().__init__(capacity=sys.maxsize, *args, **kwargs)


class Stair(PropertyManager, Vertex):
    def __init__(self, capacity, *args, **kwargs):
        super().__init__(capacity=capacity, *args, **kwargs)


class Door(PropertyManager, Vertex):
    def __init__(self, capacity, *args, **kwargs):
        super().__init__(capacity=capacity, *args, **kwargs)


class FinalExit(PropertyManager, Vertex):
    def __init__(self, capacity, *args, **kwargs):
        super(FinalExit, self).__init__(capacity=capacity, *args, **kwargs)


class USource(PropertyManager, Vertex):
    def __init__(self, *args, **kwargs):
        super().__init__(capacity=sys.maxsize, *args, **kwargs)


class USink(PropertyManager, Vertex):
    def __init__(self, *args, **kwargs):
        super().__init__(capacity=sys.maxsize, *args, **kwargs)


class ExitCapacityModel(PropertyManager, Graph):
    def __init__(self, *args, **kwargs):
        super(ExitCapacityModel, self).__init__(*args, **kwargs)
        self.source = USource()
        self.sink = USink()

    def plot_residual(self, ax):
        from matplotlib.pyplot import Axes
        if not isinstance(ax, Axes):
            raise TypeError

        residual = self.residual.toarray()
        ax.imshow(residual, cmap='Blues', origin='upper')

        for i in range(residual.shape[0]):
            for j in range(residual.shape[1]):
                ax.text(i, j, str(residual[i, j]), color='k', ha='center', va='center')

        ax.set_xticks(range(residual.shape[0]))
        ax.set_yticks(range(residual.shape[1]))
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')

    def plot_residual_graph(self, ax):
        from matplotlib.pyplot import Axes
        if not isinstance(ax, Axes):
            raise TypeError
        pass

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


def _test():
    room_1 = Room(100)
    room_1_door = Door(60)
    room_2 = Room(100)
    room_2_door = Door(60)
    room_3 = Room(100)
    room_3_door = Door(60)
    room_4 = Room(100)
    room_4_door = Door(60)
    corridor = Corridor(400)
    stair_1 = Stair(100)
    stair_1_door = Door(100)
    stair_2 = Stair(100)
    stair_2_door = Door(100)
    virtual_source = USource()
    ultimate_safety = USink()
    vertices_d = dict(
        room_1=room_1, room_1_door=room_1_door, room_2=room_2, room_2_door=room_2_door, room_3=room_3,
        room_3_door=room_3_door, room_4=room_4, room_4_door=room_4_door, corridor=corridor, stair_1=stair_1,
        stair_1_door=stair_1_door, stair_2=stair_2, stair_2_door=stair_2_door, source=virtual_source,
        sink=ultimate_safety
    )

    edges_t = (
        (room_1, room_1_door),
        (room_2, room_2_door),
        (room_3, room_3_door),
        (room_4, room_4_door),
        (room_1_door, corridor),
        (room_2_door, corridor),
        (room_3_door, corridor),
        (room_4_door, corridor),
        (corridor, stair_1_door),
        (corridor, stair_2_door),
        (stair_1_door, stair_1),
        (stair_2_door, stair_2),
        (virtual_source, room_1),
        (virtual_source, room_2),
        (virtual_source, room_3),
        (virtual_source, room_4),
        (stair_1, ultimate_safety),
        (stair_2, ultimate_safety),
    )
    edges = [Route(*i) for i in edges_t]

    model = ExitCapacityModel()
    model.add_vertex(list(vertices_d.values()))
    model.add_edge(edges)
    model.source = virtual_source
    model.sink = ultimate_safety
    residual = model.residual.toarray()
    print(f'flow achieved {model.flow_value}')
    # print('Escape path utilisation:')
    # print(g.residual)
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    model.plot_residual(ax)
    plt.show()


def _test_undirected_flow():
    room_1 = Room(1000)
    room_1_door = Door(100)
    room_2 = Room(1000)
    room_2_door = Door(10)
    room_3 = Room(1000)
    room_3_door = Door(10)
    room_4 = Room(1000)
    room_4_door = Door(10)
    corridor_1 = Corridor(400)
    corridor_2 = Corridor(400)
    stair_1 = Stair(2)
    stair_1_door = Door(200)
    stair_2 = Stair(200)
    stair_2_door = Door(200)
    final_exit_1 = FinalExit(200)
    final_exit_2 = FinalExit(300)
    vertices_d = dict(locals())

    edges = (
        Route(room_1, room_1_door),
        Route(room_2, room_2_door),
        Route(room_3, room_3_door),
        Route(room_4, room_4_door),
        Route(room_1_door, corridor_1),
        Route(room_2_door, corridor_1),
        Route(room_3_door, corridor_2),
        Route(room_4_door, corridor_2),
        Route(corridor_1, stair_1_door),
        Route(corridor_2, stair_2_door),
        Route(corridor_1, corridor_2, bidirectional=True),
        Route(stair_1_door, stair_1),
        Route(stair_2_door, stair_2),
        Route(stair_1, final_exit_1),
        Route(stair_2, final_exit_2),
    )

    model = ExitCapacityModel()
    model.add_vertex(tuple(vertices_d.values()))
    model.add_edge(edges)
    model.build()
    model.maximum_flow()
    print(f'flow achieved {model.flow_value}')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6, 6))
    model.plot_residual(ax)
    # plt.show()
    assert model.flow_value == 130


def _test_export_to_json():
    room_1 = Room(120)
    room_1_door = Door(250)
    room_2 = Room(100)
    room_2_door = Door(40)
    corridor = Corridor(1000)
    exit = FinalExit(450)
    vertices = list(dict(locals()).values())
    edges = (
        Route(room_1, room_1_door),
        Route(room_2, room_2_door),
        Route(room_1_door, corridor),
        Route(room_2_door, corridor),
        Route(corridor, exit)
    )
    model = ExitCapacityModel()
    model.add_edge(edges)
    model.add_vertex(vertices)
    model.build()
    model.maximum_flow()
    # import pprint
    # pprint.pprint(model.export_to_dict())
    print(model.flow_value)
    return model.export_to_json()


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
    # import pprint
    # pprint.pprint(model.export_to_dict())


def _test_json2graph(json_string: str):
    model = json2graph(json_string)
    model.build()
    model.maximum_flow()
    print(model.flow_value)


def csv2exit_capacity_model(fp_vertices: str, fp_edges: str) -> ExitCapacityModel:
    import csv
    with open(fp_vertices, 'r') as f:
        r = csv.reader(f)
        vertices_l = list(r)[1:]
    vertices = dict()
    vertex_type = dict(Room=Room, Door=Door, FinalExit=FinalExit, Corridor=Corridor, Stair=Stair)
    for vl in vertices_l:
        name, type_, capacity = vl
        vertices[name] = vertex_type[type_](capacity=int(capacity), name=name)

    with open(fp_edges, 'r') as f:
        r = csv.reader(f)
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


def _test_csv2exit_capacity_model():
    model = csv2exit_capacity_model(fp_vertices='vertices.csv', fp_edges='edges.csv')

    model.build()
    model.maximum_flow()
    print(model.flow_value)


if __name__ == '__main__':
    # _test()
    # _test_undirected_flow()
    # jss = _test_export_to_json()
    # _test_json2graph(jss)
    _test_csv2exit_capacity_model()
