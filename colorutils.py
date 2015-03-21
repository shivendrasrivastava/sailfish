__author__ = 'Shiven'


def color_as_hex(green):
    red = 100
    blue = 120
    color = '{:02x}{:02x}{:02x}'.format(red, green, blue)
    print color


def get_green(num_colors, index):
    green = 256/num_colors * index
    return green