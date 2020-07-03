NODE, EDGE, ATTR = range(3)


class Node:
    def __init__(self, name, attrs):
        self.name = name
        self.attrs = attrs

    def __eq__(self, other):
        return self.name == other.name and self.attrs == other.attrs


class Edge:
    def __init__(self, src, dst, attrs):
        self.src = src
        self.dst = dst
        self.attrs = attrs

    def __eq__(self, other):
        return (self.src == other.src and
                self.dst == other.dst and
                self.attrs == other.attrs)


class Graph:
    def __init__(self, data=None):

        self.nodes = []
        self.edges = []
        self.attrs = {}

        if data and self.is_valid(data):

            for spec in data:

                if spec[0] == NODE:
                    self.nodes.append(Node(*spec[1:]))
                elif spec[0] == EDGE:
                    self.edges.append(Edge(*spec[1:]))
                else:
                    self.attrs[spec[1]] = spec[2]

    @staticmethod
    def is_valid(data):
        if not isinstance(data, list):
            raise TypeError("Data not iterable")

        elif len(data[0]) < 2:
            raise TypeError("Data not complete")

        else:
            assert_obj = {NODE: [str, dict], EDGE: [str, str, dict], ATTR: [str, str]}
            try:
                if not all([assert_obj[obj[0]] == [type(x) for x in obj[1:]] for obj in data]):
                    raise ValueError("Data malformed")
            except KeyError:
                raise ValueError("Data malformed")

        return True

