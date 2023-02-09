from PIL import Image, ImageOps
import pytesseract


class OCR:
    def __init__(self, image: Image.Image) -> None:
        self.image = image

    def _preprocessImage(self):
        if self.image.mode == 'RGBA':
            r, g, b, _ = self.image.split()
            rgb_image = Image.merge('RGB', (r, g, b))

            self.image = ImageOps.invert(rgb_image)
        else:
            self.image = ImageOps.invert(self.image)

    def _getTextFromImage(self):
        self.txt = pytesseract.image_to_string(
            self.image, lang="eng", config="--psm 7")
        return self.txt

    def _processText(self):
        self.txt = self.txt.strip()
        self.txt = "".join(self.txt.split())
        return self.txt

    def getText(self):
        self._preprocessImage()
        self._getTextFromImage()
        self._processText()
        return self.txt
