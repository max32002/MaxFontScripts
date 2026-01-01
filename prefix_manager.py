import argparse
from pathlib import Path

def rename_files(folder_path, action, value, ext_filter=None, preview=False):
    target_dir = Path(folder_path)
    
    if not target_dir.is_dir():
        print(f"找不到目錄：{folder_path}")
        return

    for file_path in target_dir.iterdir():
        if file_path.is_file():
            if ext_filter and file_path.suffix.lower() != ext_filter.lower():
                continue
                
            old_name = file_path.name
            
            if action == "add":
                new_name = f"{value}{old_name}"
            elif action == "remove":
                new_name = old_name[value:]
            
            if new_name and new_name != old_name:
                if preview:
                    print(f"預覽：{old_name} -> {new_name}")
                else:
                    try:
                        file_path.rename(file_path.with_name(new_name))
                        print(f"已更名：{old_name} -> {new_name}")
                    except Exception as e:
                        print(f"更名失敗 {old_name}: {e}")
    
    if preview:
        print("預覽結束，檔案未實際修改")
    else:
        print("處理完成")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批次修改檔案名稱並支援預覽")
    parser.add_argument("action", choices=["add", "remove"], help="執行動作：add 或 remove")
    parser.add_argument("--input", "-i", default=".", help="目標目錄")
    parser.add_argument("--prefix", "-p", default="", help="要增加的前綴字串")
    parser.add_argument("--length", "-l", type=int, default=0, help="要移除的前綴長度")
    parser.add_argument("--ext", "-e", help="指定副檔名")
    parser.add_argument("--preview", action="store_true", help="開啟預覽模式，不實際更名")
    args = parser.parse_args()

    if args.action == "add" and not args.prefix:
        print("錯誤：使用 add 時必須提供 --prefix")
    else:
        param = args.prefix if args.action == "add" else args.length
        rename_files(args.input, args.action, param, args.ext, args.preview)