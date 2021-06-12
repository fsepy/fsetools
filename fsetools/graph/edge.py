from typing import Union, List

from fsetools.graph import Edge, Vertex


class Route(Edge):
    def __init__(self, v1: Vertex, v2: Union[Vertex, List[Vertex]], bidirectional: bool = False, *args, **kwargs):
        super(Route, self).__init__(v1=v1, v2=v2, bidirectional=bidirectional, *args, **kwargs)
