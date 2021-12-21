from __future__ import annotations
from dataclasses import dataclass

class Image:

    @classmethod
    def blank_image(self, h: int, w: int, default_pixel: str = "."):
        return Image(h=h, w=h, default_pixel=default_pixel)

    @classmethod
    def from_matrix(self, image: list[str], default_pixel: str = "."):
        return Image(image=image, default_pixel=default_pixel)

    def __init__(self, h=None, w=None,
                 image=None, default_pixel="."):
        if image is not None:
            self.image = list(map(list, image))
            self.height = len(image)
            self.width = len(image[0])
            self.default_pixel = default_pixel
        else:
            self.height = h
            self.width = w
            self.image = [[default_pixel] * w for _ in range(h)]
            self.default_pixel = default_pixel

    def set_pixel(self, x: int, y: int, val: str):
        assert(len(val) == 1)
        self.image[x][y] = val

    def get_pixel(self, x: int, y: int):
        return self.image[x][y]

    def extend_image(self, mag: int):
        new_h = self.height + 2 * mag
        new_w = self.width + 2 * mag
        new_image = [[self.default_pixel] * new_w for _ in range(new_h)]
        for i in range(self.height):
            for j in range(self.width):
                new_image[i + 2][j + 2] = self.image[i][j]
        self.image = new_image
        self.height = new_h
        self.width = new_w

    def count(self, pixel: str):
        ans = [1 if self.image[i][j] == pixel else 0
               for i in range(self.height)
               for j in range(self.width)]
        ans = sum(ans)
        return ans

    def __str__(self):
        v = "Image object with height = {}, width = {}, default_pixel = {}\n" \
            .format(self.height, self.width, self.default_pixel)
        v += '\n'.join([''.join(line) for line in self.image])
        return v

    def __repr__(self):
        return self.__str__()


@dataclass
class ImageEnhancementTechnique:
    pattern: str

    def _number_to_pixel(self, value):
        assert(value < 512)
        return self.pattern[value]

    def _pixel_neighbour_to_number(self, image: Image, x: int, y: int):
        ans = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                shifted_x = x + dx
                shifted_y = y + dy
                pixel = image.get_pixel(shifted_x, shifted_y)
                ans = ans * 2 + (1 if pixel == '#' else 0)
        return ans

    def enhance(self, image: Image):
        image.extend_image(2)
        bkg_num = 511 if image.default_pixel == '#' else 0
        enhanced_image = Image.blank_image(image.height - 2, image.width - 2,
                                           self._number_to_pixel(bkg_num))
        for i in range(enhanced_image.height):
            for j in range(enhanced_image.width):
                num = self._pixel_neighbour_to_number(image, i + 1, j + 1)
                pixel = self._number_to_pixel(num)
                enhanced_image.set_pixel(i, j, pixel)

        return enhanced_image


input_file = 'input1'
with open(input_file) as f:
    pattern = f.readline().strip()
    iet = ImageEnhancementTechnique(pattern)

    f.readline()
    image_matrix = [line.strip() for line in f.readlines()]
    image = Image.from_matrix(image_matrix)

for _ in range(50):
    image = iet.enhance(image)
print(image)
print(image.count('#'))