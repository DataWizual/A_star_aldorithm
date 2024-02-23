from manim import *
import pandas as pd


class Maze(Scene):
    def construct(self):
        df = pd.read_csv("mazemanim.csv")
        df_1 = pd.read_csv("mazemanimhalf.csv")
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
            r"Maze drawing using csv file", font_size=40)
        descript.set_color('#ffdd00')
        descript[0][16:19].set_color('#ff00ff')
        descript.set_x(1.5).set_y(3)

        self.play(Write(descript))
        self.play(Create(squares))
        self.maze_read(df_1, squares)
        self.maze_draw(df, squares)
        self.wait(2)

    def maze_read(self, df_1, squares):
        descript = Tex(
            r"x, y, walls", font_size=30)
        descript.set_color('#ffffff')
        descript.set_x(0).set_y(2.5)
        self.play(Write(descript))
        count = 2
        for index, row in df_1.iterrows():
            x = row['x']
            y = row['y']
            walls = eval(str(row['walls']))
            self.read_lines(x, y, walls, squares, count)
            count -= 0.5

    def read_lines(self, x, y, walls, squares, y_coor):
        square = squares[x][y]
        square_coord = square.get_center()
        square_size = square.get_width()
        coordinate = Text(f"{x}, {y}", font_size=20)
        coordinate_position = [-0.5, y_coor, 0]
        coordinate_copy = coordinate.copy()
        coordinate.move_to(coordinate_position)
        coordinate_copy.move_to(square_coord)
        self.play(FadeIn(coordinate))
        self.play(FadeIn(coordinate_copy))
        top_coords = None
        if walls['top']:
            text_0 = Tex(r"\{", font_size=30)
            text_0.set_color("#ffdd00")
            text_1 = Tex(r"top: ", r"True", font_size=28)
            text_1[0].set_color("#ffffff")
            text_1[1].set_color("#00ff00")
            text_1.next_to(text_0, RIGHT, buff=0.1)
            text = VGroup(text_0, text_1)
            text.next_to(coordinate, RIGHT, buff=0.2)
            start = square_coord + square_size / 2 * UP + square_size / 2 * LEFT
            end = square_coord + square_size / 2 * UP + square_size / 2 * RIGHT
            line = Line(start=start, end=end, color='#00ff00', stroke_width=10)
            self.play(FadeIn(text))
            self.play(Transform(text_1.copy(), line))
            top_coords = text.get_right()
        else:
            text_0 = Tex(r"\{", font_size=30)
            text_0.set_color("#ffdd00")
            text_0.next_to(coordinate, RIGHT, buff=0.2)
            text_1 = Tex(r"top: ", r"False", font_size=28)
            text_1[0].set_color("#ffffff")
            text_1[1].set_color("#ef3817")
            text_1.next_to(text_0, RIGHT, buff=0.1)
            text = VGroup(text_0, text_1)
            text.next_to(coordinate, RIGHT, buff=0.2)
            self.play(FadeIn(text))
            top_coords = text.get_right()
        right_coords = None
        if walls['right']:
            text = Tex(r"right: ", r"True,", font_size=28)
            text[0].set_color("#ffffff")
            text[1].set_color("#00ff00")
            text.next_to(top_coords, RIGHT, buff=0.2)
            start = square_coord + square_size / 2 * UP + square_size / 2 * RIGHT
            end = square_coord + square_size / 2 * DOWN + square_size / 2 * RIGHT
            line = Line(start=start, end=end, color='#00ff00', stroke_width=10)
            self.play(FadeIn(text))
            self.play(Transform(text.copy(), line))
            right_coords = text.get_right()
        else:
            text = Tex(r"right: ", r"False,", font_size=28)
            text[0].set_color("#ffffff")
            text[1].set_color("#ef3817")
            text.next_to(top_coords, RIGHT, buff=0.2)
            self.play(FadeIn(text))
            right_coords = text.get_right()
        bottom_coords = None
        if walls['bottom']:
            text = Tex(r"bottom: ", r"True,", font_size=28)
            text[0].set_color("#ffffff")
            text[1].set_color("#00ff00")
            text.next_to(right_coords, RIGHT, buff=0.2)
            start = square_coord + square_size / 2 * DOWN + square_size / 2 * LEFT
            end = square_coord + square_size / 2 * DOWN + square_size / 2 * RIGHT
            line = Line(start=start, end=end, color='#00ff00', stroke_width=10)
            self.play(FadeIn(text))
            self.play(Transform(text.copy(), line))
            bottom_coords = text.get_right()
        else:
            text = Tex(r"bottom: ", r"False,", font_size=28)
            text[0].set_color("#ffffff")
            text[1].set_color("#ef3817")
            text.next_to(right_coords, RIGHT, buff=0.2)
            self.play(FadeIn(text))
            bottom_coords = text.get_right()
        if walls['left']:
            text_0 = Tex(r"left: ", r"True", font_size=28)
            text_0[0].set_color("#ffffff")
            text_0[1].set_color("#00ff00")
            text_1 = Tex(r"\}", font_size=30)
            text_1.set_color("#ffdd00")
            text_1.next_to(text_0, RIGHT, buff=0.1)
            text = VGroup(text_0, text_1)
            text.next_to(bottom_coords, RIGHT, buff=0.2)
            start = square_coord + square_size / 2 * UP + square_size / 2 * LEFT
            end = square_coord + square_size / 2 * DOWN + square_size / 2 * LEFT
            line = Line(start=start, end=end, color='#00ff00', stroke_width=10)
            self.play(FadeIn(text))
            self.play(Transform(text_0.copy(), line))
        else:
            text_0 = Tex(r"left: ", r"False", font_size=28)
            text_0[0].set_color("#ffffff")
            text_0[1].set_color("#ef3817")
            text_1 = Tex(r"\}", font_size=30)
            text_1.set_color("#ffdd00")
            text_1.next_to(text_0, RIGHT, buff=0.1)
            text = VGroup(text_0, text_1)
            text.next_to(bottom_coords, RIGHT, buff=0.2)
            self.play(FadeIn(text))

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
            line = Line(start=start, end=end, color='#00ff00', stroke_width=10)
            self.play(Create(line), run_time=0.05)

        if walls['right']:
            start = square_coord + square_size / 2 * UP + square_size / 2 * RIGHT
            end = square_coord + square_size / 2 * DOWN + square_size / 2 * RIGHT
            line = Line(start=start, end=end, color='#00ff00', stroke_width=10)
            self.play(Create(line), run_time=0.05)

        if walls['bottom']:
            start = square_coord + square_size / 2 * DOWN + square_size / 2 * LEFT
            end = square_coord + square_size / 2 * DOWN + square_size / 2 * RIGHT
            line = Line(start=start, end=end, color='#00ff00', stroke_width=10)
            self.play(Create(line), run_time=0.05)

        if walls['left']:
            start = square_coord + square_size / 2 * UP + square_size / 2 * LEFT
            end = square_coord + square_size / 2 * DOWN + square_size / 2 * LEFT
            line = Line(start=start, end=end, color='#00ff00', stroke_width=10)
            self.play(Create(line), run_time=0.05)
