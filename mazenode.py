import random


class MazeNode:

    path_combinations = [[False, False, False, True],
                         [False, False, True, False],
                         [False, False, True, True],
                         [False, True, False, False],
                         [False, True, False, True],
                         [False, True, True, False],
                         [False, True, True, True],
                         [True, False, False, False],
                         [True, False, False, True],
                         [True, False, True, False],
                         [True, False, True, True],
                         [True, True, False, False],
                         [True, True, False, True],
                         [True, True, True, False]]

    def __init__(self, x, y) -> None:
        self.name = (x, y)

        self.adjacent = {"north": None,
                         "south": None,
                         "west": None,
                         "east": None}

        self.generated = False
        self.state = None

    def check_path(self, visited=[]):
        visited = visited + [self]

        if self.name == "exit":
            return True

        for node in self.adjacent.values():
            if node not in visited and node:
                return node.check_path(visited)
        return False

    def generate_paths(self):
        # check valid paths for node
        generated = []
        for node in self.adjacent.values():
            if node:
                adjacent = node.adjacent.values()
                if node.generated and self not in adjacent:
                    for key, value in self.adjacent.items():
                        if node == value:
                            self.adjacent[key] = None
                elif node.generated and self in adjacent:
                    generated.append(node)
                elif node.is_dead_end():
                    generated.append(node)

        # generating possible path combinations
        paths = []
        enum_adjacent = list(enumerate(self.adjacent.items()))
        for combination in self.path_combinations:
            new_adjacent = self.adjacent.copy()
            for index, item in enum_adjacent:
                path, node = item
                if new_adjacent[path] and combination[index] and new_adjacent[path] not in generated:
                    new_adjacent[path] = None
            if new_adjacent not in paths:
                not_none = False
                for value in new_adjacent.values():
                    if value:
                        not_none = True
                if not_none:
                    paths.append(new_adjacent)
        random.shuffle(paths)
        return paths

    def is_dead_end(self):
        if self.generated:
            raise Exception(f"{self.name} is already generated")

        paths = 0
        for node in self.adjacent.values():
            if node:
                if node.generated and self in node.adjacent.values():
                    paths += 1
                elif not node.generated:
                    paths += 1
                else:
                    for key, value in self.adjacent.items():
                        if node == value:
                            self.adjacent[key] = None

        if paths > 1:
            self.restore_state()
            return False
        else:
            self.generated = True
            return True

    def save_state(self):
        if not self.state:
            self.state = self.adjacent.copy()
        else:
            raise Exception("State already saved.")

    def restore_state(self):
        if self.state:
            self.adjacent = self.state.copy()
            self.generated = False
        else:
            raise Exception("No saved state to restore.")

    def __repr__(self) -> str:
        return str(self.name)
