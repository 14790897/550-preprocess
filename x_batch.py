# from sharp_ import process_image
from contrast import process_image
from PIL import Image  # 用于 TIFF 转换为 JPEG
import os


def tiff_to_jpeg(directory, output_directory):
    """将目录下的所有TIFF文件转换为JPEG文件"""
    os.makedirs(output_directory, exist_ok=True)
    count = 0
    for filename in os.listdir(directory):
        if filename.lower().endswith(".tif") or filename.lower().endswith(".tiff"):
            tiff_path = os.path.join(directory, filename)
            jpeg_path = os.path.join(
                output_directory, os.path.splitext(filename)[0] + ".jpg"
            )
            with Image.open(tiff_path) as img:
                rotated_img = img.convert("RGB").rotate(-90, expand=True)
                rotated_img.save(jpeg_path, "JPEG")
            count += 1
            print(f"已将 {tiff_path} 转换为 {jpeg_path}")
            if count >= 1500:  # 仅处理前500张
                break


def process_images_in_directory(directory, output_directory, config):
    """对目录下的所有JPEG文件进行处理（仅前500张）"""
    os.makedirs(output_directory, exist_ok=True)
    count = 0
    for filename in os.listdir(directory):
        if filename.lower().endswith(".jpg"):
            image_path = os.path.join(directory, filename)
            print(f"处理图像: {image_path}")
            output_path = os.path.join(output_directory, f"x-{count + 1}.jpg")
            process_image(image_path, output_path, config)
            count += 1
            if count >= 1500:  # 仅处理前500张
                break


def rename_files_in_directory(directory):
    """遍历目录，去掉文件名中的'相机'"""
    for filename in os.listdir(directory):
        if "相机" in filename:  # 检查文件名中是否包含 '相机'
            new_filename = filename.replace("相机", "")  # 移除 '相机'
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_filename)
            os.rename(old_file, new_file)
            print(f"已将文件 {filename} 重命名为 {new_filename}")


# 处理步骤和参数的配置
pipeline_config = {
    "gaussian_filter": {"kernel_size": (5, 5), "sigma_x": 1},
    "bilateral_filter": {"d": 9, "sigma_color": 75, "sigma_space": 75},
    "contrast_enhancement": {"clip_limit": 2.0, "tile_grid_size": (8, 8)},
    "thresholding": {"block_size": 11, "c_value": 2},
    "sharpening": {},  # 锐化暂时不需要参数
}

# 使用示例，指定你的目录路径
input_directory = r"x-550\x1-550\Acq_A_001"  # 替换为实际的图像目录路径
jpeg_directory = "jpeg_x"  # 存放转换后的JPEG文件
processed_directory = "processed_x"  # 存放处理后的图像

# 执行处理
rename_files_in_directory(input_directory)  # 重命名文件
tiff_to_jpeg(input_directory, jpeg_directory)  # 将TIFF转换为JPEG
process_images_in_directory(
    jpeg_directory, processed_directory, pipeline_config
)  # 处理前500张JPEG文件
