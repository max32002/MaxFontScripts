import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

def check_ttx_conflicts(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # 紀錄編碼到字形的對應
        code_to_glyph = {}
        # 紀錄字形到編碼的對應
        glyph_to_codes = defaultdict(set)
        
        # 定位到 cmap 內的表格
        for table in root.findall(".//cmap/*[@platformID]"):
            for mapping in table.findall("map"):
                code = mapping.get('code')
                name = mapping.get('name')
                
                # 檢查同一個編碼是否指向不同字形
                if code in code_to_glyph and code_to_glyph[code] != name:
                    print(f"衝突：編碼 {code} 同時指向 {code_to_glyph[code]} 與 {name}")
                
                code_to_glyph[code] = name
                glyph_to_codes[name].add(code)

        print("--- 檢查字形多重映射 ---")
        for name, codes in glyph_to_codes.items():
            if len(codes) > 1:
                print(f"字形 {name} 被多個編碼使用: {', '.join(sorted(codes))}")

    except Exception as e:
        print(f"讀取錯誤: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_ttx_conflicts(sys.argv[1])
    else:
        print("請拖入 .ttx 檔案或輸入路徑")