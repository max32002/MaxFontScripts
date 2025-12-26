import cv2
import numpy as np
import argparse
import os
from glob import glob
from skimage.morphology import skeletonize

def apply_pattern_cleaning_fast(img_bin, patterns_list):
    """
    img_bin: 必須是 uint8, 0/255 格式
    patterns_list: 包含 (pattern_01, replacement_01) 的列表
    """
    # 確保輸入是 0/255
    processed = img_bin.copy()
    
    for p_raw, r_raw in patterns_list:
        # 將 pattern 轉為 0/255 以符合輸入圖
        p_01 = (p_raw > 0).astype(np.uint8) * 255
        r_01 = (r_raw > 0).astype(np.uint8) * 255
        diff_mask = (p_01 != r_01)
        
        for i in range(4):
            p_rot = np.rot90(p_01, k=i)
            r_rot = np.rot90(r_01, k=i)
            d_rot = np.rot90(diff_mask, k=i)
            
            # 使用 TM_SQDIFF，當完全匹配時 res 會是 0
            res = cv2.matchTemplate(processed, p_rot, cv2.TM_SQDIFF)
            loc = np.where(res == 0)
            
            h, w = p_rot.shape
            # 遍歷匹配到的座標
            for pt in zip(*loc[::-1]):
                x, y = pt
                # 取得該區塊
                roi = processed[y:y+h, x:x+w]
                # 只針對 pattern 定義的差異處進行替換
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

def smooth_sharp_edges(img_bin, scale=4):
    # 確保輸入是 255 格式
    if img_bin.max() == 1:
        img_bin = img_bin * 255
        
    h, w = img_bin.shape
    dist_transform = cv2.distanceTransform(img_bin, cv2.DIST_L2, 5)
    skeleton = skeletonize(img_bin > 0).astype(np.uint8) * 255
    
    # 建立放大畫布，使用 LINE_AA 必須背景為 0
    canvas_large = np.zeros((h * scale, w * scale), dtype=np.uint8)
    points = np.column_stack(np.where(skeleton > 0))

    for p in points:
        y, x = p
        radius = dist_transform[y, x]
        
        # 端點偵測
        y_min, y_max = max(0, y-1), min(h, y+2)
        x_min, x_max = max(0, x-1), min(w, x+2)
        neighbor_region = skeleton[y_min:y_max, x_min:x_max]
        is_endpoint = np.sum(neighbor_region) / 255 <= 2

        draw_x = int(x * scale + scale // 2)
        draw_y = int(y * scale + scale // 2)
        
        # 補償參數
        width_compensation = -0.15 # 稍微收縮防止過胖
        length_compensation = 0.5 if is_endpoint else 0.0
        
        final_radius = (radius + width_compensation + length_compensation) * scale
        draw_radius = int(round(final_radius))
        
        if draw_radius > 0:
            cv2.circle(canvas_large, (draw_x, draw_y), draw_radius, 255, -1, lineType=cv2.LINE_AA)

    canvas_large = cv2.medianBlur(canvas_large, 3)
    canvas_small = cv2.resize(canvas_large, (w, h), interpolation=cv2.INTER_AREA)
    _, binary_output = cv2.threshold(canvas_small, 128, 255, cv2.THRESH_BINARY)
    
    return binary_output

def process_file(input_path, output_path, patterns):
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None: return
    
    # 1. 轉為黑底白字 (0/255)
    _, img_bin = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    # 2. 平滑邊緣 (處理 0/255, 回傳 0/255)
    smoothed = smooth_sharp_edges(img_bin, scale=4)
    
    # 3. Pattern 清理 (統一使用 0/255)
    cleaned_bin = apply_pattern_cleaning_fast(smoothed, patterns)
    
    # 4. 轉回白底黑字輸出
    final_output = cv2.bitwise_not(cleaned_bin)
    cv2.imwrite(output_path, final_output)
    
    print(f"已完成: {os.path.basename(output_path)}")


def main():
    parser = argparse.ArgumentParser(description='批次處理圖片中的特定雜點樣式')
    parser.add_argument('--input', '-i', required=True, help='輸入圖片路徑或資料夾')
    parser.add_argument('--output', '-o', help='輸出路徑或資料夾')
    
    args = parser.parse_args()
    patterns = get_patterns()

    if os.path.isdir(args.input):
        # 資料夾模式
        in_dir = args.input
        out_dir = args.output if args.output else f"{in_dir.rstrip('/')}_clean"
        
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        
        # 支援多種常見格式
        extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff']
        files = []
        for ext in extensions:
            files.extend(glob(os.path.join(in_dir, ext)))

        print(f"開始批次處理，共 {len(files)} 個檔案...")
        for f in files:
            fname = os.path.basename(f)
            out_f = os.path.join(out_dir, fname)
            process_file(f, out_f, patterns)
    else:
        # 單一檔案模式
        if args.output:
            out_path = args.output
        else:
            base, ext = os.path.splitext(args.input)
            out_path = f"{base}_clean{ext}"
        process_file(args.input, out_path, patterns)

if __name__ == "__main__":
    main()