from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

class ColorPrinter:
    def __init__(self):
        self.color_actions = {
            Color.RED: (self.print_red, ()),
            Color.GREEN: (self.print_green, ("extra_argument",)),
            Color.BLUE: (self.print_blue, (1, 2, 3)),
        }

    def print_color(self, color_enum):
        action = self.color_actions.get(color_enum)
        if action:
            function, args = action
            function(*args)
        else:
            self.print_unknown()

    def print_red(self):
        print("Printing in red color.")

    def print_green(self, extra_argument):
        print(f"Printing in green color with extra argument: {extra_argument}")

    def print_blue(self, arg1, arg2, arg3):
        print(f"Printing in blue color with arguments: {arg1}, {arg2}, {arg3}")

    def print_unknown(self):
        print("Unknown color.")

# Example usage:
printer = ColorPrinter()

# Call the method with an enum value
printer.print_color(Color.RED)
printer.print_color(Color.GREEN)
printer.print_color(Color.BLUE)
