from manim import *
import pandas as pd


class Maze(Scene):
    def construct(self):
        df = pd.read_csv("mazeastar.csv")
        rows, cols = 6, 6
        square_size = 0.8

        squares = VGroup(*[
            VGroup(*[Square(side_length=square_size, color=GRAY_E, fill_opacity=0.1)
                   for _ in range(cols)])
            for _ in range(rows)
        ])

        for i, row in enumerate(squares):
            for j, square in enumerate(row):
                square.move_to(square_size * DOWN *
                               j + square_size * RIGHT * i)
        squares.set_x(-4).set_y(0)

        descript = Tex(
            r"A* pathfinding", font_size=42)
        descript.set_color('#ffdd00')
        descript[0][0:2].set_color('#ff00ff')
        descript.set_x(0.5).set_y(3.5)

        close = [(0, 1), (2, 1), (2, 2), (1, 2), (0, 2), (0, 3), (1, 3), (1, 4), (1, 5),
                 (2, 5), (2, 4), (3, 5), (4, 5), (4, 4), (5, 4), (4, 3)]

        open = [(0, 0), (0, 1), (2, 1), (2, 2), (1, 2), (0, 2),
                (0, 3), (1, 3), (1, 4), (1, 5), (2, 5),  (2, 4), (2, 3), (3, 5), (4, 5), (5, 5), (4, 4), (5, 4), (5, 3), (4, 3)]

        path = [(2, 1), (2, 2), (1, 2), (0, 2), (0, 3), (1, 3),
                (1, 4), (1, 5), (2, 5), (3, 5), (4, 5), (4, 4), (4, 3)]

        gradient = ['#ffdd00', '#fdcb02', '#fbb905', '#faa807', '#f8960a', '#f6850c',
                    '#f5730f', '#f36111', '#f15014', '#f03e16', '#ee2d19', '#ec1b1b', '#eb0a1e']

        start = self.point(1, 1, '#ffdd00', squares)
        start.set_opacity(1)
        goal = self.point(4, 2, '#ff0000', squares)
        goal.set_opacity(1)

        start_point_text = r'Start'
        start_point = self.declare(
            '#ffdd00', descript, descript, start_point_text)
        end_point_text = r'Goal'
        end_point = self.declare(
            '#ff0000', start_point, descript, end_point_text)
        open_point_text = r'Open set'
        open_point = self.declare(
            '#ff00ff', end_point, descript, open_point_text)
        close_point_text = r'Closed set'
        close_point = self.declare(
            '#ff99ff', open_point, descript, close_point_text)
        path_point_text = r'Found path'
        path_point = self.declare(
            '#ffdd00', close_point, descript, path_point_text)

        distance = Arrow(squares[2][1].get_center(
        ), squares[4][2].get_center(), color=BLUE, stroke_width=4, buff=0.2)
        g_value = DoubleArrow(squares[1][1].get_center(
        ), squares[2][1].get_center(), color=BLUE, buff=-1)
        arrows = VGroup(distance, g_value)

        formula = MathTex(r"f_{n} = g_{n} + h_{n}", font_size=46)
        formula.set_color('#ffdd00')
        formula.set_x(-4).set_y(3)

# f value
        formula_f = MathTex(r"f_{n}", font_size=46)
        formula_f.set_color('#ffdd00')
        formula_f.next_to(path_point, DOWN, buff=0.2)
        formula_f.align_to(descript, LEFT)
        formula_f_text = Tex(
            r"- total path cost", font_size=42)
        formula_f_text.set_color(BLUE)
        formula_f_text.next_to(formula_f, RIGHT, buff=0.5)
        formula_f_value = VGroup(formula_f, formula_f_text)
# g value
        formula_g = MathTex(r"g_{n}", font_size=46)
        formula_g.set_color('#ffdd00')
        formula_g.next_to(formula_f_value, DOWN, buff=0.2)
        formula_g.align_to(descript, LEFT)
        formula_g_text = Tex(
            r"- cost between start cell and n", font_size=42)
        formula_g_text.set_color(BLUE)
        formula_g_text.next_to(formula_g, RIGHT, buff=0.5)
        formula_g_value = VGroup(formula_g, formula_g_text)
# h value
        formula_h = MathTex(r"h_{n}", font_size=46)
        formula_h.set_color('#ffdd00')
        formula_h.next_to(formula_g_value, DOWN, buff=0.2)
        formula_h.align_to(descript, LEFT)
        formula_h_text = Tex(
            r"- heuristic function", font_size=42)
        formula_h_text.set_color(BLUE)
        formula_h_text.next_to(formula_h, RIGHT, buff=0.5)
        formula_h_value = VGroup(formula_h, formula_h_text)
# h value formula
        heuristic = MathTex(
            r"h_{n}=\left| x_{start}-x_{goal}\right|+\left| y_{start}-y_{goal}\right|", font_size=42)
        heuristic.set_color('#ffdd00')
        heuristic.next_to(formula_h_value, DOWN, buff=0.2)
        heuristic.align_to(descript, LEFT)
