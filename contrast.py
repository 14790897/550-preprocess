import cv2
import numpy as np


def enhance_contrast(image, alpha=2, beta=20):  # alpha Y图像可以用2.5然后X图像用2
    """
    增强图像对比度
    alpha: 对比度控制（1.0-3.0），值越大对比度越高
    beta: 亮度控制（0-100），调整图像整体的亮度
    """
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)


def enhance_exposure(image, gamma=2):
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
    """
    对比度限制自适应直方图均衡化 (CLAHE)
    输入：BGR 彩色图像或灰度图像
    输出：增强后的灰度图像
    """
    # 如果是彩色图像，转换为灰度图
    if len(image.shape) == 3 and image.shape[2] == 3:  # 检查是否是彩色图像
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 创建 CLAHE 对象
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))

    # 应用 CLAHE
    enhanced_image = clahe.apply(image)

    return enhanced_image


def sharpen_image(image):
    # 定义一个锐化核
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    # 使用滤波器进行锐化
    sharpened = cv2.filter2D(image, -1, kernel)
    return sharpened


def sharpen_after_gaussian(image, kernel_size=(5, 5), sigma=1.0):
    # 高斯滤波去噪
    smoothed = cv2.GaussianBlur(image, kernel_size, sigmaX=sigma)

    # 锐化图像
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])  # 锐化核
    image = cv2.filter2D(smoothed, -1, kernel)
    return image


def adjust_hsv_properties(
    image, saturation_scale=1.2, hue_shift=10, brightness_scale=1.2
):
    """
    调整图像的饱和度、色调和亮度
    image: 输入的 BGR 图像
    saturation_scale: 饱和度调整倍数（>1 增强，<1 减弱）
    hue_shift: 色调偏移量（取值范围 -180 到 180）
    brightness_scale: 亮度调整倍数（>1 增亮，<1 减暗）
    """
    # 转换为 HSV 空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 拆分 HSV 通道
    h, s, v = cv2.split(hsv)

    # 调整饱和度
    s = cv2.multiply(s, saturation_scale)
    s = np.clip(s, 0, 255).astype(np.uint8)  # 防止溢出

    # 调整色调
    h = (h + hue_shift) % 180  # 色调范围为 [0, 180]，需要取模处理

    # 调整亮度
    v = cv2.multiply(v, brightness_scale)
    v = np.clip(v, 0, 255).astype(np.uint8)  # 防止溢出

    # 合并调整后的通道
    hsv_adjusted = cv2.merge([h, s, v])

    # 转回 BGR 空间
    adjusted_image = cv2.cvtColor(hsv_adjusted, cv2.COLOR_HSV2BGR)
    return adjusted_image


def apply_s_curve_contrast(image, alpha=1.0, beta=0.5):
    """
    使用S曲线增强图像对比度。

    参数：
    - image: 输入图像，BGR格式（OpenCV默认）。
    - alpha: 控制S曲线的陡峭程度（默认值1.0，值越大对比度越强）。
    - beta: 控制曲线的拐点（范围0-1，默认值0.5，中心点位置）。

    返回：
    - result: 处理后的图像。
    """
    # 检查输入图像是否是彩色图像或灰度图
    if len(image.shape) == 2:  # 灰度图
        is_gray = True
        img = image.copy()
    else:  # 彩色图
        is_gray = False
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 归一化到0-1范围
    img_normalized = img / 255.0

    # 应用S曲线： f(x) = 1 / (1 + exp(-alpha * (x - beta)))
    s_curve = 1 / (1 + np.exp(-alpha * (img_normalized - beta)))

    # 恢复到0-255范围
    result = (s_curve * 255).astype(np.uint8)

    if not is_gray:  # 如果是彩色图，将结果合并回BGR格式
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

    return result


def unsharp_masking(img, ksize=5, sigma=1.0, amount=1.5, threshold=0):
    # 应用高斯模糊
    blurred = cv2.GaussianBlur(img, (ksize, ksize), sigma)
    # 计算锐化掩模
    sharpened = float(amount + 1) * img - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    return sharpened


def process_image(image_path, output_path, config=None):
    # 读取图像
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    image_original = image.copy()  # 保留原始图像
    # image = enhance_contrast_CLAHE(image)
    # image = sharpen_after_gaussian(image, kernel_size=(5, 5), sigma=1.0)
    # image = unsharp_masking(image)
    image = enhance_contrast(image)
    # image = sharpen_image(image)
    # image = enhance_exposure(image, gamma=2)
    # image = adjust_hsv_properties(
    #     image, saturation_scale=3, hue_shift=15, brightness_scale=1.1
    # )
    # image = apply_s_curve_contrast(image, alpha=8.0, beta=0.5)

    image_show = np.hstack((image_original, image))

    # # 显示与保存图像
    # cv2.imshow("Processed Image", image_show)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imwrite(output_path, image)


# 调用处理图像
process_image("1.jpg", "xdenoised_sharpened_image.jpg")
