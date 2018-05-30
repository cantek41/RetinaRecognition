import cv2

def image_process(img):
    img = cv2.resize(img, (256, 256))
    laplacian = cv2.Laplacian(img, cv2.CV_64FC4)
    return laplacian


reader = cv2.imread('image/A01_1.jpg', cv2.IMREAD_GRAYSCALE)
reader = image_process(reader)
cv2.imwrite("image/img.jpg", reader)
cv2.imshow("img", reader)
cv2.waitKey(0)
cv2.destroyAllWindows()

