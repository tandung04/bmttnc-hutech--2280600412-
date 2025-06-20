import sys
from PIL import Image

def encode_image(image_path, message):
    img = Image.open(image_path)
    width, height = img.size

    # Chuyển message thành chuỗi bit (8-bit mỗi ký tự)
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    # Thêm delimiter (chuỗi đánh dấu kết thúc)
    binary_message += '1111111111111110'  # 16-bit kết thúc

    data_index = 0
    binary_message_len = len(binary_message)

    for row in range(height):
        for col in range(width):
            if data_index >= binary_message_len:
                break  # Đã ẩn hết dữ liệu

            pixel = list(img.getpixel((col, row)))

            for color_channel in range(3):  # RGB channels
                if data_index < binary_message_len:
                    # Thay thế bit cuối của mỗi màu bằng bit của message
                    pixel[color_channel] = (pixel[color_channel] & ~1) | int(binary_message[data_index])
                    data_index += 1

            img.putpixel((col, row), tuple(pixel))

        if data_index >= binary_message_len:
            break

    encoded_image_path = 'encoded_image.png'
    img.save(encoded_image_path)
    print("Steganography complete. Encoded image saved as", encoded_image_path)


def main():
    if len(sys.argv) != 3:
        print("Usage: python encrypt.py <image_path> <message>")
        return

    image_path = sys.argv[1]
    message = sys.argv[2]
    encode_image(image_path, message)


if __name__ == "__main__":
    main()
