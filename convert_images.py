import os
import argparse
import cv2

def convert_images_opencv_imwrite(input_dir, output_dir, output_format="pbm"):
    """
    將指定輸入目錄中的所有圖片轉換為指定的格式，並保存到輸出目錄中。
    使用 OpenCV (cv2) 進行圖像的讀取和保存 (統一使用 cv2.imwrite)。

    Args:
        input_dir (str): 要處理的輸入目錄路徑。
        output_dir (str): 要保存轉換後檔案的輸出目錄路徑。
        output_format (str): 目標檔案格式 (預設為 "pbm")。
    """
    output_format = output_format.lower()

    for filename in os.listdir(input_dir):
        if is_image_file(filename):
            filepath = os.path.join(input_dir, filename)
            try:
                img = cv2.imread(filepath)
                if img is None:
                    print(f"警告: 無法讀取檔案 '{filename}'。")
                    continue

                name, ext = os.path.splitext(filename)
                output_filename = f"{name}.{output_format}"
                output_path = os.path.join(output_dir, output_filename)

                if output_format == "pbm":
                    # 嘗試使用 OpenCV 保存二值化後的圖像 (可能不是標準 PBM)
                    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    _, binary_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
                    success = cv2.imwrite(output_path, binary_img)
                    if success:
                        #print(f"已嘗試將 '{filename}' 保存為 (二值化後) '{output_filename}' 到 '{output_dir}'")
                        pass
                    else:
                        print(f"錯誤: 無法使用 OpenCV 保存 '{output_filename}' (即使是二值化後)。")
                else:
                    success = cv2.imwrite(output_path, img)
                    if success:
                        print(f"已將 '{filename}' 轉換為 '{output_filename}' 並保存到 '{output_dir}'")
                    else:
                        print(f"錯誤: 無法使用 OpenCV 保存 '{output_filename}'。請檢查 OpenCV 是否支援此格式。")

            except Exception as e:
                print(f"處理 '{filename}' 時發生錯誤: {e}")

def is_image_file(filename):
    """
    檢查檔案名稱是否為常見的圖片檔案格式。
    """
    extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff", ".webp", '.pbm', '.pgm', '.ppm'}
    return any(filename.lower().endswith(ext) for ext in extensions)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="轉換指定輸入目錄中的圖片為指定格式，並保存到輸出目錄中 (使用 OpenCV 的 cv2.imwrite)。")
    parser.add_argument("--input", required=True, help="要轉換圖片的輸入目錄路徑")
    parser.add_argument("--output", required=True, help="要保存轉換後檔案的輸出目錄路徑")
    parser.add_argument("-f", "--format", default="pbm", help="目標檔案格式 (例如: pbm, png, jpg)")

    args = parser.parse_args()
    input_directory = args.input
    output_directory = args.output
    output_format = args.format

    if os.path.isdir(input_directory):
        os.makedirs(output_directory, exist_ok=True) # 確保輸出目錄存在
        convert_images_opencv_imwrite(input_directory, output_directory, output_format)
        print("轉換完成！")
    else:
        print(f"錯誤: 輸入目錄 '{input_directory}' 不存在。")