# n value
        formula_n = MathTex(r"n", font_size=46)
        formula_n.set_color('#ffdd00')
        formula_n.next_to(heuristic, DOWN, buff=0.2)
        formula_n.align_to(descript, LEFT)
        formula_n_text = Tex(
            r"- number of cell", font_size=42)
        formula_n_text.set_color(BLUE)
        formula_n_text.next_to(formula_n, RIGHT, buff=0.5)
        formula_n_value = VGroup(formula_n, formula_n_text)

        self.play(Write(descript))
        self.play(Create(squares))
        self.maze_draw(df, squares)
        self.play(Create(start))
        self.play(Create(start_point))
        self.play(Create(goal))
        self.play(Create(end_point))
        self.play(Create(open_point))
        self.neighbor(open, '#ff00ff', squares, True)
        self.play(Create(arrows), run_time=1.5)
        self.play(Transform(arrows.copy(), formula), run_time=1.5)

        # self.arrows(close, squares)
        self.play(Create(close_point))
        self.neighbor(close, '#ff99ff', squares, True)
        self.play(Create(path_point))
        self.neighbor(path, gradient, squares, False,
                      path=path, gradient=gradient)
        self.play(Transform(formula[0][0:2].copy(),
                            formula_f_value), run_time=1.5)
        self.play(Transform(formula[0][3:5].copy(),
                            formula_g_value), run_time=1.5)
        self.play(Transform(formula[0][6:8].copy(),
                            formula_h_value), run_time=1.5)
        self.play(Transform(formula_h_value.copy(),
                            heuristic), run_time=1.5)
        self.play(Transform(formula[0][2].copy(),
                            formula_n_value), run_time=1.5)
        self.wait(2)

    def declare(self, color, nextto, descript, dtext):
        position = Square(side_length=0.25,
                          color=color, fill_opacity=1)
        position.next_to(nextto, DOWN, buff=0.2)
        position.align_to(descript, LEFT)
        text = Tex(dtext, font_size=42)
        text.next_to(position, RIGHT, buff=0.5)
        text.set_color(color)
        declare = VGroup(position, text)
        return declare

    def neighbor(self, area, color, squares, choice, gradient=None, path=None):
        for index, (col, row) in enumerate(area):
            if choice:
                cell = self.point(col, row, color, squares)
            else:
                if area == path and gradient:
                    cell_color = gradient[index % len(gradient)]
                else:
                    cell_color = color
                cell = self.point(col, row, cell_color, squares)
            opacity = 0.5 if choice else 1
            cell.set_opacity(opacity)
            self.play(Create(cell), run_time=0.1)

    def maze_draw(self, df, squares):
        for index, row in df.iterrows():
            x = row['x']
            y = row['y']
            walls = eval(str(row['walls']))
            self.draw_lines(x, y, walls, squares)

    def draw_lines(self, x, y, walls, squares):
        square = squares[x][y]
        square_coord = square.get_center()
        square_size = square.get_width()
        coordinate = Text(f"{x}, {y}", font_size=20)
        coordinate.move_to(square_coord)
        self.play(FadeIn(coordinate), run_time=0.01)
        if walls['top']:
            start = square_coord + square_size / 2 * UP + square_size / 2 * LEFT
            end = square_coord + square_size / 2 * UP + square_size / 2 * RIGHT
            line = Line(start=start, end=end, color='#00ff00', stroke_width=6)
            self.play(Create(line), run_time=0.01)
        if walls['right']:
            start = square_coord + square_size / 2 * UP + square_size / 2 * RIGHT
            end = square_coord + square_size / 2 * DOWN + square_size / 2 * RIGHT
            line = Line(start=start, end=end, color='#00ff00', stroke_width=6)
            self.play(Create(line), run_time=0.01)
        if walls['bottom']:
            start = square_coord + square_size / 2 * DOWN + square_size / 2 * LEFT
            end = square_coord + square_size / 2 * DOWN + square_size / 2 * RIGHT
            line = Line(start=start, end=end, color='#00ff00', stroke_width=6)
            self.play(Create(line), run_time=0.01)
        if walls['left']:
            start = square_coord + square_size / 2 * UP + square_size / 2 * LEFT
            end = square_coord + square_size / 2 * DOWN + square_size / 2 * LEFT
            line = Line(start=start, end=end, color='#00ff00', stroke_width=6)
            self.play(Create(line), run_time=0.01)

    def point(self, row, col, color, squares):
        square = squares[row][col]
        square_center = square.get_center()
        inner_square_size = 0.4
        point = Square(side_length=inner_square_size,
                       color=color, fill_opacity=0.75)
        point.move_to(square_center)
        return point

    def arrows(self, area, squares):
        for index, (x, y) in enumerate(area):
            distance = Arrow(squares[x][y].get_center(
            ), squares[4][2].get_center(), color=YELLOW, buff=0.2)
            self.play(Create(distance), run_time=0.1)
            self.play(FadeOut(distance), run_time=0.5)
  