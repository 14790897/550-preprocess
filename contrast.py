import cv2
import numpy as np


def enhance_contrast(image, alpha=2, beta=30):
    """
    增强图像对比度
    alpha: 对比度控制（1.0-3.0），值越大对比度越高
    beta: 亮度控制（0-100），调整图像整体的亮度
    """
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)


def enhance_exposure(image, gamma=2.0):
    """
    增强曝光度
    gamma: 曝光度参数，值小于1.0时图像变亮，值大于1.0时图像变暗
    """
    inv_gamma = 1.0 / gamma
    table = np.array(
        [(i / 255.0) ** inv_gamma * 255 for i in np.arange(0, 256)]
    ).astype("uint8")
    return cv2.LUT(image, table)


def enhance_contrast_CLAHE(image):
    # 对比度限制自适应直方图均衡化
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(image)


def process_image(image_path, output_path, config=None):
    # 读取图像
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image_original = image.copy()  # 保留原始图像
    # image = enhance_contrast_CLAHE(image)
    image = enhance_contrast(image)
    # image = enhance_exposure(image)
    image = np.hstack((image_original, image))

    # 显示与保存图像
    cv2.imshow("Processed Image", image)
    cv2.imwrite(output_path, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 调用处理图像
process_image("1.jpg", "denoised_sharpened_image.jpg")
