import halftone as ht
from PIL import Image, ImageChops


class Riso:

    def __init__(self, image_path: str, paper_path = "Paper-Texture-4.jpg", spacing=10):
        self.image_path = image_path
        self.paper_path = paper_path
        self.spacing = spacing

        self.img_name = self.image_path.split(".")[0]

        self.img = Image.open(f'input/{image_path}')
        self.size = (1277, 1280)
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

        # c = ImageChops.multiply(c, k)
        # m = ImageChops.multiply(m, k)
        # y = ImageChops.multiply(y, k)

        c_half = ht.halftone(c, ht.euclid_dot(spacing=self.spacing, angle=15))
        m_half = ht.halftone(m, ht.euclid_dot(spacing=self.spacing, angle=75))
        y_half = ht.halftone(y, ht.euclid_dot(spacing=self.spacing, angle=0))
        k_half = ht.halftone(k, ht.euclid_dot(spacing=self.spacing, angle=45))

        c_half.save(f"output/{self.img_name}_{self.spacing}_cyan.png")
        m_half.save(f"output/{self.img_name}_{self.spacing}_magenta.png")
        y_half.save(f"output/{self.img_name}_{self.spacing}_yellow.png")
        k_half.save(f"output/{self.img_name}_{self.spacing}_black.png")




        cyan = Image.merge('CMYK', [c_half, Image.new('L', self.size),
                                    Image.new('L', self.size),
                                    Image.new('L', self.size)])

        magenta = Image.merge('CMYK', [Image.new('L', self.size), m_half,
                                    Image.new('L', self.size),
                                    Image.new('L', self.size)])

        yellow = Image.merge('CMYK', [Image.new('L', self.size),
                                    Image.new('L', self.size), y_half,
                                    Image.new('L', self.size)])

        black = Image.merge('CMYK', [Image.new('L', self.size),
                                    Image.new('L', self.size),
                                    Image.new('L', self.size), k_half])

        # cyan.convert("RGB").save(f"output/{self.img_name}_{self.spacing}_cyan_colored.png")


        cyan = ImageChops.offset(cyan, xoffset=5, yoffset=-5)
        magenta = ImageChops.offset(magenta, xoffset=4, yoffset=0)

        result = ImageChops.darker(self.paper, yellow.convert("RGB"))
        result = ImageChops.darker(result, cyan.convert("RGB"))
        result = ImageChops.darker(result, magenta.convert("RGB"))
        # result = ImageChops.darker(result, black.convert("RGB"))

        # mask = Image.open("mask.jpg").convert('L')
        # c_half = ImageChops.multiply(c_half, mask)
        # m_half = ImageChops.multiply(m_half, mask)
        # y_half = ImageChops.multiply(y_half, mask)
        # k_half = ImageChops.multiply(k_half, mask)

        # result.save(f"output/{self.img_name}_{self.spacing}_result.png")

        m_half = ImageChops.offset(m_half, xoffset=5, yoffset=-5)
        y_half = ImageChops.offset(y_half, xoffset=4, yoffset=0)

        self.riso = ImageChops.darker(self.paper, Image.merge( 'CMYK', (c_half, m_half, y_half, k_half)).convert("RGB"))


        # self.riso = result
        return self

    def export(self):
        if self.alpha:
            temp = Image.merge("RGBA", [*self.riso.convert("RGB").split(), self.alpha])
        else:
            temp = self.riso.convert("RGB")

        temp.save(f"output/{self.img_name}_{self.spacing}.png")
        # self.riso.convert("RGB").save(f"output/{self.img_name}_{self.spacing}.png")


if __name__ == '__main__':
    Riso("tomato.png", spacing=5, paper_path="white-paper-texture-2.jpg").convert().export()
