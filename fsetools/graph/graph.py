from fsetools.graph import Graph
from fsetools.graph.edge import *
from fsetools.graph.vertex import *


class ExitCapacityModel(Graph):
    def __init__(self, *args, **kwargs):
        super(ExitCapacityModel, self).__init__(*args, **kwargs)

        # self.__usource = USource()
        # self.__usink = USink()
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
            vertices=list(vertices)+[self.source, self.sink], edges=list(edges)+edges_new
        )


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
    plt.show()
    assert model.flow_value == 130


if __name__ == '__main__':
    # _test()
    _test_undirected_flow()
