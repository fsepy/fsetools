def draw_polygon(path, ax, origin=(0, 0)):
    vertices = list()
    vertices.append(path.pop(0))

    for v in path:
        previous_vertex = vertices[-1]
        vertices.append((previous_vertex[0] + v[0], previous_vertex[1] + v[1]))

    vertices.append(vertices[0])

    for i in range(len(vertices)):
        vertices[i] = (vertices[i][0] + origin[0], vertices[i][1] + origin[1])

    xs, ys = zip(*vertices)

    ax.axis('equal')

    ax.fill(xs, ys)


def plan_forced_draught_column(ax):
    # forced draught, column, plan

    is_forced_draught = True
    w_t = 5
    h_eq = 2

    d_1 = 0.5
    d_2 = 0.8
    d_3 = 1
    d_4 = 2.5

    L_L = 3
    L_H = 2

    wall_thickness = 0.2
    wall_1_length = 1
    wall_2_length = 0.5

    w_f = 7

    path_upper_wall = [
        (0, 0),
        (wall_thickness, 0),
        (0, wall_1_length),
        (wall_2_length, 0),
        (0, wall_thickness),
        (-wall_2_length - wall_thickness, 0),
        (0, -wall_thickness - wall_1_length),
    ]

    path_lower_wall = [
        (0, -w_t),
        (0, -wall_1_length - wall_thickness),
        (wall_2_length + wall_thickness, 0),
        (0, wall_thickness),
        (-wall_2_length, 0),
        (0, wall_1_length),
        (-wall_thickness, 0)
    ]

    path_fire = [
        (0, 0),
        (-L_H, abs(w_f - w_t) / 2),
        (0, -w_f),
        (L_H, abs(w_f - w_t) / 2)
    ]

    path_column = [
        (-d_3, -d_4),
        (0, -d_2),
        (d_1, 0),
        (0, d_2),
    ]

    draw_polygon(path_upper_wall, ax)
    draw_polygon(path_lower_wall, ax)
    draw_polygon(path_fire, ax)
    draw_polygon(path_column, ax)


def section_forced_draught_column(ax):
    # forced draught, column, plan

    is_forced_draught = True
    w_t = 5
    h_eq = 2

    d_1 = 0.5  # column dimension perpendicular to the external wall
    d_2 = 0.8  # column dimension parallel to the external wall
    d_3 = 1  # horizontal distance between column and external wall
    d_4 = 2.5  # vertical distance between column and external wall

    L_L = 3
    L_H = 2

    wall_thickness = 0.2
    wall_1_upper = 1  # external wall upper length
    wall_1_lower = 0.5  # external wall lower length
    wall_1_left = 0.5  # external wall left length
    wall_1_right = 0.5  # external wall right length
    wall_1_upper_ = 0.5  # external wall the storey above
    wall_1_lower_ = 0.5  # external wall the storey below
    wall_2 = 0.5  # wall perpendicular to the external wall
    wall_3 = 0.5  # wall perpendicular to the external wall

    floor_1 = 0.5
    floor_2 = 0.5
    floor_thickness = 0.2

    w_f = 7

    path_upper_wall = [
        (0, 0),
        (wall_thickness, 0),
        (0, wall_1_left),
        (floor_1, 0),
        (0, floor_thickness),
        (-floor_1, 0),
        (0, wall_1_upper_),
        (-wall_thickness, 0),
        (0, -wall_1_upper_ - floor_thickness - wall_1_left),
    ]

    path_lower_wall = [
        (0, -h_eq),
        (0, -wall_1_lower - floor_thickness - wall_1_lower_),
        (wall_thickness, 0),
        (0, wall_1_lower_),
        (floor_2, 0),
        (0, floor_thickness),
        (-floor_2, 0),
        (0, wall_1_lower)
    ]

    fire = [
        (0, 0),
        (-L_H, L_L),
        (0, -h_eq),
        (L_H, -L_L),
    ]

    fire = [
        (0, 0),
        (-L_H, L_L),
        (0, -h_eq),
        (L_H, -L_L),
    ]

    draw_polygon(path_upper_wall, ax)
    draw_polygon(path_lower_wall, ax)
    draw_polygon(fire, ax)


if __name__ == '__main__':
    # fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True)
    # ax1.axis('equal')
    # ax2.axis('equal')
    #
    # plan_forced_draught_column(ax1)
    # section_forced_draught_column(ax2)
    #
    # plt.show()

    if (a := 10) > 9:
        pass
    print(a)
