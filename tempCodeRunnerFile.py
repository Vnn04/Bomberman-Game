import pygame
import os

# Lấy thư mục hiện tại
current_dir = os.path.dirname(__file__)

# Đường dẫn đến file ảnh
image_path = os.path.join(current_dir, "background.png")

# Load ảnh từ file
background_image = pygame.image.load(image_path)

# Kiểm tra xem ảnh có load thành công không
if background_image is None:
    print("Không thể load ảnh từ file: " + image_path)
else:
    print("Load ảnh thành công!")