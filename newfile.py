# ----------------------------------------------------------
# Author   : SK Sahil
# GitHub   : https://github.com/Sahil-pixel
# Project  : KvLab
# Requires : Kivy >= 2.3.0, Python >= 3.10
# For Educational Use Only
# Do not directly copy this code for commercial use.
# Learn from it, and build your own projects.
# ----------------------------------------------------------
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty
from kivy.factory import Factory

KV = '''
<TileButton@Button>:
    font_size: 32
    size: dp(60), dp(60)
    size_hint: None, None
    background_normal: ''
    background_down: ''
    background_color: 0, 0, 0, 0
    color: 1, 1, 1, 1
    canvas.before:
        PushMatrix
        Color:
            rgba: 0, 1, 1, 0.4 if self.state == 'normal' else 0.9
        RoundedRectangle:
            size: self.size[0] + 10, self.size[1] + 10
            pos: self.x - 5, self.y - 5
            radius: [20]
        Color:
            rgba: (0.2, 0.7, 1, 1) if self.state == 'normal' else (1, 0.4, 0.4, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [15]
        PopMatrix

<MainWidget>:
    status: "Turn: X"
    canvas.before:
        Color:
            rgba: 0.05, 0.05, 0.08, 1
        Rectangle:
            pos: self.pos
            size: self.size
    FloatLayout:
        BoxLayout:
            orientation: 'vertical'
            size_hint: None, None
            size: self.minimum_size
            pos_hint: {'center_x': 0.5, 'center_y': 0.6}
            spacing: dp(10)

            Label:
                text: root.status
                font_size: 28
                color: 0.8, 0.8, 1, 1
                size_hint: None, None
                size: self.texture_size

            GridLayout:
                id: grid
                cols: 3
                rows: 3
                spacing: dp(8)
                size_hint: None, None
                size: self.minimum_size

            Button:
                text: "Restart"
                font_size: 20
                size_hint: None, None
                size: dp(180), dp(40)
                background_normal: ''
                background_color: (0.2, 0.9, 0.5, 1)
                color: 0, 0, 0, 1
                on_press: root.reset()
'''

Builder.load_string(KV)


class MainWidget(BoxLayout):
    status = StringProperty("Turn: X")
    board = ListProperty([["" for _ in range(3)] for _ in range(3)])
    turn = "X"
    buttons = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_board()

    def init_board(self):
        self.buttons.clear()
        self.board = [["" for _ in range(3)] for _ in range(3)]
        grid = self.ids.grid
        grid.clear_widgets()

        for i in range(3):
            row = []
            for j in range(3):
                btn = Factory.TileButton()
                btn.bind(on_press=self.make_move)
                grid.add_widget(btn)
                row.append(btn)
            self.buttons.append(row)

    def make_move(self, btn):
        if btn.text != "":
            return
        btn.text = self.turn
        i, j = self.get_btn_pos(btn)
        self.board[i][j] = self.turn
        if self.check_winner(self.turn):
            self.status = f"{self.turn} wins!"
            self.disable_all()
        elif self.is_draw():
            self.status = "It's a draw!"
        else:
            self.turn = "O" if self.turn == "X" else "X"
            self.status = f"Turn: {self.turn}"

    def get_btn_pos(self, btn):
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j] == btn:
                    return i, j
        return -1, -1

    def check_winner(self, symbol):
        for i in range(3):
            if all(self.board[i][j] == symbol for j in range(3)):
                return True
            if all(self.board[j][i] == symbol for j in range(3)):
                return True
        if all(self.board[i][i] == symbol for i in range(3)):
            return True
        if all(self.board[i][2 - i] == symbol for i in range(3)):
            return True
        return False

    def is_draw(self):
        return all(self.board[i][j] != "" for i in range(3) for j in range(3))

    def disable_all(self):
        for row in self.buttons:
            for btn in row:
                btn.disabled = True

    def reset(self):
        self.turn = "X"
        self.status = "Turn: X"
        self.init_board()


class GlowingCenteredTicTacToeApp(App):
    def build(self):
        return MainWidget()


if __name__ == '__main__':
    GlowingCenteredTicTacToeApp().run()
