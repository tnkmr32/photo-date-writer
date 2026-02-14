"""
Image Effects Module
画像に様々な効果を適用する機能を提供
"""

import numpy as np
from PIL import Image


def apply_film_date_effect(base_img, text_mask, color=(255, 150, 80), intensity=0.5):
    """
    フィルム写真の日付印字を再現する効果を適用
    
    フィルムカメラの日付機能は、フィルムに直接光を照射して日付を焼き込む。
    プリント時には、その部分の輝度が高くなる。この処理を再現する。
    
    Args:
        base_img: PIL Image（ベース画像、RGBモード）
        text_mask: PIL Image（テキストマスク、Lモード。白い部分がテキスト）
        color: tuple（日付の色のRGB値）
        intensity: float（効果の強度 0.0-1.0）
    
    Returns:
        PIL Image: 輝度増加効果を適用した画像
    """
    # PIL ImageをNumPy配列に変換
    base_array = np.array(base_img, dtype=np.float32)
    mask_array = np.array(text_mask, dtype=np.float32) / 255.0  # 0.0-1.0に正規化
    
    # カラー値をNumPy配列に変換
    color_array = np.array(color, dtype=np.float32)
    
    # マスクを3次元に拡張（RGB各チャンネル用）
    mask_3d = mask_array[:, :, np.newaxis]
    
    # 輝度加算: Base + (Mask × Color × Intensity)
    result = base_array + (mask_3d * color_array * intensity)
    
    # 255でクリップ
    result = np.clip(result, 0, 255)
    
    # NumPy配列をPIL Imageに変換
    result_img = Image.fromarray(result.astype(np.uint8))
    
    return result_img
