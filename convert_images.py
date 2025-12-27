import cv2
import numpy as np
import argparse
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# 設定日誌 (調整為 WARNING 級別，避免 INFO 訊息干擾進度條顯示)
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

def resize_image(img, target_width: int = None, target_height: int = None):
    """
    根據目標寬高調整圖片大小，保持縱橫比或強制拉伸。
    """
    h, w = img.shape[:2]
    new_w, new_h = w, h

    if target_width and target_height:
        # 如果同時指定寬高，強制拉伸到該尺寸
        new_w, new_h = target_width, target_height
    elif target_width:
        # 只指定寬度，計算等比例高度
        scale = target_width / w
        new_w = target_width
        new_h = int(h * scale)
    elif target_height:
        # 只指定高度，計算等比例寬度
        scale = target_height / h
        new_h = target_height
        new_w = int(w * scale)

    # 只有當尺寸有變化時才進行 resize
    if (new_w, new_h) != (w, h):
        # 選擇插值方法：縮小時用 INTER_AREA 效果較好，放大時用 INTER_LINEAR
        interpolation = cv2.INTER_AREA if (new_w * new_h < w * h) else cv2.INTER_LINEAR
        resized_img = cv2.resize(img, (new_w, new_h), interpolation=interpolation)
        return resized_img
    return img

def process_single_image(input_path: Path, output_dir: Path, output_format: str, width: int = None, height: int = None):
    """處理單張圖片：讀取 -> Resize(可選) -> 格式轉換 -> 儲存"""
    try:
        # 解決 OpenCV 不支援中文路徑的問題 (使用 numpy 讀取)
        img_array = np.fromfile(str(input_path), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if img is None:
            logging.warning(f"跳過損壞或無法讀取的檔案: {input_path.name}")
            return False

        # --- 新增功能：調整圖片大小 ---
        img = resize_image(img, width, height)
        # ---------------------------

        # 準備輸出路徑
        output_filename = input_path.with_suffix(f".{output_format}").name
        output_path = output_dir / output_filename

        # 針對 PBM 格式的特殊處理
        if output_format.lower() == "pbm":
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, final_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
        else:
            final_img = img

        # 解決 OpenCV 不支援中文路徑的儲存問題
        ext = f".{output_format}"
        is_success, buffer = cv2.imencode(ext, final_img)
        if is_success:
            with open(output_path, "wb") as f:
                f.write(buffer)
            return True
        else:
            logging.error(f"OpenCV 編碼失敗: {input_path.name} -> {output_format}")
            return False

    except Exception as e:
        logging.error(f"處理 {input_path.name} 時發生異常: {e}")
        return False

def batch_convert(input_dir: str, output_dir: str, output_format: str, max_workers: int, width: int = None, height: int = None):
    """批量轉換入口，加入多執行緒與 tqdm 進度條"""
    input_path_obj = Path(input_dir)
    output_path_obj = Path(output_dir)
    output_path_obj.mkdir(parents=True, exist_ok=True)

    # 定義支援的輸入副檔名
    extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff", ".webp", ".pbm", ".pgm", ".ppm"}
    
    # 篩選檔案清單
    image_files = [
        f for f in input_path_obj.iterdir() 
        if f.is_file() and f.suffix.lower() in extensions
    ]

    total_files = len(image_files)
    if total_files == 0:
        print("在輸入目錄中找不到可處理的圖片檔案。")
        return

    print(f"準備處理 {total_files} 張圖片，輸出格式: {output_format}...")
    if width or height:
         print(f"目標尺寸: 寬={width if width else 'Auto'}, 高={height if height else 'Auto'}")

    success_count = 0

    # 使用 ThreadPoolExecutor 進行並行處理
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任務，並獲取 futures 列表
        futures = {
            executor.submit(process_single_image, file, output_path_obj, output_format, width, height): file
            for file in image_files
        }

        # --- tqdm 顯示進度條 ---
        # as_completed 會在任務完成時產生 yield，配合 tqdm 實現即時更新
        tqdm_iterator = tqdm(as_completed(futures), total=total_files, desc="轉換進度", unit="張", dynamic_ncols=True)
        
        for future in tqdm_iterator:
            try:
                result = future.result()
                if result:
                    success_count += 1
            except Exception as e:
                file_path = futures[future]
                logging.error(f"{file_path.name} 執行時發生未捕捉的錯誤: {e}")
        # ------------------------------------

    print(f"\n任務完成！成功轉換: {success_count}/{total_files}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="進階圖片批量轉換工具 (支援並行處理、Resize、進度顯示)")
    parser.add_argument("-i", "--input", required=True, help="輸入目錄路徑")
    parser.add_argument("-o", "--output", required=True, help="輸出目錄路徑")
    parser.add_argument("-f", "--format", default="pbm", help="目標格式 (如: pbm, png, jpg，預設 pbm)")
    parser.add_argument("-w", "--workers", type=int, default=4, help="並行執行緒數量 (預設 4)")
    
    # 新增 Resize 相關參數
    parser.add_argument("--width", type=int, default=None, help="目標圖片寬度 (選填，若只填一邊則保持比例)")
    parser.add_argument("--height", type=int, default=None, help="目標圖片高度 (選填，若只填一邊則保持比例)")

    args = parser.parse_args()

    if Path(args.input).is_dir():
        # 確保已安裝 tqdm
        try:
            from tqdm import tqdm  # 修改這裡
        except ImportError:
            print("錯誤: 請先安裝 'tqdm'。執行: pip install tqdm")
            exit(1)

        batch_convert(args.input, args.output, args.format, args.workers, args.width, args.height)
    else:
        print(f"錯誤: 輸入目錄 '{args.input}' 不存在。")