import cv2
import numpy as np
import argparse
import os
from glob import glob
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial

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

# PS: fast 造成部份 shape 無法 match, 因此改用 hit_miss
def apply_pattern_cleaning_fast(img_bin, patterns_list):
    """
    優化後的 Pattern 清理：確保處理後依然是二值圖
    修正了長方形 Pattern 旋轉後維度不匹配的問題
    """
    processed = img_bin.copy()
    for pattern, replacement in patterns_list:
        # 確保 pattern 是 uint8 且值為 0 或 255
        p_255 = (pattern > 0).astype(np.uint8) * 255
        r_255 = (replacement > 0).astype(np.uint8) * 255
        
        for i in range(4):
            # 旋轉 Pattern 與其對應的替換內容
            p_rot = np.rot90(p_255, k=i)
            r_rot = np.rot90(r_255, k=i)
            
            # 獲取旋轉後的實際高度與寬度
            curr_h, curr_w = p_rot.shape
            
            # 使用 matchTemplate 找出 100% 匹配的地方
            res = cv2.matchTemplate(processed, p_rot, cv2.TM_SQDIFF)
            
            # 找出精確匹配 (SQDIFF 接近 0)
            loc = np.where(res <= 0) 
            
            for pt in zip(*loc[::-1]):
                x, y = pt
                # 使用旋轉後的 curr_h, curr_w 進行切片賦值
                processed[y:y+curr_h, x:x+curr_w] = r_rot
                
    return processed

def apply_pattern_cleaning_hitmiss(img_bin, patterns_list):
    processed = img_bin.copy()
    img_h, img_w = processed.shape
    
    for pattern, replacement in patterns_list:
        # 1 代表找白點，-1 代表找黑點
        hm_kernel = np.where(pattern > 0, 1, -1).astype(np.int8)
        
        for i in range(4):
            p_rot = np.rot90(hm_kernel, k=i)
            r_rot = np.rot90(replacement, k=i)
            
            # 執行 Hit-or-Miss 變換
            hit_mask = cv2.morphologyEx(processed, cv2.MORPH_HITMISS, p_rot)
            
            # 找到匹配點的座標
            loc = np.where(hit_mask > 0)
            h, w = p_rot.shape
            offset_y, offset_x = h // 2, w // 2
            
            for y, x in zip(*loc):
                start_y = y - offset_y
                start_x = x - offset_x
                end_y = start_y + h
                end_x = start_x + w
                
                # 關鍵修正：確保替換範圍完全在影像邊界內
                # fix: 處理檔案時發生錯誤: could not broadcast input array from shape (6,6) into shape (4,4)
                if start_y >= 0 and start_x >= 0 and end_y <= img_h and end_x <= img_w:
                    processed[start_y:end_y, start_x:end_x] = r_rot * 255
                    
    return processed

def apply_blur_and_threshold(cleaned):
    """
    超採樣平滑化，並強制轉回二值圖以利後續處理
    """
    h, w = cleaned.shape[:2]
    img_upscaled = cv2.resize(cleaned, (w * 2, h * 2), interpolation=cv2.INTER_LINEAR)
    img_smoothed = cv2.medianBlur(img_upscaled, 3)
    img_downscaled = cv2.resize(img_smoothed, (w, h), interpolation=cv2.INTER_AREA)
    
    # 邏輯修正：必須進行 Threshold，否則後續的 Pattern Matching 會失效
    _, final_bin = cv2.threshold(img_downscaled, 127, 255, cv2.THRESH_BINARY)
    return final_bin


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

    p.append(np.array([
        [1, 1, 0],
        [1, 1, 0],
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [1, 1, 0]
    ], dtype=np.uint8))
    r.append(np.array([
        [1, 1, 0],
        [1, 1, 0],
        [1, 1, 0],
        [1, 1, 0],
        [1, 1, 0],
        [1, 1, 0]
    ], dtype=np.uint8))

    p.append(np.array([
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [1, 1, 0],
        [1, 0, 0],
        [1, 0, 0]
    ], dtype=np.uint8))
    r.append(np.array([
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0]
    ], dtype=np.uint8))

    p.append(np.array([
        [1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ], dtype=np.uint8))
    r.append(np.array([
        [1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 0, 0],
        [1, 1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
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

def process_file(file_info, patterns):
    """
    file_info: (input_path, output_path)
    """
    input_path, output_path = file_info

    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None: return
    
    # 1. 二值化 (黑底白字)
    _, img_bin = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    # 2. 形態學分離筆畫
    img_bin = reduce_ink_bleeding(img_bin, kernel_size=3)

    # 3. 第一次清理雜點 (針對鋸齒)
    #patterns_255 = [(p * 255, r * 255) for p, r in patterns]
    for idx in range(2):
        #img_bin = apply_pattern_cleaning_fast(img_bin, patterns_255)
        img_bin = apply_pattern_cleaning_hitmiss(img_bin, patterns)

        # 4. 平滑化 (包含強制二值化回歸)
        img_bin = apply_blur_and_threshold(img_bin)

    # 6. 轉回白底黑字
    final_output = cv2.bitwise_not(img_bin)
    cv2.imwrite(output_path, final_output)
    print(f"處理完成: {os.path.basename(output_path)}")

def main():
    parser = argparse.ArgumentParser(description='多進程加速：減少筆畫暈染並清理雜點')
    parser.add_argument('--input', '-i', required=True)
    parser.add_argument('--output', '-o')
    parser.add_argument('--workers', '-w', type=int, default=os.cpu_count(), help='使用的 CPU 核心數')
    args = parser.parse_args()

    patterns = get_patterns()
    
    # 建立檔案清單
    if os.path.isdir(args.input):
        in_dir = args.input
        out_dir = args.output if args.output else f"{in_dir.rstrip('/')}_clean"
        os.makedirs(out_dir, exist_ok=True)
        input_files = []
        for ext in ('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff'):
            input_files.extend(glob(os.path.join(in_dir, ext)))
        
        # 準備 (輸入, 輸出) 路徑對
        tasks = []
        for f in input_files:
            out_f = os.path.join(out_dir, os.path.basename(f))
            tasks.append((f, out_f))
    else:
        out_f = args.output if args.output else f"{os.path.splitext(args.input)[0]}_clean{os.path.splitext(args.input)[1]}"
        tasks = [(args.input, out_f)]

    # 使用 ProcessPoolExecutor 進行多進程並行處理
    print(f"開始處理，使用核心數: {args.workers}，總檔案數: {len(tasks)}")
    
    # 使用 partial 固定 patterns 參數
    worker_func = partial(process_file, patterns=patterns)

    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        # 提交所有任務
        futures = {executor.submit(worker_func, task): task for task in tasks}
        
        for future in as_completed(futures):
            try:
                result = future.result()
                print(result)
            except Exception as e:
                print(f"處理檔案時發生錯誤: {e}")

if __name__ == "__main__":
    main()
