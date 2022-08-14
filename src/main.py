import numpy as np

# initialising necessary global variables
starting_grid = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                          [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                          [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
                          [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
                          [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
                          [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                          [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                          [0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                          [0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0],
                          [0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 3],
                          [0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
                          [2, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
                          [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
                          [0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])  # 2 = starting, 3 = goal
grid_rows, grid_columns = starting_grid.shape
goal_row, goal_column = np.where(starting_grid == 3)  # 3 indicates goal point
goal_row, goal_column = int(goal_row), int(goal_column)


class Node:
    def __init__(self, row, column, parent, operator, moves):
        self.row = row
        self.column = column
        self.parent = parent
        self.operator = operator
        self.moves = moves
        if row is not None and column is not None:
            self.heuristic = abs(row - goal_row) + abs(column - goal_column)

    # Sort nodes
    def __lt__(self, other):
        return self.heuristic < other.heuristic

    # Compare nodes
    def __eq__(self, other):
        return self.row == other.row and self.column == other.column


# function to create a node
def create_node(row, column, parent, operator, moves):
    return Node(row, column, parent, operator, moves)


# function to move up, left, right, down if it's doable
def expand_node(node, visited):
    expanded_nodes = [create_node(move_up(node.row, node.column, visited), node.column, node, "Up", node.moves + 1),
                      create_node(node.row, move_left(node.row, node.column, visited), node, "Left", node.moves + 1),
                      create_node(node.row, move_right(node.row, node.column, visited), node, "Right", node.moves + 1),
                      create_node(move_down(node.row, node.column, visited), node.column, node, "Down", node.moves + 1)]
    expanded_nodes = [node for node in expanded_nodes if node.row is not None and node.column is not None]
    return expanded_nodes


# check if the position is already visited or not
def isVisited(row, column, visited):
    for i in visited:  # checking if node is already visited or not
        if i.row == row and i.column == column:
            return True
    return False


# function to move left if it's doable
def move_left(row, column, visited):
    if column != 0 and starting_grid[row][column - 1] in [1, 3] and not isVisited(row, column - 1, visited):
        return column - 1
    return None


# function to move right if it's doable
def move_right(row, column, visited):
    if column != grid_columns - 1 and starting_grid[row][column + 1] in [1, 3] \
            and not isVisited(row, column + 1, visited):
        return column + 1
    return None


# function to move up if it's doable
def move_up(row, column, visited):
    if row != 0 and starting_grid[row - 1][column] in [1, 3] and not isVisited(row - 1, column, visited):
        return row - 1
    return None


# function to move down if it's doable
def move_down(row, column, visited):
    if row != grid_rows - 1 and starting_grid[row + 1][column] in [1, 3] and not isVisited(row + 1, column, visited):
        return row + 1
    return None


# GBFS search
def GBFS(starting_row, starting_column):
    # Create lists for open nodes and closed nodes
    open = []
    visited = []

    # Create a start node and an goal node
    start_node = create_node(starting_row, starting_column, None, None, 0)

    # Add the start node
    open.append(start_node)

    # Create cost variable to find total moves utilized
    cost = -1

    # Loop until the open list is empty
    while open:
        # Sort the open list to get the node with the lowest cost first
        open.sort()

        # Get the node with the lowest cost
        current_node = open.pop(0)

        # counting total moves
        if current_node not in visited:
            cost += 1

        # Add the current node to the closed list
        visited.append(current_node)

        # Check if we have reached the goal, return the path (From Current Node to Start Node By Node.parent)
        if current_node.row == goal_row and current_node.column == goal_column:
            # Print costs and return True
            print('Algorithm used = "GBFS" , ', end='')
            print("Path cost =", current_node.moves, ', No of moves utilized =', cost)
            return True

        # Get neighbours
        neighbors = expand_node(current_node, visited)

        # Loop neighbors
        for neighbor in neighbors:
            # Check if the neighbor is in the closed list
            if neighbor in visited:
                continue

            # Check if neighbor is in open list and if it has a lower f value
            if In_Open(open, neighbor):
                # Everything is green, add neighbor to open list
                open.append(neighbor)

    # Return None, no path is found
    return None


# Check if a neighbor should be added to open list
def In_Open(open, neighbor):
    for node in open:
        if neighbor == node and neighbor.heuristic >= node.heuristic:
            return False
    return True


def main():
    # initialising starting coordinates and goal coordinates
    starting_row, starting_column = np.where(starting_grid == 2)  # 2 indicates starting point
    starting_row, starting_column = int(starting_row), int(starting_column)

    # calling functions and displaying output
    if GBFS(starting_row, starting_column) is None:
        print("No solution found using GBFS.")

if __name__ == "__main__":
    main()
