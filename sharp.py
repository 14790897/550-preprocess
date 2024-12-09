import cv2
import numpy as np


def apply_bilateral_filter(image, config):
    """使用双边滤波，减少噪点的同时保留边缘"""
    return cv2.bilateralFilter(
        image, config["d"], config["sigma_color"], config["sigma_space"]
    )


def apply_contrast_enhancement(image, config):
    """增强对比度（CLAHE）"""
    clahe = cv2.createCLAHE(
        clipLimit=config["clip_limit"], tileGridSize=config["tile_grid_size"]
    )
    return clahe.apply(image)


def apply_thresholding(image, config):
    """自适应阈值分割：区分背景和粒子"""
    return cv2.adaptiveThreshold(
        image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        config["block_size"],
        config["c_value"],
    )


def apply_sharpening(image, config):
    """锐化处理，增强粒子效果"""
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)


def apply_median_filter(image):
    """中值滤波去除噪点"""
    return cv2.medianBlur(image, 3)


def apply_gaussian_filter(image, kernel_size=(5, 5), sigma_x=0):
    """使用高斯滤波进行去噪处理"""
    return cv2.GaussianBlur(image, kernel_size, sigma_x)


def apply_morphological_opening(image, kernel_size=3):
    """使用形态学开运算去除噪点"""
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# 处理步骤和参数的配置
pipeline_config = {
    "gaussian_filter": {"kernel_size": (5, 5), "sigma_x": 1},
    "bilateral_filter": {"d": 9, "sigma_color": 75, "sigma_space": 75},
    "contrast_enhancement": {"clip_limit": 2.0, "tile_grid_size": (8, 8)},
    "thresholding": {"block_size": 11, "c_value": 2},
    "sharpening": {},  # 锐化暂时不需要参数
}


def process_image(image_path, output_path, config):
    # 读取图像
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = apply_gaussian_filter(image, **config["gaussian_filter"])
    image = apply_bilateral_filter(image, config["bilateral_filter"])
    # image = apply_median_filter(image)
    image = apply_contrast_enhancement(image, config["contrast_enhancement"])

    image = apply_thresholding(image, config["thresholding"])

    image = apply_sharpening(image, config["sharpening"])
    image = apply_morphological_opening(image, kernel_size=4)

    # 显示与保存图像
    cv2.imshow("Processed Image", image)
    cv2.imwrite(output_path, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 调用处理图像
process_image("1.jpg", "denoised_sharpened_image.jpg", pipeline_config)
