import os
import sys
import termios
import tty

class TUI:
    def __init__(self):
        self.running = True
        self.screen = []
        self.width = 40
        self.height = 20
        self.old_settings = termios.tcgetattr(sys.stdin)

    def __enter__(self):
        self.activate_alt_buffer()
        self.enable_raw_mode()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.deactivate_alt_buffer()
        self.disable_raw_mode()

    def activate_alt_buffer(self):
        sys.stdout.write("\033[?1049h")
        sys.stdout.flush()

    def deactivate_alt_buffer(self):
        sys.stdout.write("\033[?1049l")
        sys.stdout.flush()

    def enable_raw_mode(self):
        tty.setraw(sys.stdin.fileno())

    def disable_raw_mode(self):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def clear_screen(self):
        sys.stdout.write("\033[2J")
        sys.stdout.write("\033[H")
        sys.stdout.flush()

    def draw(self):
        self.clear_screen()
        for row in self.screen:
            sys.stdout.write(''.join(row) + '\r\n')
        sys.stdout.flush()

    def update_screen(self):
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
            self.update_screen()
            self.add_text(0, 0, "Welcome to the TUI with Alternative Buffer!")
            self.add_text(0, 2, "Press 'q' to quit")
            self.add_text(0, 4, "Test from other line")
            self.draw()
            
            key = self.get_key()
            if key.lower() == 'q':
                self.running = False

if __name__ == "__main__":
    with TUI() as tui:
        tui.run()
