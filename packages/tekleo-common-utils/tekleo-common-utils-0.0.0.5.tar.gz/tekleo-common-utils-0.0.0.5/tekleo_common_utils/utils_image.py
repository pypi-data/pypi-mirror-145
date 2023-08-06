from PIL import Image as image_pil_main
from PIL.Image import Image
import cv2
import numpy
from numpy import ndarray
from injectable import injectable


@injectable
class UtilsImage:
    def convert_image_pil_to_image_cv(self, image_pil: Image) -> ndarray:
        return cv2.cvtColor(numpy.array(image_pil), cv2.COLOR_RGB2BGR)

    def convert_image_cv_to_image_pil(self, image_cv: ndarray) -> Image:
        return image_pil_main.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))

    def open_image_pil(self, image_path: str) -> Image:
        return image_pil_main.open(image_path)

    def open_image_cv(self, image_path: str) -> ndarray:
        return self.convert_image_pil_to_image_cv(self.open_image_pil(image_path))

    def save_image_pil(self, image_pil: Image, image_path: str) -> str:
        image_pil.save(image_path)
        return image_path

    def debug_image_cv(self, image_cv: ndarray, window_name: str = 'Debug Image'):
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.imshow(window_name, image_cv)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


