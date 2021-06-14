from fsetools.graph.exit_capacity import *


def test_ExitCapacityModel():
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
    exit_1 = FinalExit(500)
    exit_2 = FinalExit(500)
    vertices_d = dict(
        room_1=room_1, room_1_door=room_1_door, room_2=room_2, room_2_door=room_2_door, room_3=room_3,
        room_3_door=room_3_door, room_4=room_4, room_4_door=room_4_door, corridor=corridor, stair_1=stair_1,
        stair_1_door=stair_1_door, stair_2=stair_2, stair_2_door=stair_2_door, exit_1=exit_1, exit_2=exit_2
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
        (stair_1, exit_1),
        (stair_2, exit_2),
    )
    edges = [Route(*i) for i in edges_t]

    model = ExitCapacityModel()
    model.add_vertex(list(vertices_d.values()))
    model.add_edge(edges)
    model.build()
    model.maximum_flow()
    try:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        model.plot_residual(ax)
        plt.show()
    except ImportError:
        pass

    print(f'flow achieved {model.flow_value}')
    assert model.flow_value == 200


def test_ExitCapacityModel_undirected_flow():
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
    try:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6, 6))
        model.plot_residual(ax)
    except ImportError:
        pass
    assert model.flow_value == 130


def test_export_to_json():
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
    print(model.flow_value)
    return model.export_to_json()


def test_json2graph():
    model = json2graph(test_export_to_json())
    model.build()
    model.maximum_flow()
    print(model.flow_value)


def test_csv2exit_capacity_model():
    from fsetools.tests.graph.data import vertices_csv, edges_csv
    model = csv2exit_capacity_model(fp_vertices=vertices_csv, fp_edges=edges_csv)
    model.build()
    model.maximum_flow()
    print(model.flow_value)


if __name__ == '__main__':
    pass
