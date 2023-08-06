import builtins

import pygame as pg
import PyQt5


def __test__():
    builtins.print(
        module,
        NoneType,
        function,
        inf,
        isNone(None),
        take_first_item([0, 1, 2]),
        bin_id(bin_id),
        printNoLn(1, 2, 3),
        print(4, 5, 6)

    )


module = type(pg)
NoneType = type(None)
function = type(__test__)
inf = float('inf')

class colors:
    red = '#FF0000' #
    orange = 'FF7F00'
    yellow = '#ffff00'
    green = '#00FF00' #
    aqua = '#00FFFF'
    blue = '#0000FF' #
    purple = '#FF00FF'
    magenta = '#E4007F'



def isNone(data):
    if data is None:
        return True
    if data is not None:
        return False


def take_first_item(data):
    try:
        return data[0]

    except:
        raise TypeError("Expected str,list or tuple type")


def bin_id(tid):
    return bin(id(tid))


def printNoLn(*args, sep=' ', end='', file=None):
    builtins.print(args, sep, end, file)


if __name__ == '__main__':
    __test__()
