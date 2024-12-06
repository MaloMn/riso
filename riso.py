from typing import Tuple
import random

import halftone as ht
from PIL import Image, ImageChops

random.seed(9001)


class Riso:

    def __init__(self, image_path: str, paper_path: str, spacing=10, debug=False):
        self.image_path = image_path
        self.paper_path = paper_path
        self.spacing = spacing
        self.debug = debug

        self.img_name = self.image_path.split(".")[0]

        self.img = Image.open(f'input/{image_path}')
        self.size: Tuple[int, int] = (200, 200)
        self.img = self.img.resize(self.size)

        if len(self.img.split()) == 4:
            _, _, _, self.alpha = self.img.split()
        else:
            self.alpha = None

        self.paper = Image.open(f'paper/{paper_path}')
        self.paper = self.paper.crop((0, 0, *self.size))

        self.riso = None

        print(self.img.size, self.paper.size)

    def convert(self):
        c, m, y, k = self.img.convert('CMYK').split()

        c_half = ht.halftone(c, ht.euclid_dot(spacing=self.spacing, angle=15))
        m_half = ht.halftone(m, ht.euclid_dot(spacing=self.spacing, angle=75))
        y_half = ht.halftone(y, ht.euclid_dot(spacing=self.spacing, angle=0))
        k_half = ht.halftone(k, ht.euclid_dot(spacing=self.spacing, angle=45))

        if self.debug:
            c_half.save(f"output/{self.img_name}_{self.spacing}_cyan.png")
            m_half.save(f"output/{self.img_name}_{self.spacing}_magenta.png")
            y_half.save(f"output/{self.img_name}_{self.spacing}_yellow.png")
            k_half.save(f"output/{self.img_name}_{self.spacing}_black.png")

        max_offset = int(self.size[0] * 0.01)
        a, b, c, d = [random.randint(-max_offset, max_offset) for _ in range(4)]
        m_half = ImageChops.offset(m_half, xoffset=a, yoffset=b)
        y_half = ImageChops.offset(y_half, xoffset=c, yoffset=d)

        self.riso = ImageChops.darker(self.paper, Image.merge( 'CMYK', (c_half, m_half, y_half, k_half)).convert("RGB"))
        return self

    def export(self):
        if self.alpha:
            temp = Image.merge("RGBA", [*self.riso.convert("RGB").split(), self.alpha])
        else:
            temp = self.riso.convert("RGB")

        temp.save(f"output/{self.img_name}_{self.spacing}.png")


if __name__ == '__main__':
    Riso("tomato.png", spacing=1, paper_path="white-paper-texture-2.jpg").convert().export()
