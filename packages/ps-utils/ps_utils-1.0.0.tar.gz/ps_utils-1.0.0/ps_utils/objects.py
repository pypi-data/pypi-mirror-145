from pathlib import Path
import numpy as np
import cv2
from ps_utils.converters import cm2px


class Image():

    def __init__(self, path):
        self.__path = Path(path)
        self.__make_tests()
        self.array = cv2.imread(str(self.__path))

    def __make_tests(self):
        if not Path(self.__path).exists():
            raise self.Error('This image path not exists')

    class Error(Exception):

        def __init__(self, text):
            super().__init__(text)


class Sheet():

    __ALLOWED_SIZES = ['A4']
    __SIZES_IN_PIXELS = {
        'A4': {
            'width': cm2px(21),
            'height': cm2px(29.7),
        },
    }

    def __init__(self, size='A4'):
        self.__size = str(size).upper()
        self.__make_tests()
        self.width = self.__SIZES_IN_PIXELS[self.__size]['width']
        self.height = self.__SIZES_IN_PIXELS[self.__size]['height']
        self.array = np.full((self.height, self.width, 3), 255)

    def __make_tests(self):
        if self.__size not in self.__ALLOWED_SIZES:
            raise self.Error('This size is not allowed')

    class Error(Exception):

        def __init__(self, text):
            super().__init__(text)
