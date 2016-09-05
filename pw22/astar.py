import logging


class AStar:

    _nodes = []

    class Node:

        parent = None
        h = 0
        g = 0
        f = 0

        def __init__(self, x, y, weight):
            self.x = x
            self.y = y
            self.weight = weight * 2

        def reset(self):
            self.parent = None
            self.h = 0
            self.g = 0
            self.f = 0

    def __init__(self, graph, size):
        logging.debug('Initializing AStar')
        self._open = set()
        self._closed = set()
        self._size = size

        logging.debug('Creating nodes')
        for y in range(0, self._size):
            self._nodes.append([])
            for x in range(0, self._size):
                self._nodes[y].append(AStar.Node(x, y, graph[y][x]))

    def _reset(self):
        self._open.clear()
        self._closed.clear()

        for nodes in self._nodes:
            for node in nodes:
                node.reset()

    def _find_node(self, x, y):
        try:
            return self._nodes[y][x]
        except IndexError:
            logging.debug('Could not find node at x: {0}, y: {1}'.format(x, y))
            return None

    def _calculate_cost(self, node_a, node_b):
        node_a.g = node_a.parent.g + 10
        node_a.h = (abs(node_a.x - node_b.x) + abs(node_a.y - node_b.y))
        node_a.f = node_a.g + node_a.h + node_a.weight

    def _get_node_with_lowest_f(self):
        lowest = None
        for node in self._open:
            if not lowest or node.f < lowest.f:
                lowest = node
        return lowest

    def _neighbors(self, node):
        for y in [-1, 0, 1]:
            for x in [-1, 0, 1]:
                if (x == 0 and y == 0) or ((x == 1 or x == -1) and (y == 1 or y == -1)):
                    continue

                nx = node.x + x
                ny = node.y + y
                if nx == -1 or nx == self._size or ny == -1 or ny == self._size:
                    continue

                n = self._find_node(nx, ny)
                if n:
                    yield n

    def _construct_path(self, node):
        path = []
        while node.parent:
            path.append((node.x, node.y))
            node = node.parent
        return path

    def find_path(self, sx, sy, ex, ey):
        logging.debug('Finding path between {0},{1} and {2},{3}'.format(sx, sy, ex, ey))
        self._reset()

        start_node = self._find_node(sx, sy)
        end_node = self._find_node(ex, ey)

        self._open.add(start_node)

        while len(self._open) > 0:
            current_node = self._get_node_with_lowest_f()
            if current_node == end_node:
                return self._construct_path(current_node)

            self._open.remove(current_node)
            self._closed.add(current_node)

            for node in self._neighbors(current_node):
                if node not in self._closed and node not in self._open:
                    node.parent = current_node
                    self._calculate_cost(node, end_node)
                    self._open.add(node)
