import argparse
from pathlib import Path
from PIL import Image

def resize_image(input_path, width, ext, output_path):
    try:
        with Image.open(input_path) as img:
            # 計算新尺寸
            target_width = width if width > 0 else img.size[0]
            ratio = target_width / float(img.size[0])
            new_height = int(float(img.size[1]) * ratio)
            
            resized_img = img.resize((target_width, new_height), Image.Resampling.LANCZOS)

            # 處理副檔名轉換與模式相容性
            target_ext = ext.strip(".") if ext else input_path.suffix.strip(".")
            save_format = target_ext.upper()
            if save_format == "JPG":
                save_format = "JPEG"

            # 如果要存成 JPEG 但原圖有透明層，需轉換模式
            if save_format == "JPEG" and resized_img.mode in ("RGBA", "P"):
                resized_img = resized_img.convert("RGB")

            # 確保輸出路徑的資料夾存在
            output_path = Path(output_path).with_suffix(f".{target_ext}")
            output_path.parent.mkdir(parents=True, exist_ok=True)

            resized_img.save(output_path, format=save_format)
            print(f"處理完成：{output_path}")
    except Exception as e:
        print(f"跳過檔案 {input_path}，錯誤：{e}")

def main():
    parser = argparse.ArgumentParser(description="圖片批次縮放工具")
    parser.add_argument("input", help="輸入檔案或資料夾路徑")
    parser.add_argument("-w", "--width", type=int, default=0, help="新的寬度，設為 0 則保持原寬度")
    parser.add_argument("-e", "--ext", help="新的副檔名")
    parser.add_argument("-p", "--postfix", type=str, default="_resized", help="後綴")
    parser.add_argument("-o", "--output", type=str, default="", help="輸出路徑或檔名")

    args = parser.parse_args()
    input_path = Path(args.input)

    if not input_path.exists():
        print("路徑不存在")
        return

    valid_exts = {'.jpg', '.jpeg', '.png', '.pbm', '.pgm', '.ppm', '.bmp', '.tif', '.tiff', '.webp'}

    if input_path.is_dir():
        # 處理資料夾
        output_folder = Path(args.output) if args.output else input_path / "resized"
        for file in input_path.iterdir():
            if file.suffix.lower() in valid_exts:
                target_path = output_folder / file.name
                resize_image(file, args.width, args.ext, target_path)
    
    elif input_path.is_file():
        # 處理單一檔案
        if args.output:
            target_path = Path(args.output)
        else:
            new_name = f"{input_path.stem}{args.postfix}{input_path.suffix}"
            target_path = input_path.parent / new_name
        
        resize_image(input_path, args.width, args.ext, target_path)

if __name__ == "__main__":
    main()