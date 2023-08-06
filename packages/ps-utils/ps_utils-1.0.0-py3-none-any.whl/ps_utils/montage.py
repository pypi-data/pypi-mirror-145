import cv2
from pathlib import Path
from ps_utils.converters import cm2px
from ps_utils.objects import Sheet


class MontageMaker():

    def __init__(self, **kwargs):
        self.__sheet = Sheet()
        self.__images = []
        self.__images_width = cm2px(kwargs.get('images_width', 6.5))
        self.__images_height = cm2px(kwargs.get('images_height', 6.5))
        self.current_number_of_images = 0
        self.__set_total_number_of_images()
        self.__set_gap()
        self.__download_directory = Path(
            kwargs.get('download_directory', Path.home() / 'Downloads')
        )
        self.__make_tests()

    @property
    def sheet(self):
        return self.__sheet

    @property
    def images_width(self):
        return self.__images_width

    @property
    def images_height(self):
        return self.__images_height

    @property
    def download_directory(self):
        return self.__download_directory

    @sheet.setter
    def sheet(self, value):
        self.__sheet = value
        self.__make_tests()
        self.__set_total_number_of_images()
        self.__set_gap()

    @images_width.setter
    def images_width(self, value):
        self.__images_width = cm2px(value)
        self.__make_tests()
        self.__set_total_number_of_images()
        self.__set_gap()
        self.__images = []

    @images_height.setter
    def images_height(self, value):
        self.__images_height = cm2px(value)
        self.__make_tests()
        self.__set_total_number_of_images()
        self.__set_gap()
        self.__images = []

    @download_directory.setter
    def download_directory(self, value):
        self.__download_directory = Path(value)
        self.__make_tests()

    def __set_total_number_of_images(self):
        self.__number_of_columns = self.sheet.width // self.images_width
        self.__number_of_rows = self.sheet.height // self.images_height
        self.total_number_of_images = (
            self.__number_of_columns * self.__number_of_rows
        )

    def __set_gap(self):
        self.__set_column_gap()
        self.__set_row_gap()

    def __set_column_gap(self):
        total_gap = (
            self.sheet.width - self.images_width * self.__number_of_columns
        )
        number_of_gaps = self.__number_of_columns - 1
        self.__column_gap = total_gap // number_of_gaps

    def __set_row_gap(self):
        total_gap = (
            self.sheet.height - self.images_height * self.__number_of_rows
        )
        number_of_gaps = self.__number_of_rows - 1
        self.__row_gap = total_gap // number_of_gaps

    def add_image(self, image, amount):
        image.amount = amount
        self.current_number_of_images += amount
        image.array = cv2.resize(
            image.array, (self.images_width, self.images_height)
        )
        self.__images.append(image)
        self.__make_tests()

    def make_montage(self):
        self.__current_column = 0
        self.__current_row = 0
        self.__place_images()
        self.__write_final_image()
        self.__images = []

    def __place_images(self):
        for image in self.__images:
            self.__place_image(image)

    def __place_image(self, image):
        while image.amount > 0:
            y1 = (
                self.__current_row * self.images_height
                + self.__current_row * self.__row_gap
            )
            y2 = y1 + self.images_height
            x1 = (
                self.__current_column * self.images_width
                + self.__current_column * self.__column_gap
            )
            x2 = x1 + self.images_width
            self.sheet.array[y1:y2, x1:x2] = image.array
            self.__change_position()
            image.amount -= 1

    def __change_position(self):
        if self.__current_column == self.__number_of_columns - 1:
            self.__current_column = 0
            self.__current_row += 1
        elif self.__current_column != self.__number_of_columns - 1:
            self.__current_column += 1

    def __write_final_image(self):
        cv2.imwrite(
            str(self.download_directory / 'final_image.png'),
            self.sheet.array,
        )

    def __make_tests(self):
        if not isinstance(self.sheet, Sheet):
            raise self.Error('Invalid sheet')
        if self.images_width > self.sheet.width or self.images_width <= 0:
            raise self.Error('Invalid images width')
        if self.images_height > self.sheet.height or self.images_height <= 0:
            raise self.Error('Invalid images height')
        if not self.download_directory.exists():
            raise self.Error('This download directory not exists')
        total_amount = sum([image.amount for image in self.__images])
        if total_amount > self.total_number_of_images:
            image = self.__images.pop()
            self.current_number_of_images -= image.amount
            raise self.Error('Invalid images amount')

    class Error(Exception):

        def __init__(self, text):
            super().__init__(text)
