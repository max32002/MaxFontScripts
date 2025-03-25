import os
import argparse
from PIL import Image

def crop_images(input_dir, output_dir="cropped_images", reverse=False):
    """
    裁剪輸入目錄中的圖片，並將結果儲存到輸出目錄。

    Args:
        input_dir (str): 輸入圖片目錄的路徑。
        output_dir (str, optional): 輸出目錄的路徑。預設為 "cropped_images"。
        reverse (bool, optional): 如果為 True，則裁剪右半邊的圖片。預設為 False。
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            filepath = os.path.join(input_dir, filename)
            try:
                img = Image.open(filepath)
                width, height = img.size
                if reverse:
                    crop_area = (width // 2, 0, width, height)
                else:
                    crop_area = (0, 0, width // 2, height)
                cropped_img = img.crop(crop_area)
                output_path = os.path.join(output_dir, filename)
                cropped_img.save(output_path)
                print(f"已裁剪並儲存：{output_path}")
            except Exception as e:
                print(f"處理 {filename} 時發生錯誤：{e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="裁剪圖片的左半邊或右半邊。")
    parser.add_argument("--input", required=True, help="輸入圖片目錄的路徑。")
    parser.add_argument("--output", default="cropped_images", help="輸出目錄的路徑。")
    parser.add_argument("--reverse", action="store_true", help="裁剪右半邊的圖片。")
    args = parser.parse_args()

    crop_images(args.input, args.output, args.reverse)