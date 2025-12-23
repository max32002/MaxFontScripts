import os
import argparse

# 設定指令列參數
parser = argparse.ArgumentParser(description="根據字元編碼刪除 PNG 檔案")
parser.add_argument("--path", default=".", help="目標資料夾路徑")
parser.add_argument("--string", help="直接輸入要轉換的中文字串")
parser.add_argument("--file", help="指定包含中文字的文字檔路徑")
args = parser.parse_args()

target_path = args.path
keyword_content = ""

# 決定字串來源：優先使用指令列輸入，其次使用檔案
if args.string:
    keyword_content = args.string
elif args.file:
    if os.path.isfile(args.file):
        with open(args.file, 'r', encoding='utf-8') as f:
            keyword_content = f.read().strip()
    else:
        print(f"錯誤：找不到檔案 {args.file}")

# 開始執行刪除動作
if keyword_content:
    if os.path.exists(target_path):
        for char in keyword_content:
            # 跳過空白字元
            if char.isspace():
                continue
            
            # 轉換字元為編碼並組合檔名
            code = ord(char)
            filename = f"{code}.png"
            file_path = os.path.join(target_path, filename)
            
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    print(f"已刪除：{filename} (字元：{char})")
                except Exception as e:
                    print(f"刪除 {filename} 時發生錯誤：{e}")
            else:
                print(f"跳過：檔案 {filename} 不存在")
    else:
        print(f"錯誤：路徑 {target_path} 不存在")
else:
    print("提示：請提供 --string 或 --file 參數")