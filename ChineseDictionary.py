import json
import os

class ChineseDictionary:
    def __init__(self, lite: bool = False):
        """
        初始化中文字典，預設使用完整版資料庫。

        :param lite: 如果為 True，則使用精簡版 Dictionary_lite.json
        """
        filename = "Dictionary_lite.json" if lite else "Dictionary.json"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(script_dir, filename)

        if not os.path.exists(data_path):
            raise FileNotFoundError(f"找不到資料檔案: {data_path}")

        with open(data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def unicode(self, char: str) -> int:
        """取得中文字的 Unicode（十進制）"""
        return self.data.get(char, {}).get("unicode", None)

    def unicode_hex(self, char: str) -> str:
        """取得中文字的 Unicode（十六進制）"""
        return self.data.get(char, {}).get("unicode_hex", None)

    def radical(self, char: str) -> str:
        """取得中文字的部首"""
        return self.data.get(char, {}).get("radical", None)

    def radical_count(self, char: str) -> int:
        """取得部首的筆畫數"""
        return self.data.get(char, {}).get("radical_count", None)

    def strokes_count(self, char: str) -> int:
        """取得中文字的非部首筆畫數"""
        return self.data.get(char, {}).get("strokes_count", None)

    def strokes_total(self, char: str) -> int:
        """取得中文字的總筆畫數"""
        return self.data.get(char, {}).get("strokes_total", None)

    def alternate(self, char: str) -> list:
        """取得中文字的異體字"""
        return self.data.get(char, {}).get("alternate", [])

    def semantic_variant(self, char: str) -> list:
        """取得中文字的語義變體"""
        return self.data.get(char, {}).get("semantic_variant", [])

    def pronunciation_mandarin(self, char: str) -> list:
        """取得中文字的普通話拼音（含漢語拼音 & 注音）"""
        return self.data.get(char, {}).get("pronunciation_mandarin", [])

    def pronunciation_cantonese(self, char: str) -> list:
        """取得中文字的粵語拼音"""
        return self.data.get(char, {}).get("pronunciation_cantonese", [])

    def pronunciation_southern_min(self, char: str) -> list:
        """取得中文字的閩南語拼音"""
        return self.data.get(char, {}).get("pronunciation_southern_min", [])

    def component(self, char: str) -> dict:
        """取得中文字的左右部件"""
        return self.data.get(char, {}).get("component", {})

# 測試用例
if __name__ == "__main__":
    dictionary = ChineseDictionary(lite=True)  # 使用精簡版
    char = "姚"
    
    print(f"『{char}』的 Unicode（十進制）: {dictionary.unicode(char)}")
    print(f"『{char}』的 Unicode（十六進制）: {dictionary.unicode_hex(char)}")
    print(f"『{char}』的部首: {dictionary.radical(char)}")
    print(f"『{char}』的部首筆畫數: {dictionary.radical_count(char)}")
    print(f"『{char}』的非部首筆畫數: {dictionary.strokes_count(char)}")
    print(f"『{char}』的總筆畫數: {dictionary.strokes_total(char)}")
    print(f"『{char}』的異體字: {dictionary.alternate(char)}")
    print(f"『{char}』的語義變體: {dictionary.semantic_variant(char)}")
    print(f"『{char}』的普通話拼音: {dictionary.pronunciation_mandarin(char)}")
    print(f"『{char}』的粵語拼音: {dictionary.pronunciation_cantonese(char)}")
    print(f"『{char}』的閩南語拼音: {dictionary.pronunciation_southern_min(char)}")
    print(f"『{char}』的組件: {dictionary.component(char)}")
