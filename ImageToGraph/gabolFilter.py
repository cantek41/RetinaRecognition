import numpy as np
import cv2
from skimage.morphology import skeletonize
import matplotlib.pyplot as plt
from skimage import img_as_ubyte

def _floodfill(image):
    ret, thresh1 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    # b = imageToBinary.extract_bv(src)
    bw = np.asarray(thresh1, dtype=np.bool)
    skeleton = skeletonize(bw)

    # cv2.imshow("skeleton", cv2.resize(skeleton, (600, 600)))

    # thinned = thin(image)
    # thinned_partial = thin(image, max_iter=25)
    # cv2.imshow("thinned", cv2.resize(thinned, (600, 600)))
    # cv2.imshow("thinned_partial", cv2.resize(thinned_partial, (600, 600)))
    if __name__ == "__main__":
        fig, axes = plt.subplots(2, 2, figsize=(8, 8), sharex=True, sharey=True)
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
    # cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    bw2 =  _floodfill(src)
    # bw2 = skeletonize(bw)
    # print(bw2)

    wimage = img_as_ubyte(bw2)
    # wimage = cv2.imdecode(bw2, cv2.THRESH_BINARY)
    # cv2.imshow("src", cv2.resize(bw2, (600, 600)))
    # cv2.imshow("thinning",cv2.resize(bw2, (600, 600)))
    cv2.imwrite("../image/wwws4.png", wimage)
    # cv2.waitKey()

