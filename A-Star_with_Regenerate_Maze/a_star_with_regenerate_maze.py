import heapq
import pandas as pd
import pygame


pygame.init()

TILE = 25
WIDTH, HEIGHT = 1200, 900
cols, rows = WIDTH // TILE, HEIGHT // TILE

start_color = (40, 0, 103)
end_color = (255, 0, 0)

sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('A* algorithm')
clock = pygame.time.Clock()


class MazeDraw():
    def __init__(self, data):
        self.data = data
        self.start_cell = None
        self.end_cell = None

    def get_start_cell(self):
        return self.start_cell

    def get_end_cell(self):
        return self.end_cell

    def draw_lines(self, x, y, walls):
        if walls['top']:
            pygame.draw.line(sc, pygame.Color('#030659'),
                             (x, y), (x + TILE, y), 4)
        if walls['right']:
            pygame.draw.line(sc, pygame.Color('#030659'),
                             (x + TILE, y), (x + TILE, y + TILE), 4)
        if walls['bottom']:
            pygame.draw.line(sc, pygame.Color('#030659'),
                             (x, y + TILE), (x + TILE, y + TILE), 4)
        if walls['left']:
            pygame.draw.line(sc, pygame.Color('#030659'),
                             (x, y), (x, y + TILE), 4)

    def draw_start_end_cells(self):
        if self.start_cell:
            x, y = self.start_cell
            pygame.draw.rect(sc, pygame.Color('#280067'),
                             (x * TILE, y * TILE, TILE, TILE))
        if self.end_cell:
            x, y = self.end_cell
            pygame.draw.rect(sc, pygame.Color('#ff0000'),
                             (x * TILE, y * TILE, TILE, TILE))

    def maze_draw(self):
        for index, row in self.data.iterrows():
            x = row['x'] * TILE
            y = row['y'] * TILE
            walls = eval(str(row['walls']))
            self.draw_lines(x, y, walls)


def heuristic(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])


def a_star(grid, start, goal):
    open_set = [(0, start)]
    closed_set = set()
    paths = {start: (None, 0)}
    changes = []
    while open_set:
        _, current_cell = heapq.heappop(open_set)
        if current_cell == goal:
            path = []
            while current_cell:
                path.append(current_cell)
                current_cell, _ = paths[current_cell]
            return path[::-1], changes
        if current_cell in closed_set:
            continue
        closed_set.add(current_cell)
        changes.append((current_cell, 'closed_set'))
        for neighbor in get_neighbors(grid, current_cell):
            tentative_g = paths[current_cell][1] + 1
            if neighbor not in paths or tentative_g < paths[neighbor][1]:
                paths[neighbor] = (current_cell, tentative_g)
                f_value = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_value, neighbor))
                changes.append((neighbor, 'open_set'))
    return [], []


def get_neighbors(grid, cell):
    col, row = cell
    neighbors = []
    def find_index(x, y): return x + y * cols
    ind = find_index(col, row)
    if grid[ind][0] == 0:
        neighbors.append((col, row-1))
    if grid[ind][1] == 0:
        neighbors.append((col+1, row))
    if grid[ind][2] == 0:
        neighbors.append((col, row+1))
    if grid[ind][3] == 0:
        neighbors.append((col-1, row))
    return neighbors


def draw_changes(changes):
    for cell, cell_type in changes:
        x1, y1 = cell[0] * TILE + TILE // 2, cell[1] * TILE + TILE // 2
        x2, y2 = (cell[0]) * TILE + TILE // 2, (cell[1]) * TILE + TILE // 2
        if cell_type == 'open_set':
            color = '#f5730f'
        elif cell_type == 'closed_set':
            color = '#ffdd00'
        pygame.draw.circle(sc, color, (x1, y1), 8)
        pygame.draw.circle(sc, color, (x2, y2), 8)


def draw_color(grid, start, goal):
    path, changes = a_star(grid, start, goal)
    draw_changes(changes)
    num_steps = len(path)
    for i in range(num_steps - 1):
        cell1 = path[i]
        cell2 = path[i + 1]
        x1, y1 = cell1[0] * TILE + TILE // 2, cell1[1] * TILE + TILE // 2
        x2, y2 = cell2[0] * TILE + TILE // 2, cell2[1] * TILE + TILE // 2

        gradient_factor = i / (num_steps - 1)
        current_color = calculate_gradient_color(start_color,
                                                 end_color,
                                                 gradient_factor)
        hex_color = "#{:02X}{:02X}{:02X}".format(*current_color)

        pygame.draw.circle(sc, hex_color, (x1, y1), 8)
        pygame.draw.circle(sc, hex_color, (x2, y2), 8)
        pygame.draw.line(sc, hex_color, (x1, y1), (x2, y2), 4)


def calculate_gradient_color(start_color, end_color, factor):
    return tuple(int(start + (end - start) * factor)
                 for start, end in zip(start_color, end_color))


def main():
    df = pd.read_csv("maze.csv")
    maze = MazeDraw(df)
    running = True
    while True:
        sc.fill(pygame.Color('#a6d5e2'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                cell_x = mouse_x // TILE
                cell_y = mouse_y // TILE

                if 0 <= cell_x < cols and 0 <= cell_y < rows:
                    if pygame.mouse.get_pressed()[0]:
                        maze.start_cell = (cell_x, cell_y)
                    elif pygame.mouse.get_pressed()[2]:
                        maze.end_cell = (cell_x, cell_y)
        grid = []
        for _, row in df.iterrows():
            walls = eval(row['walls'])
            top_open = 0 if not walls['top'] else 1
            right_open = 0 if not walls['right'] else 1
            bottom_open = 0 if not walls['bottom'] else 1
            left_open = 0 if not walls['left'] else 1
            grid_row = [top_open, right_open, bottom_open, left_open]
            grid.append(grid_row)

        start_cell = maze.get_start_cell()
        end_cell = maze.get_end_cell()
        maze.maze_draw()
        maze.draw_start_end_cells()
        if start_cell is not None and end_cell is not None:
            draw_color(grid, start_cell, end_cell)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
