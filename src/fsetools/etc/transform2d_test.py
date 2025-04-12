import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8")


def test_angle_between_two_vectors():
    v1 = [0, 10]
    v2 = [10, 0]
    from fsetools.etc.transforms2d import angle_between_two_vectors_2d
    import numpy as np
    assert angle_between_two_vectors_2d(v1, v2) == np.pi / 2

    v1 = [1, 0]
    v2 = [-1, -1]
    print(angle_between_two_vectors_2d(v2, v1))


def test_rotation_meshgrid():
    import numpy as np
    x_span = np.arange(-10, 11, 1)
    y_span = np.arange(-10, 11, 1)
    theta = 45 / 180 * 3.1415926

    xx_1, yy_1 = np.meshgrid(x_span, y_span)

    from fsetools.etc.transforms2d import rotation_meshgrid
    xx_2, yy_2 = rotation_meshgrid(xx_1, yy_1, theta)

    fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(9, 9))

    ax1.contourf(xx_1, yy_1, np.ones_like(xx_1))
    ax1.set_aspect('equal')
    ax1.set_xlim((-20, 20))
    ax1.set_ylim((-20, 20))

    ax2.contourf(xx_2, yy_2, np.ones_like(xx_2) * 2)
    ax2.set_aspect('equal')
    ax2.set_xlim((-20, 20))
    ax2.set_ylim((-20, 20))

    from fsetools.etc.transforms2d import rotation_meshgrid
    x, y = rotation_meshgrid([10], [0], theta)


def test_find_line_segment_intersection_1():
    pt1 = (10, 10)
    pt2 = (20, 20)

    pt3 = (10, 20)
    pt4 = (20, 10)

    from fsetools.etc.transforms2d import find_line_segment_intersection_1
    result = find_line_segment_intersection_1(pt1, pt2, pt3, pt4)
    print(result)


def test_find_line_segment_intersection_2():
    pt1 = (10, 10)
    pt2 = (20, 20)

    pt3 = (10, 20)
    pt4 = (20, 10)

    from fsetools.etc.transforms2d import find_line_segment_intersection_2
    result = find_line_segment_intersection_2(pt1, pt2, pt3, pt4)
    print(result)


def test_points_in_ploy():
    points_xy = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )

    poly_xy = [
        (1.1, 1.1),
        (3.9, 1.1),
        (3.9, 3.9),
        (1.1, 3.9)
    ]

    from fsetools.etc.transforms2d import points_in_ploy
    res = points_in_ploy(points_xy, poly_xy)

    print(res)


if __name__ == '__main__':
    test_rotation_meshgrid()
    test_find_line_segment_intersection_1()
    test_find_line_segment_intersection_2()
    test_points_in_ploy()
    test_angle_between_two_vectors()
