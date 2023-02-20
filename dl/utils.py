from PIL import Image
import io


def tiff_to_jpeg_on_memory(tiff_path):
    with Image.open(tiff_path) as im:
        with io.BytesIO() as buffer:
            im.convert('RGB').save(buffer, format='JPEG')
            return buffer.getvalue()
