# from sharp_ import process_image
from contrast import process_image
import os


def process_images_in_directory(directory, output_directory, config):
    """对目录下的所有JPEG文件进行处理"""
    os.makedirs(output_directory, exist_ok=True)
    for filename in os.listdir(directory):
        if filename.lower().endswith(".jpg"):
            image_path = os.path.join(directory, filename)
            print(f'{image_path}')
            output_path = os.path.join(output_directory, "processed_" + filename)
            process_image(image_path, output_path, config)


def rename_files_in_directory(directory):
    """遍历目录，去掉文件名中的'相机'"""
    for filename in os.listdir(directory):
        # 检查文件名中是否包含 '相机'
        if "相机" in filename:
            # 构建新文件名，移除 '相机'
            new_filename = filename.replace("相机", "")
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_filename)

            # 重命名文件
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
input_directory = "550-y\Y2-550\相机No.1_C001H001S0001"  # 替换为实际的图像目录路径  "550-y\Y2-550\相机No.1_C001H001S0001" "550-y\Y1-550\C001H001S0001"
output_directory = "processed_y2_550"  # 自定义输出目录

rename_files_in_directory(input_directory)
process_images_in_directory(input_directory, output_directory, pipeline_config)
