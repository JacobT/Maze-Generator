import mazenode


def print_maze(maze):
    for row in maze:
        print_list = [[], [], []]
        for node in row:
            if node.adjacent["north"] or node.name == "entry":
                print_list[0].append("# #")
            else:
                print_list[0].append("###")

            if node.adjacent["east"] and node.adjacent["west"]:
                print_list[1].append("   ")
            elif node.adjacent["east"] and not node.adjacent["west"]:
                print_list[1].append("  #")
            elif not node.adjacent["east"] and node.adjacent["west"]:
                print_list[1].append("#  ")
            else:
                print_list[1].append("# #")

            if node.adjacent["south"] or node.name == "exit":
                print_list[2].append("# #")
            else:
                print_list[2].append("###")

        for line in print_list:
            for part in line:
                print(part, end="")
            print("")


def find_not_generated(maze, not_generated):
    for row in maze:
        for node in row:
            if not node.generated:
                not_generated.append(node)
                return True
    return False


def generate(maze):
    not_generated = []
    if not find_not_generated(maze, not_generated):
        return True

    node = not_generated[0]

    paths = node.generate_paths()
    for path in paths:
        node.adjacent = path
        node.generated = True
        if node.check_path():
            if generate(maze):
                return True
        node.restore_state()
    return False


WIDTH = 10
HEIGHT = 5

maze = [[mazenode.MazeNode(i, j) for j in range(WIDTH)] for i in range(HEIGHT)]

for i in range(HEIGHT):
    for j in range(WIDTH):
        if i != 0:
            maze[i][j].adjacent["north"] = maze[i - 1][j]
        if i != HEIGHT - 1:
            maze[i][j].adjacent["south"] = maze[i + 1][j]
        if j != 0:
            maze[i][j].adjacent["east"] = maze[i][j - 1]
        if j != WIDTH - 1:
            maze[i][j].adjacent["west"] = maze[i][j + 1]
        maze[i][j].save_state()

maze[0][0].name = "entry"
maze[HEIGHT - 1][WIDTH - 1].name = "exit"

# print(maze[0][0].check_path())

# maze[0][0].adjacent["west"] = None
# maze[0][0].generated = True
# maze[1][1].adjacent["north"] = None
# maze[1][1].generated = True
# maze[1][2].generated = True
# maze[0][3].adjacent["east"] = None
# maze[0][3].generated = True

# print(maze[0][1].generated)
# maze[0][2].generate_paths()
# print(maze[0][1].generated)

# for row in maze:
#     print(row)

print(generate(maze))
print_maze(maze)
