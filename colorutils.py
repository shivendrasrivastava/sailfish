__author__ = 'Shiven'


def color_as_hex(green):
    red = 100
    blue = 120
    color = '{:02x}{:02x}{:02x}'.format(red, green, blue)
    print color


def get_green(years, index):
    green = 256/len(years) * index
    return green