import cv2
import numpy as np
import argparse
import os
from glob import glob

def reduce_ink_bleeding(img_bin, kernel_size=3):
    """
    使用形態學操作減少筆畫暈染黏連。
    img_bin: 黑底白字 (0/255) 的二值圖
    """
    # 建立結構元素 (3x3 十字型或矩形)
    # 十字型 (cv2.MORPH_CROSS) 對於分離筆畫效果較好，且較不會過度削弱轉角
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (kernel_size, kernel_size))
    
    # 執行「開運算」：先腐蝕（切斷細小連結）後膨脹（還原主體粗細）
    # 這對於處理筆畫間的細微暈染非常有效
    processed = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernel, iterations=1)
    
    # 如果暈染嚴重，可以再進行一次輕微的腐蝕來增加筆畫間距
    # processed = cv2.erode(processed, kernel, iterations=1)
    
    return processed

def apply_pattern_cleaning_fast(img_bin, patterns_list):
    """
    快速 Pattern 清理，確保 1:1 像素對齊
    """
    processed = img_bin.copy()
    for pattern, replacement in patterns_list:
        diff_mask = (pattern != replacement)
        for i in range(4):
            p_rot = np.rot90(pattern, k=i)
            r_rot = np.rot90(replacement, k=i)
            d_rot = np.rot90(diff_mask, k=i)
            
            res = cv2.matchTemplate(processed, p_rot, cv2.TM_SQDIFF)
            loc = np.where(res == 0)
            
            h, w = p_rot.shape
            for pt in zip(*loc[::-1]):
                x, y = pt
                roi = processed[y:y+h, x:x+w]
                roi[d_rot] = r_rot[d_rot]
    return processed

def get_patterns():
    """清理特定的像素雜點樣式"""
    p = []
    r = []
    p.append(np.array([
        [0, 0, 0],
        [0, 1, 0],
        [1, 1, 1]
    ], dtype=np.uint8))
    r.append(np.array([
        [0, 0, 0],
        [0, 0, 0],
        [1, 1, 1]
    ], dtype=np.uint8))

    p.append(np.array([
        [0, 0, 0],
        [0, 1, 0],
        [0, 1, 0],
        [1, 1, 1]
    ], dtype=np.uint8))
    r.append(np.array([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [1, 1, 1]
    ], dtype=np.uint8))

    p.append(np.array([
        [0, 0, 0],
        [0, 1, 0],
        [1, 1, 0],
        [1, 1, 0]
    ], dtype=np.uint8))
    r.append(np.array([
        [0, 0, 0],
        [0, 0, 0],
        [1, 1, 0],
        [1, 1, 0]
    ], dtype=np.uint8))

    p.append(np.array([
        [0, 0, 0],
        [0, 1, 0],
        [0, 1, 1],
        [0, 1, 1]
    ], dtype=np.uint8))
    r.append(np.array([
        [0, 0, 0],
        [0, 0, 0],
        [0, 1, 1],
        [0, 1, 1]
    ], dtype=np.uint8))

    p.append(np.array([
        [1, 1, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 0, 0]
    ], dtype=np.uint8))
    r.append(np.array([
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 1, 0, 0]
    ], dtype=np.uint8))

    raw_patterns = []
    for idx in range(len(p)):
        raw_patterns.append( (p[idx], r[idx]))

    return [(np.array(p, dtype=np.uint8), np.array(r, dtype=np.uint8)) for p, r in raw_patterns]

# 超採樣中值濾波平滑化 ---
def apply_blue(cleaned):
    # 取得原始尺寸
    h, w = cleaned.shape[:2]
    
    # (A) 放大 2 倍 (使用線性插值 cv2.INTER_LINEAR 使邊緣稍微柔化)
    img_upscaled = cv2.resize(cleaned, (w * 2, h * 2), interpolation=cv2.INTER_LINEAR)
    
    # (B) 套用微量中值濾波 (ksize=3 是最小單位，能有效去除單像素鋸齒)
    # 中值濾波能保護邊緣位置不位移，只剔除突出的噪點
    img_smoothed = cv2.medianBlur(img_upscaled, 3)
    
    # (C) 縮小回原尺寸 (使用 cv2.INTER_AREA 對縮小最友好，能產生高質量的抗鋸齒效果)
    # 此時邊緣會帶有微量的灰階，能讓視覺上更平滑
    final_bin = cv2.resize(img_smoothed, (w, h), interpolation=cv2.INTER_AREA)
    
    # 如果你希望最後輸出依然是純黑白 (無灰階)，可以取消下面這行的註解：
    _, final_bin = cv2.threshold(final_bin, 127, 255, cv2.THRESH_BINARY)

    return final_bin

def process_file(input_path, output_path, patterns):
    # 1. 讀取並轉為黑底白字
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None: return
    _, img_bin = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    # 2. 【核心】減少暈染：分離黏連的筆畫
    # kernel_size=3 是最安全的選擇，若暈染嚴重可改用 5
    img_bin = reduce_ink_bleeding(img_bin, kernel_size=3)

    # 3. 執行 Pattern 清理 (處理特定細節)
    patterns_255 = [(p * 255, r * 255) for p, r in patterns]
    cleaned = apply_pattern_cleaning_fast(img_bin, patterns_255)

    # 4. blur
    final_bin = apply_blue(cleaned)

    final_bin = apply_pattern_cleaning_fast(final_bin, patterns_255)

    # 5. 轉回白底黑字輸出
    final_output = cv2.bitwise_not(final_bin)
    cv2.imwrite(output_path, final_output)
    print(f"處理完成: {os.path.basename(output_path)}")

def main():
    parser = argparse.ArgumentParser(description='減少筆畫暈染並清理雜點')
    parser.add_argument('--input', '-i', required=True)
    parser.add_argument('--output', '-o')
    args = parser.parse_args()

    patterns = get_patterns()
    
    # 處理資料夾或單一檔案
    if os.path.isdir(args.input):
        in_dir = args.input
        out_dir = args.output if args.output else f"{in_dir.rstrip('/')}_clean"
        os.makedirs(out_dir, exist_ok=True)
        files = []
        for ext in ('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff'):
            files.extend(glob(os.path.join(in_dir, ext)))
    else:
        files = [args.input]
        out_dir = None

    for f in files:
        if out_dir:
            out_f = os.path.join(out_dir, os.path.basename(f))
        else:
            base, ext = os.path.splitext(f)
            out_f = f"{base}_clean{ext}" if not args.output else args.output
        process_file(f, out_f, patterns)

if __name__ == "__main__":
    main()
