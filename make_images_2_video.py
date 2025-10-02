import cv2
import os


def images_to_video(image_folder, output_video, frame_rate=25):
    # 获取目录下的所有图片文件并排序
    images = [
        img
        for img in os.listdir(image_folder)
        if img.endswith((".png", ".jpg", ".jpeg"))
    ]
    images.sort()  # 确保按文件名排序
    images = images[1000:1500]  # 从第1000张开始取500张图片

    # 如果目录下没有足够的图片，报错退出
    if len(images) < 500:
        print(
            f"Error: Found only {len(images)} images in the range, need at least 500 images."
        )
        return

    # 读取第一张图片来获取视频的宽度和高度
    first_image_path = os.path.join(image_folder, images[0])
    first_image = cv2.imread(first_image_path)
    height, width, layers = first_image.shape

    # 初始化视频编码器（这里使用 MJPEG 编码，保存为 .avi 格式）
    fourcc = cv2.VideoWriter_fourcc(*"h264")
    video = cv2.VideoWriter(output_video, fourcc, frame_rate, (width, height))

    # 将每一张图片写入视频
    for image in images:
        image_path = os.path.join(image_folder, image)
        img = cv2.imread(image_path)
        video.write(img)

    # 释放视频文件
    video.release()
    print(f"Video saved as {output_video}")


# 设置图片目录和输出视频路径
image_folder = "./process"  # 图片文件夹路径
output_video = "./my_process_particle_video.mp4"  # 输出视频文件路径
frame_rate = 20  # 每秒帧数

images_to_video(image_folder, output_video, frame_rate)
