from window import Window
from constants import WINDOW_HEIGHT, WINDOW_WIDTH


def main() -> None:
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)
    window.run()


if __name__ == "__main__":
    main()
