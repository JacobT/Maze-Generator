import random
import time
from collections import deque


class MazeNode:

    def __init__(self, row, column):
        self.name = "node"
        self.coords = (row, column)
        self.visited = False

        self.adjacent = {"north": None,
                         "south": None,
                         "west": None,
                         "east": None}

    def __repr__(self):
        return str(self.coords)


class Maze:

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.total_nodes = height * width
        self.visited = 0

        self.maze = [[MazeNode(h, w) for w in range(self.width)]
                     for h in range(self.height)]

        self.maze[0][0].name = "entry"
        self.maze[height - 1][width - 1].name = "exit"

    def generate_recursive(self, node):
        # self.print_maze()
        # time.sleep(0.005)
        node.visited = True
        self.visited += 1

        if self.visited == self.total_nodes:
            return True

        adjacent = self.get_adjacent(node.coords)
        for next_node, node_direction, next_node_direction in adjacent:
            if not next_node.visited:
                node.adjacent[node_direction] = next_node
                next_node.adjacent[next_node_direction] = node
                if self.generate_recursive(next_node):
                    return True
        return False

    def generate_loop(self):
        stack = deque()
        self.maze[0][0].visited = True
        stack.append(self.maze[0][0])
        while len(stack) > 0:
            # self.print_maze()
            # time.sleep(0.005)
            node = stack.pop()
            adjacent = self.get_adjacent(node.coords)
            if len(adjacent) > 0:
                next_node, node_direction, next_node_direction = adjacent[0]
                node.adjacent[node_direction] = next_node
                next_node.adjacent[next_node_direction] = node
                next_node.visited = True
                stack.append(node)
                stack.append(next_node)

    def get_adjacent(self, node_coords):
        x = node_coords[1]
        y = node_coords[0]
        adjacent = []
        if x > 0:
            if not self.maze[y][x - 1].visited:
                adjacent.append((self.maze[y][x - 1], "west", "east"))
        if x < self.width - 1:
            if not self.maze[y][x + 1].visited:
                adjacent.append((self.maze[y][x + 1], "east", "west"))
        if y > 0:
            if not self.maze[y - 1][x].visited:
                adjacent.append((self.maze[y - 1][x], "north", "south"))
        if y < self.height - 1:
            if not self.maze[y + 1][x].visited:
                adjacent.append((self.maze[y + 1][x], "south", "north"))

        random.shuffle(adjacent)
        return adjacent

    def print_maze(self):
        print("# ", (self.width - 1) * "##", "#", sep="")
        for row in self.maze:
            line_1 = "#"
            line_2 = "#"
            for node in row:
                if node.adjacent["east"]:
                    line_1 += "  "
                elif node.visited == True:
                    line_1 += " #"
                else:
                    line_1 += "##"

                if node.adjacent["south"] or node.name == "exit":
                    line_2 += " #"
                else:
                    line_2 += "##"
            print(line_1)
            print(line_2)


if __name__ == "__main__":
    maze = Maze(15, 100)
    maze.generate_recursive(maze.maze[0][0])
    # maze.generate_loop()
    maze.print_maze()
