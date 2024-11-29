import os
import sys
import termios
import tty

class TUI:
    def __init__(self):
        self.running = True
        self.screen = []
        self.width = 80
        self.height = 40
        self.old_settings = termios.tcgetattr(sys.stdin)
        self.screen = [[' ' for _ in range(self.width)] for _ in range(self.height)]

    def __enter__(self):
        sys.stdout.write("\033[?1049h")
        sys.stdout.flush()
        tty.setraw(sys.stdin.fileno())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.write("\033[?1049l")
        sys.stdout.flush()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def draw(self):
        sys.stdout.write("\033[2J")
        sys.stdout.write("\033[H")
        sys.stdout.flush()

        for row in self.screen:
            sys.stdout.write(''.join(row) + '\r\n')
        sys.stdout.flush()
        
        self.screen = [[' ' for _ in range(self.width)] for _ in range(self.height)]

    def add_text(self, x, y, text):
        if 0 <= y < self.height:
            row = self.screen[y]
            for i, char in enumerate(text):
                if 0 <= x + i < self.width:
                    row[x + i] = char

    def get_key(self):
        return sys.stdin.read(1)

    def run(self):
        while self.running:
            self.add_text(2, 2, "Welcome to the TUI with Alternative Buffer!")
            self.add_text(2, 4, "Press 'q' to quit")
            self.add_text(2, 6, "Test from other line")
            self.add_text(0, 0, "-" * (self.width-1))
            self.add_text(0, self.height-1, "-" * (self.width-1))
            for i in range(self.height):
                self.add_text(0, i, "|")
                self.add_text(self.width-1, i, "|")
            self.draw()
            
            key = self.get_key()
            if key.lower() == 'q':
                self.running = False

if __name__ == "__main__":
    with TUI() as tui:
        tui.run()
