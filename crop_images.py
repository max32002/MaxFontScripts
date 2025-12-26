import argparse
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from PIL import Image

def process_single_image(img_path: Path, output_dir: Path, reverse: bool):
    """處理單張圖片的裁剪與儲存"""
    try:
        # 使用 context manager 確保檔案正確關閉
        with Image.open(img_path) as img:
            width, height = img.size
            
            # 定義裁剪區域 (left, upper, right, lower)
            if reverse:
                crop_area = (width // 2, 0, width, height)
            else:
                crop_area = (0, 0, width // 2, height)
            
            cropped_img = img.crop(crop_area)
            
            # 保持原始格式儲存
            output_path = output_dir / img_path.name
            cropped_img.save(output_path)
            return f"成功: {img_path.name}"
    except Exception as e:
        return f"錯誤: 處理 {img_path.name} 時發生問題 - {e}"

def crop_images(input_dir: str, output_dir: str = "cropped_images", reverse: bool = False):
    # 1. 使用 pathlib 處理路徑，比 os.path 更直觀
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    if not input_path.exists():
        print(f"錯誤：找不到輸入目錄 '{input_dir}'")
        return

    output_path.mkdir(parents=True, exist_ok=True)

    # 2. 篩選圖片檔案
    extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.webp'}
    image_files = [
        f for f in input_path.iterdir() 
        if f.suffix.lower() in extensions
    ]

    if not image_files:
        print("目錄中沒有找到支援的圖片檔案。")
        return

    print(f"開始處理 {len(image_files)} 張圖片...")

    # 3. 使用多進程 (Multi-processing) 加速圖片處理
    # 圖片處理是 CPU 密集型任務，多進程能大幅提升速度
    with ProcessPoolExecutor() as executor:
        # 建立任務列表
        futures = [
            executor.submit(process_single_image, f, output_path, reverse) 
            for f in image_files
        ]
        
        for future in futures:
            print(future.result())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="高效圖片裁剪工具：裁剪左半邊或右半邊。")
    parser.add_argument("--input", "-i", required=True, help="輸入圖片目錄的路徑。")
    parser.add_argument("--output", "-o", default="cropped_images", help="輸出目錄的路徑。")
    parser.add_argument("--reverse", action="store_true", help="若設置則裁剪右半邊，否則裁剪左半邊。")
    
    args = parser.parse_args()
    crop_images(args.input, args.output, args.reverse)