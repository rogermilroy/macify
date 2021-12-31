from enum import Enum


class AspectRatio:
    __slots__ = ["width", "height", "ratio"]
    width: int
    height: int

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ratio = self.width / self.height


class ScreenDimension:
    __slots__ = ["width", "height", "menubar_height", "corrected_height"]
    width: int
    height: int
    menubar_height: int

    def __init__(self, width, height, menubar_height):
        self.width = width
        self.height = height
        self.menubar_height = menubar_height
        self.corrected_height = height - menubar_height


class Screen(Enum):
    MacBookPro_16_2021_BigSur: ScreenDimension(width=3456, height=2234, menubar_height=74)
    MacBookPro_14_2021_BigSur: ScreenDimension(width=3024, height=1964, menubar_height=74)
