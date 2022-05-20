import numpy as np
import cv2 as cv


def draw_rec(image, width, height, label, number):
    (H, W) = image.shape[:2]
    rec = (H, W)
    COLORS = np.random.randint(0, 255, size=2, dtype="uint8")
    color = [int(c) for c in COLORS]

    (w, h) = (width, height)
    (x, y) = (int((rec[1] - width) / 2), int((rec[0] - height) / 2))

    cv.rectangle(img=image, pt1=(x, y), pt2=(x + w, y + h), color=color[0], thickness=2)

    text = "{}:{:.3f}".format(label, number)
    cv.putText(image, text, (x, y - 5), cv.FONT_HERSHEY_COMPLEX, fontScale=0.5, color=color[1], thickness=1)


if __name__ == '__main__':
    imagePath = "./pic.jpg"
    image = cv.imread(imagePath)

    # 画矩形
    width = 250
    height = 80
    draw_rec(image, width, height, "zhangphil@csdn", 2019)

    width = 250
    height = 80
    draw_rec(image, width, height, "zhangphil@csdn", 2019)

    width = 250
    height = 80
    draw_rec(image, width, height, "zhangphil@csdn", 2019)

    width = 250
    height = 80
    draw_rec(image, width, height, "zhangphil@csdn", 2019)

    width = 250
    height = 80
    draw_rec(image, width, height, "zhangphil@csdn", 2019)

    width = 250
    height = 80
    draw_rec(image, width, height, "zhangphil@csdn", 2019)

    width = 250
    height = 80
    draw_rec(image, width, height, "zhangphil@csdn", 2019)

    width = 250
    height = 80
    draw_rec(image, width, height, "zhangphil@csdn", 2019)

    cv.imshow("pic", image)
    cv.waitKey(0)