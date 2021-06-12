import sys

from fsetools.graph import Vertex


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


class Room(Vertex, Shape2D):
    def __init__(self, occupants, *args, **kwargs):
        super().__init__(capacity=occupants, *args, **kwargs)


class Corridor(Vertex):
    def __init__(self, capacity, *args, **kwargs):
        super().__init__(capacity=capacity, *args, **kwargs)


class Floor(Vertex):
    def __init__(self, *args, **kwargs):
        super().__init__(capacity=sys.maxsize, *args, **kwargs)


class Stair(Vertex):
    def __init__(self, capacity, *args, **kwargs):
        super().__init__(capacity=capacity, *args, **kwargs)


class Door(Vertex):
    def __init__(self, capacity, *args, **kwargs):
        super().__init__(capacity=capacity, *args, **kwargs)


class FinalExit(Vertex):
    def __init__(self, capacity, *args, **kwargs):
        super(FinalExit, self).__init__(capacity=capacity, *args, **kwargs)


class USource(Vertex):
    def __init__(self, *args, **kwargs):
        super().__init__(capacity=sys.maxsize, *args, **kwargs)


class USink(Vertex):
    def __init__(self, *args, **kwargs):
        super().__init__(capacity=sys.maxsize, *args, **kwargs)


if __name__ == '__main__':
    a=USink()
    print(issubclass(type(a), Vertex))
