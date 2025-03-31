import argparse
import os
import logging
import cv2
from tqdm import tqdm

def convert_image_to_binary_gray(input_path, output_path, threshold=127, antialiasing=0):
    """使用 OpenCV 轉換單一圖片為二進制灰度模式。"""
    try:
        img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            logging.error(f"無法讀取圖片：{input_path}")
            return False

        if antialiasing > 0:
            img = cv2.GaussianBlur(img, (antialiasing, antialiasing), 0)

        _, binary_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
        cv2.imwrite(output_path, binary_img)
        #logging.info(f"已轉換：{input_path} -> {output_path}")
        return True
    except Exception as e:
        logging.error(f"轉換 {input_path} 時發生錯誤：{e}")
        return False

def convert_images_in_directory(input_dir, output_dir=None, threshold=127, antialiasing=0):
    """轉換目錄中的所有圖片。"""
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.bmp', '.gif', '.tif', '.tiff'))]

    for filename in tqdm(image_files, desc="轉換進度"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename) if output_dir else input_path
        convert_image_to_binary_gray(input_path, output_path, threshold, antialiasing)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="將圖片檔案轉換為二進制灰度模式。")
    parser.add_argument("input_dir", help="輸入目錄路徑。")
    parser.add_argument("--output_dir", help="輸出目錄路徑。如果未提供，則覆蓋原始檔案。")
    parser.add_argument("--threshold", type=int, default=127, help="二值化閾值，預設值為 127。")
    parser.add_argument("--antialiasing", type=int, default=0, help="反鋸齒處理強度，預設值為 0 (不套用)。")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    convert_images_in_directory(args.input_dir, args.output_dir, args.threshold, args.antialiasing)
