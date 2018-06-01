import numpy as np
import cv2
from skimage.morphology import skeletonize
import matplotlib.pyplot as plt
from skimage import img_as_ubyte

def _floodfill(image):
    ret, thresh1 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    bw = np.asarray(thresh1, dtype=np.bool)
    skeleton = skeletonize(bw)
    if __name__ == "__main__":
        fig, axes = plt.subplots(2, 1, figsize=(8, 8), sharex=True, sharey=True)
        ax = axes.ravel()
        ax[0].imshow(image, cmap=plt.cm.gray, interpolation='nearest')
        ax[0].set_title('original')
        ax[0].axis('off')
        ax[1].imshow(skeleton, cmap=plt.cm.gray, interpolation='nearest')
        ax[1].set_title('skeleton')
        ax[1].axis('off')
        fig.tight_layout()
        plt.show()
    return skeleton

if __name__ == "__main__":
    src = cv2.imread("../image/www.png", cv2.THRESH_BINARY)
    bw2 =  _floodfill(src)
    wimage = img_as_ubyte(bw2)
    cv2.imwrite("../image/wwws4.png", wimage)

